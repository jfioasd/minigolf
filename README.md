# minigolf
A minimalist stack-based esolang inspired Vyxal's corpus.

It currently has 8 instructions:
| Command | Overload | Description |
| :-----: | :------: | :---------: |
| `, ... ;`     | (int / float)    | map loop `[1..int(n)]` |
|         | (list)   | map loop over TOS |
| `:`     | (any)    | duplicate TOS |
| `*`     | (int, int) | Multiply top two stack items |
|         | (list, int) | Vectorize |
|         | (ND list) | Flatten TOS (N > 1) |
|         | (1D list) | Sum of TOS |
| `+`     | (int, int) | Add top two stack items |
|         | (list, int) | Vectorize |
|         | (list) | Length of TOS |
| `i`     |        | Request the next (cyclic) input (or `-1` if input is empty)|
| `n`     |        | Current item in map loop (or `2` if outside of loop) |
| `s`     |        | swap top two stack items |
| `=`     | (int, int) | int(a == b) |
|         | (list, int) | vectorizes |
|         | (list, list) | vectorizes |

Input is separated by newlines. It can contain lists of ints or integers. Additionally, strings push a list of codepoints.

The entire stack is implicitly outputted after the program.

Specifically, the map loop executes the code with `n` as the current iteration variable; it has no side effects.

map pops TOS after each iteration, and pushes a list of each popped item after the loop.

Since it's terrible at pushing constants, I've added a lot of 1-byte constants into minigolf (which hopefully makes it easier to program in). These constants can be found within the source code.

There are also a few flags, which could be found by reading the code.
