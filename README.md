# minigolf
A minimalist stack-based esolang inspired by Vyxal's corpus.

The current instructions are as follows:
| Command | Overload | Description |
| :-----: | :------: | :---------: |
| `$ ... $` | / | Push an array of codepoints onto the stack|
| `, ... ;`     | (int / float)    | map over `[1..int(n)]` |
|         | (list)   | map over TOS |
| `:`     | (any)    | Duplicate TOS |
| `*`     | (int/list, int) | Multiply. (Vectorizes) |
|         | (ND list) | Flatten. |
| `+`     | (int/list, int) | Add. (Vectorizes) |
|         | (list) | Sum. (Vectorizes at depth 1) |
| `i`     |        | Push next (cyclic) input (or `-1` if input is empty)|
| `n`     |        | Push current item in map (or `2` if outside of loop) |
| `s`     | (any, any) | Swap. |
| `v`     | (any, any) | Over: `( ... a b -- ... a b a )` |
| `w`     | (any, any) | Nip: `( ... a b -- ... b )`
| `=`     | (list/int, int) | Equality. (Vectorizes) |
|         | (list, list) | Zip two lists together. |
| `<`     | (int, int) | Less than. |
| `#`     | (list) | Length of a list. |
| `o`     | (list) | Reverse a list. |
| `%`     | (int, int) | Modulo. |
| `/`     | (int, int) | Integer division. |



Additionally, the following characters transpile to their equivalent minigolf substring:

| Character | Replacement |
| :-------: | :---------: |
| `_`       | `0;++` (useful for foreach loops) |

Input is separated by newlines. It can contain lists of ints or integers. Additionally, strings push a list of codepoints.

The entire stack is implicitly outputted after the program.

The map loop executes the code with `n` as the current iteration variable.

map pops TOS after each iteration, and pushes a list of each popped item after the loop.

Since it's terrible at pushing constants, I've added a lot of 1-byte constants into minigolf (which hopefully makes it easier to program in). These constants can be found within the source code.

There are also a few flags, which could be found by reading the code.
