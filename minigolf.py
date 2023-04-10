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

ins = sys.stdin.read().split("\n")
for i in ins[:-1]:
    curr = eval(i)
    if type(curr) == str:
        inputs.append(list(map(ord, curr)))
    else:
        inputs.append(curr)

inputs = list(inputs)

inputs_idx = 0

def parse(code: str) -> list:
    result = []
    for idx, i in enumerate(code):
        if i == ";": # end_for
            temp = []
            while result[-1] != ",":
                temp = [result.pop()] + temp
            l = result.pop()
            result.append([l] + temp)
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

def run(ast: list, n = 2):
    for i in ast:
        if type(i) == list: # map loop
            i = i[1:]
            tmp = stack.pop()
            result = []
            if type(tmp) != list: # map each
                tmp = range(1, int(tmp+1))

            for n_alt in tmp:
                run(i, n_alt)
                result.append(stack.pop())

            stack.append(result)

        elif i == ":": # dup
            stack.append(stack[-1])

        elif i == "s": # swap
            stack[-1], stack[-2] = stack[-2], stack[-1]

        elif i == "*": # mul / flatten
            if type(stack[-1]) == list: # (list) - flatten
                stack.append(flatten(stack.pop()))

            elif type(stack[-2]) == list: # (list, int) - vectorize
                a, b = stack.pop(), stack.pop()
                r = []
                for i in b:
                    r.append(i * a)
                stack.append(r)

            else: # (int, int) - a * b
                stack.append(stack.pop() * stack.pop())

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

        elif i == "n": # current foreach item / 2
            stack.append(n)

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

        elif i == "=": # vectorizing equality
            if type(stack[-2]) == list: # (list, list): a == b vectorizes
                # (list, int) also vectorizes
                a, b = stack.pop(), stack.pop()
                res = []

                if type(a) == list: # (list, list)
                    for i, j in zip(a, b):
                        res.append(int(i == j))
                else: # (list, int)
                    for i in b:
                        res.append(int(i == a))

                stack.append(res)

            else: # (int, int): a == b
                stack.append(int(stack.pop() == stack.pop()))

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
            r.append("".join(map(chr, i)))
        else:
            r.append(i)
    stack = r

print("\n".join(map(str,stack)))
