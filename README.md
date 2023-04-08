# minigolf
A minimalist stack-based esolang inspired Vyxal's corpus.

It currently has 8 instructions:
| Command | Overload | Description |
| :-----: | :------: | :---------: |
| `, ... ;`     | (int)    | for loop `[1..n]` |
|         | (list)   | foreach loop over TOS |
| `:`     | (any)    | duplicate TOS |
| `_ ... ;`     | (int)     | map over `[1..n]` |
|         | (list) | map loop over TOS |
| `*`     | (int, int) | Multiply top two stack items |
|         | (list, int) | Vectorize |
|         | (2D list) | Flatten TOS |
|         | (1D list) | Sum of TOS |
| `+`     | (int, int) | Add top two stack items |
|         | (list, int) | Vectorize |
|         | (list) | Length of TOS |
| `i`     |        | Request the next (cyclic) input (or `-1` if input is empty)|
| `n`     |        | Current item in for loop (or `2` if outside of loop) |
| `s`     |        | swap top two stack items |

Input is separated by newlines. It can contain lists of ints or integers. Additionally, strings push a list of codepoints.

The entire stack is implicitly outputted after the program.

Specifically, the for loop executes the code with `n` as the current iteration variable; it has no side effects.

However, the map loop `_ ... ;` pops TOS after each iteration, and pushes a list of each popped item after the loop.

Since it's terrible at pushing constants, I've added a lot of 1-byte constants into minigolf (which hopefully makes it easier to program in). These constants can be found within the source code.

There are also a few flags, which could be found by reading the code.
