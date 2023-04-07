import sys
import argparse

parser = argparse.ArgumentParser(description="minigolf")
parser.add_argument('file', nargs = 1,
                        type = str)
parser.add_argument('-t',
                    action = "store_true",
                    help = "Print only TOS at the end of the program")

args = parser.parse_args()

code = open(args.file[0]).read()

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
            while result[-1] not in (",", "_"):
                temp = [result.pop()] + temp
            l = result.pop()
            result.append([l] + temp)
        else: # other
            result.append(i)
    return result

def run(ast: list, n = 2):
    for i in ast:
        if type(i) == list: # for loop / map loop
            x = i[0]
            i = i[1:]
            if x == ",": # foreach
                if stack[-1] == list: # foreach
                    temp_list = stack.pop()
                    for n_alt in temp_list:
                        run(i, n_alt)
                else: # [ 1..n ] foreach
                    tmp = stack.pop()
                    for n_alt in range(1, tmp+1):
                        run(i, n_alt)
            else: # `_` map loop
                if stack[-1] == list: # map each
                    temp_list = stack.pop()
                    result = []
                    for n_alt in temp_list:
                        run(i, n_alt)
                        result.append(stack.pop())
                    stack.append(result)
                else: # map [ 1..n ]
                    tmp = stack.pop()
                    result = []
                    for n_alt in range(1, tmp+1):
                        run(i, n_alt)
                        result.append(stack.pop())
                    stack.append(result)
        elif i == ":": # dup
            stack.append(stack[-1])
        elif i == "s": # swap
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif i == "*": # mul / sum
            if type(stack[-1]) == list: # (list) - sum
                stack.append(sum(stack.pop()))
            elif type(stack[-2]) == list: # (list, int) - vectorize
                a, b = stack.pop(), stack.pop()
                r = []
                for i in b:
                    r.append(i * a)
                stack.append(r)
            else: # (int, int) - a * b
                stack.append(stack.pop() * stack.pop())
        elif i == "+": # add / length
            if type(stack[-1]) == list: # (list) - length
                stack.append(len(stack.pop()))
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

run(parse(code))

if args.t: # output last item
    print(stack[-1])
else:
    print("\n".join(map(str,stack)))
