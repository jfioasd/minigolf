# minigolf
A stack-based esolang inspired by Vyxal's and Factor's corpus.

The current instructions are as follows:
| Command | Overload | Description |
| :-----: | :------: | :---------: |
| `, ... ;`     | (int / float)    | map over `[1..int(n)]` |
|         | (list)   | map over TOS |
| `:`     | (any)    | Duplicate TOS |
| `s`     | (any, any) | Swap. |
| `*`     | (int/list, int) | Multiply. (Vectorizes) |
|         | (ND list) | Flatten. |
| `+`     | (int/list, int) | Add. (Vectorizes) |
|         | (list) | Sum. (Vectorizes at depth 1) |
| `i`     |        | Push next (cyclic) input (or `-1` if input is empty)|
| `n`     |        | Push current item in map (or `2` if outside of loop) |
| `=`     | (list/int, int) | Equality. |
|         | (list) | Transpose a list. |

Those commands were added later in order to make minigolf easier to program in:

| Command | Overload | Description |
| :-----: | :------: | :---------: |
| `[ ... ]` | / | Push an array of codepoints onto the stack|
| `x`     |        | Push current 0-based iteration index in map (or `32` if outside of loop) |
| `a`     |        | Push current value of accumulator (initially `20`) |
| `e`     |        | Copy TOS to Acc, does not pop TOS. |
| `u`     |        | Pop TOS to Acc. |
| `v`     | (any, any) | Over: `( ... a b -- ... a b a )` |
| `<`     | (int, int) | Less than. |
|         | (list, list) | Lexicographically less than (like in Python). |
| `#`     | (list) | Length of a list. |
| `o`     | (list) | Reverse a list. |
|         | (int)  | X + 1. |
| `y`     | (list)     | Uniquify (preserves order). |
|         | (int)      | 2 ** X. |
| `%`     | (int, int) | Modulo. |
| `!`     | (any)      | Logical not - see definition of minigolf truthy below. |

minigolf's truthiness is defined like this:
* if `N` is a list, it's truthy iff `len(N) >= 1`.
* if `N` is a number, it's truthy iff `N >= 1`.

Additionally, the following characters transpile to their equivalent minigolf substring:

| Character | Replacement |
| :-------: | :---------: |
| `_`       | `0;++` (useful for foreach loops) |

## I/O method
Input is separated by newlines. It can contain lists of ints or integers. Additionally, strings push a list of codepoints.

If there aren't enough stack items for a word's arity at any point in execution, then enough cyclic implicit inputs (analogous to `i`) are prepended to the stack.

The entire stack is implicitly outputted after the program.

## Map loop
If `;` is at the end of the program, it can be omitted from the program.

The map loop executes the code with `n` as the current iteration variable.

map pops TOS after each iteration, and pushes a list of each popped item after the loop.

## Misc.
Since it's terrible at pushing constants, I've added a lot of 1-byte constants into minigolf (which hopefully makes it easier to program in). These constants can be found within the source code.

There are also a few flags, which could be found by reading the code.
