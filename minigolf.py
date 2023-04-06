import sys
import argparse

parser = argparse.ArgumentParser(description="minigolf")
parser.add_argument('file', metavar = "<file>", nargs = '?',
                        type = str)
parser.add_argument('-t',
                    action = "store_true",
                    help = "Print only TOS at the end of the program")

args = parser.parse_args()

code = open(args.file).read()

stack = []

inputs = []

ins = sys.stdin.read().split("\n")
for i in ins[:-1]:
    inputs.append(eval(i))

inputs = list(inputs)

inputs_idx = 0

def parse(code: str) -> list:
    result = []
    for idx, i in enumerate(code):
        if i == ";": # end_for
            temp = []
            while result[-1] != ",":
                temp = [result.pop()] + temp
            result.pop()
            result.append(temp)
        else: # other
            result.append(i)
    return result

def run(ast: list, n = 2):
    for i in ast:
        if type(i) == list: # for loop
            if stack[-1] == list: # foreach
                temp_list = stack.pop()
                for n_alt in temp_list:
                    run(i, n_alt)
            elif stack[-1] == -1: # filter loop
                pass
            else: # [ 1..n ] foreach
                tmp = stack.pop()
                for n_alt in range(1, tmp+1):
                    run(i, n_alt)
        elif i == ":": # dup
            stack.append(stack[-1])
        elif i == "s": # swap
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif i == "*": # mul / sum
            if type(stack[-1]) == list:
                stack.append(sum(stack.pop()))
            else:
                stack.append(stack.pop() * stack.pop())
        elif i == "+": # add / length
            if type(stack[-1]) == list:
                stack.append(len(stack.pop()))
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

run(parse(code))

if args.t: # output last item
    print(stack[-1])
else:
    print("\n".join(map(str,stack)))
