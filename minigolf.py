import sys
import argparse

parser = argparse.ArgumentParser(description="minigolf")
parser.add_argument('file',
                        type = str)

parser.add_argument('-v',
                    action = "store_true",
                    help = "Print minigolf version (for checking ATO updates)")

parser.add_argument('-c',
                    action = "store_true",
                    help = "Output list of codepoints as a string")

args = parser.parse_args()

if args.v:
    print("v0.3")
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

def parse(code: str) -> list:
    result = []
    is_str = False
    for idx, i in enumerate(code):
        if is_str:
            if i == '$': # End codepoint string
                temp = ""
                while result[-1] != '$':
                    temp = result.pop() + temp
                result.append(list(result.pop() + temp))
                is_str = False
            else:
                result.append(i)
        elif is_str == False and i == '$': # begin codepoint string
            is_str = True
            result.append("$")
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

def to_base(orig, base):
    digits = []
    while orig > 0:
        digits = [orig % base] + digits
        orig //= base
    return digits

def uniquify(x):
    o = []
    for i in x:
        if i not in o:
            o.append(i)
    return o

def in_chunks_n(x, l_chunk):
    o = []
    while len(x) > 0:
        o.append(x[0:l_chunk])
        x = x[l_chunk:]
    return o

def run(ast: list, n = 2, x = 32):
    acc = 20 # Very nice for some golfing.

    for i in ast:
        if type(i) == list: # Map or string.
            h, i = i[0], i[1:]
            if h == ",": # Map loop
                tmp = stack.pop()
                result = []
                if type(tmp) != list: # map each
                    tmp = range(1, int(tmp+1))

                for x_alt, n_alt in enumerate(tmp):
                    run(i, n_alt, x_alt)
                    result.append(stack.pop())

                stack.append(result)
            elif h == "$": # str
                stack.append(list(map(ord, i)))

        elif i == "x": # Push x
            stack.append(x)

        elif i == ":": # dup
            stack.append(stack[-1])

        elif i == "s": # swap
            stack[-1], stack[-2] = stack[-2], stack[-1]

        elif i == "v": # over
            stack.append(stack[-2])

        elif i == "w": # nip
            del stack[-2]

        elif i == "*": # mul / flatten
            if type(stack[-1]) == list: # (list) - flatten
                stack.append(flatten(stack.pop()))

            elif type(stack[-2]) == list: # (list, int) - vectorize
                a, b = stack.pop(), stack.pop()
                r = []
                for i in b:
                    r.append(int(i * a))
                stack.append(r)

            else: # (int, int) - a * b
                stack.append(int(stack.pop() * stack.pop()))

        elif i == "+": # add / sum
            if type(stack[-1]) == list: # (list) - sum
                stack.append(v_sum(stack.pop()))

            elif type(stack[-2]) == list: # (list, int) - vectorize
                a, b = stack.pop(), stack.pop()
                r = []
                for i in b:
                    r.append(i + a)
                stack.append(r)

            else:
                stack.append(stack.pop() + stack.pop())

        elif i == "@": # Indexing (vectorizes).
            R, L = stack.pop(), stack.pop()
            if type(R) == int: # Regular indexing (Python).
                stack.append(L[R])
            elif type(R) == list: # Vectorized indexing (good for slices).
                o = []
                for j in R:
                    if j >= 0 and j < len(R):
                        o.append(L[j])
                stack.append(o)

        elif i == "/": # Integer division (does not vectorize)
            R, L = stack.pop(), stack.pop()
            stack.append(L // R)

        elif i == "%": # Modulo (does not vectorize)
            R, L = stack.pop(), stack.pop()
            stack.append(L % R)

        elif i == "n": # current foreach item / 2
            stack.append(n)

        elif i == "a": # Push acc value
            stack.append(acc)

        elif i == "e": # Tee TOS to acc (does not pop)
            acc = stack[-1]

        elif i == "u": # Pop TOS to acc.
            acc = stack.pop()

        elif i == "d": # Wrap in chunks of length x.
            R, L = stack.pop(), stack.pop()
            stack.append(in_chunks_n(L, R))

        elif i == "i": # request next (cyclic) input
            # or push -1 if input is empty.
            if len(inputs) == 0:
                stack.append(-1)
            else:
                global inputs_idx
                stack.append(inputs[inputs_idx])
                inputs_idx += 1
                if inputs_idx == len(inputs):
                    inputs_idx = 0

        elif i == "o": # reverse TOS
            stack.append(list(reversed(stack.pop())))

        elif i == "b": # Convert to base N
            R, L = stack.pop(), stack.pop()
            stack.append(to_base(L, R))

        elif i == "y": # Uniquify TOS
            stack.append(uniquify(stack.pop()))

        elif i == "#": # Length of TOS
            stack.append(len(stack.pop()))

        elif i == "=": # vectorizing equality
            if type(stack[-2]) == list: # (list, int): a == b vectorizes
                # (list, list) zip two lists together
                a, b = stack.pop(), stack.pop()
                res = []

                if type(a) == list: # (list, list) - zip.
                    for i, j in zip(a, b):
                        res.append([j, i])
                else: # (list, int)
                    for i in b:
                        res.append(int(i == a))

                stack.append(res)

            else: # (int, int): a == b
                stack.append(int(stack.pop() == stack.pop()))

        elif i == "<": # Less than. Scalar only
            R, L = stack.pop(), stack.pop()
            stack.append(int(L < R))

        elif i == "-": # Subtraction.
            R, L = stack.pop(), stack.pop()
            stack.append(L - R)

        elif i in "0123456789": # push respective digit
            stack.append(int(i))
        elif i in "ABCDEFGH": # 10 - 17
            stack.append(10 + "ABCDEFGH".find(i))
        elif i in "IJKLMNOPQRST": # -12 - -1
            stack.append(-12 + "IJKLMNOPQRST".find(i))
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

print("\n".join(map(str,stack)))
