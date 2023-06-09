import sys
import math
import argparse

sys.setrecursionlimit(1 << 30) # Allow deeper recursive calls.

parser = argparse.ArgumentParser(description="minigolf")
parser.add_argument('file',
                        type = str)

parser.add_argument('-v',
                    action = "store_true",
                    help = "Print minigolf version (for checking ATO updates)")

parser.add_argument('-c',
                    action = "store_true",
                    help = "Output list of codepoints as a string")

parser.add_argument('-t',
                    action = "store_true",
                    help = "Only print TOS at the end of execution")

args = parser.parse_args()

if args.v:
    print("v0.6")
    exit(0)

code = open(args.file).read()

stack = []

inputs = []

ins = (sys.stdin.read()+"\n").split("\n")
for i in ins[:-1]:
    if len(i) > 0:
        curr = eval(i)
        if type(curr) == str:
            inputs.append(list(map(ord, curr)))
        else:
            inputs.append(curr)

inputs = list(inputs)

inputs_idx = 0

def parse(code):
    result = []
    in_str = 0
    s = ""
    for idx, i in enumerate(code):
        if in_str:
            if i == '[': in_str += 1
            elif i == ']':
                in_str -= 1
                if in_str == 0:
                    result.append(list(s))
                    s = ""
            s += i
            continue
        if i == '[': # Begin codepoint string
            in_str += 1
            s = "["
        elif i == ";" or i == "_": # end_for
            temp = []
            while result[-1] != ",":
                temp = [result.pop()] + temp
            l = result.pop()
            other_temp = [l] + temp
            if i == "_":
                other_temp += ["0"]
            other_temp += [";"]
            result.append(other_temp)
            if i == "_":
                result.append("+")
                result.append("+")
        else: # other
            result.append(i)

    for i in result:
        if i == ",":
            result.append(";")
    if "," in result:
        return parse(result)

    return result

def flatten(a):
    result = []
    for i in a:
        if type(i) == list:
            result += flatten(i)
        else:
            result.append(i)
    return result

def v_sum(a):
    try:
        return sum(a)
    except:
        return list(map(v_sum,a))

def minigolf_truthify(x):
    if type(x) == list:
        if len(x) >= 1: return 1
        else: return 0
    else:
        if x >= 1: return 1
        else: return 0

def split_by(X, sep):
    s = sep[0]
    o = [[]]
    for i in X:
        if i == s:
            o.append([])
        else:
            o[-1].append(i)
    return o

def v_add(LHS, RHS):
    if type(LHS) != list:
        return LHS + RHS
    else:
        o = []
        for i in LHS:
            o.append(v_add(i, RHS))
        return o

def transpose(L):
    if type(L[0]) == int:
        return list(map(lambda x: [x],L))
    o = list(map(list,zip(*L)))
    if len(o) == 1: o = o[0]
    return o

printed = False

arities = {
    ":": 1,
    "*": 1, # treat 2 separately
    "+": 1, # treat 2 separately
    "u": 1,
    "s": 2,
    "v": 2,
    "=": 1, # Handle separately in code
    "<": 2,
    "#": 1,
    "o": 1,
    "y": 1,
    "%": 2,
    "/": 1, # Handle separately in code.
    "!": 1
}

acc = 20 # Very nice for some golfing.

def run(ast: list, n = 2, x = 32):
    global acc
    global stack
    global inputs_idx

    for i in ast:
        if type(i) == str and i in arities.keys() and len(stack) < arities[i]:
            # Rudimentary Implicit input
            # (takes inputs under the stack)
            for j in range(arities[i] - len(stack)):
                # Copy code for `i` here
                if len(inputs) == 0:
                    stack = [-1] + stack
                else:
                    stack = [inputs[inputs_idx]] + stack
                    inputs_idx += 1
                    if inputs_idx == len(inputs):
                        inputs_idx = 0

        if type(i) == list: # Map or string.
            h, i = i[0], i[1:]
            if h == ",": # Map loop
                if len(stack) == 0:
                    stack = [inputs[inputs_idx]] + stack
                    inputs_idx += 1
                    if inputs_idx == len(inputs):
                        inputs_idx = 0
                tmp = stack.pop()
                result = []
                if type(tmp) != list: # map each
                    tmp = range(1, int(tmp+1))

                for x_alt, n_alt in enumerate(tmp):
                    run(i, n_alt, x_alt)
                    result.append(stack.pop())

                stack.append(result)
            elif h == "[": # str
                stack.append(list(map(ord, i)))

        elif i == "x": # Push x
            stack.append(x)

        elif i == ":": # dup
            stack.append(stack[-1])

        elif i == "s": # swap
            stack[-1], stack[-2] = stack[-2], stack[-1]

        elif i == "v": # over
            stack.append(stack[-2])

        elif i == "!": # Logical not TOS.
            stack.append(1 - minigolf_truthify(stack.pop()))

        elif i == "&": # Call TOS / Call TOS with arg.
            if type(stack[-1]) == list: # Direct call w/ no args.
                a = "".join(map(chr,stack.pop()))
                run(parse(a))
            else: # Call with n = TOS.
                n_alt = stack.pop()
                a = "".join(map(chr,stack.pop()))
                run(parse(a), n_alt)

        elif i == "P": # Print (temporary operation)
            print(stack.pop())
            printed = True

        elif i == "*": # mul / flatten
            if type(stack[-1]) == list: # (list) - flatten
                stack.append(flatten(stack.pop()))

            else: # Dyadic case
                if len(stack) == 1:
                    if len(inputs) == 0:
                        stack.append(-1)
                    else:
                        stack.append(inputs[inputs_idx])
                        inputs_idx += 1
                        if inputs_idx == len(inputs):
                            inputs_idx = 0
                if type(stack[-2]) == list: # (list, int) - vectorize
                    a, b = stack.pop(), stack.pop()
                    r = []
                    for i in b:
                        r.append(i * a)
                    stack.append(r)

                else: # (int, int) - a * b
                    stack.append(stack.pop() * stack.pop())

        elif i == "+": # add / sum
            if type(stack[-1]) == list: # (list) sum / vertical sum
                a = stack.pop()
                if a == []:
                    stack.append(0)
                elif type(a[0]) != list:
                    stack.append(sum(a))
                else: # 2D - sum (implicit transpose)
                    stack.append(v_sum(transpose(a)))
            else:
                if len(stack) == 1:
                    if len(inputs) == 0:
                        stack.append(-1)
                    else:
                        stack.append(inputs[inputs_idx])
                        inputs_idx += 1
                        if inputs_idx == len(inputs):
                            inputs_idx = 0
                if type(stack[-2]) == list: # (list, int) - vectorize
                    R, L = stack.pop(), stack.pop()
                    stack.append(v_add(L, R))

                else:
                    stack.append(stack.pop() + stack.pop())

        elif i == "%": # Modulo (does not vectorize)
            R, L = stack.pop(), stack.pop()
            stack.append(L % R)

        elif i == "/": # Division (does not vectorize)
            # Or transpose for lists.
            R = stack.pop()
            if type(R) == list:
                stack.append(transpose(R))
            else:
                if len(stack) == 0:
                    if len(inputs) == 0:
                        stack.append(-1)
                    else:
                        stack.append(inputs[inputs_idx])
                        inputs_idx += 1
                        if inputs_idx == len(inputs):
                            inputs_idx = 0
                L = stack.pop()
                stack.append(L // R)


        elif i == "n": # current foreach item / 2
            stack.append(n)

        elif i == "a": # Push acc value
            stack.append(acc)

        elif i == "u": # Pop TOS to acc.
            acc = stack.pop()

        elif i == "i": # request next (cyclic) input
            # or push -1 if input is empty.
            if len(inputs) == 0:
                stack.append(-1)
            else:
                stack.append(inputs[inputs_idx])
                inputs_idx += 1
                if inputs_idx == len(inputs):
                    inputs_idx = 0

        elif i == "o": # reverse TOS / x + 1
            L = stack.pop()
            if type(L) == list:
                stack.append(list(reversed(L)))
            else:
                stack.append(L + 1)

        elif i == "y": # 2 ** x
            L = stack.pop()
            stack.append(2 ** L)

        elif i == "#": # Length of TOS
            L = stack.pop()
            stack.append(len(L))

        elif i == "=": # equality
            if len(stack) == 1:
                if len(inputs) == 0:
                    stack.append(-1)
                else:
                    stack.append(inputs[inputs_idx])
                    inputs_idx += 1
                    if inputs_idx == len(inputs):
                        inputs_idx = 0
            stack.append(int(stack.pop() == stack.pop()))

        elif i == "<": # Less than. Scalar only
            R, L = stack.pop(), stack.pop()
            stack.append(int(L < R))

        elif i in "0123456789": # push respective digit
            stack.append(int(i))
        elif i in "ABCDEFGH": # 10 - 17
            stack.append(10 + "ABCDEFGH".find(i))
        elif i == "I": # 32
            stack.append(32)
        elif i == "J": # 20
            stack.append(20)
        elif i in "KLMNOPQRST": # -10 - -1
            stack.append(-10 + "KLMNOPQRST".find(i))
        elif i == "U": # 0.5
            stack.append(0.5)
        elif i == "V": # 256
            stack.append(256)
        elif i == "W": # 100
            stack.append(100)
        elif i == "X": # 1024
            stack.append(1024)
        elif i == "Y": # 128
            stack.append(128)
        elif i == "Z": # 1000
            stack.append(1000)

run(parse(code))

if args.c: # output strings from list of codepoints
    r = []
    for i in stack:
        if type(i) == list:
            if type(i[0]) == list: # >= 2D
                i = map(flatten, i)
                x = []
                for j in i:
                    if type(j) == list:
                        x.append(list(map(chr,j)))
                    else:
                        x.append(chr(j))
                r.append("\n".join(map(lambda o:"".join(o), x)))
            else:
                r.append("".join(map(chr, i)))
        else:
            r.append(chr(i))
    stack = r

if not printed:
    if args.t:
        print(stack[-1])
    else:
        print("\n".join(map(str,stack)))
