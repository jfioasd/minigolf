# minigolf
A minimalist stack-based esolang inspired Vyxal's corpus.

It currently has 9 instructions:
| Command | Overload | Description |
| :-----: | :------: | :---------: |
| `, ... ;`     | (int)    | for loop `[1..n]` |
|         | (list)   | foreach loop over TOS |
| `:`     | (any)    | duplicate TOS |
| `_ ... ;`     | (int)     | map over `[1..n]` |
|         | (list) | map loop over TOS |
| `*`     | (int, int) | Multiply top two stack items |
|         | (list, int) | Vectorize |
|         | (list) | Sum of TOS |
| `+`     | (int, int) | Add top two stack items |
|         | (list, int) | Vectorize |
|         | (list) | Length of TOS |
| `i`     |        | Request the next (cyclic) input (or `-1` if input is empty)|
| `n`     |        | Current item in for loop (or `2` if outside of loop) |
| `s`     |        | swap top two stack items |

Input is separated by newlines. It can contain lists of ints or integers.

The entire stack is implicitly outputted after the program.

Specifically, the for loop executes the code with `n` as the current iteration variable; it has no side effects.

However, the map loop `_ ... ;` pops TOS after each iteration, and pushes a list of each popped item after the loop.

## TODO
* Make `s+` push `-1`
* Implement some more flags
* Charcode I/O flag.
  * strings would push list of codepoints (ord)
  * an integer list (of codepoints) would output a string (chr)
