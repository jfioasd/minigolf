# minigolf
A minimalist stack-based esolang inspired by stack-based golfing languages. It only has 8 instructions:
| Command | Overload | Description |
| :-----: | :------: | :---------: |
| `,`     | (int)    | for loop `[1..n]` |
|         | (list)   | for each loop in TOS |
| `:`     | (any)    | duplicate TOS |
| `;`     |          | End a for loop structure |
| `*`     | (int, int) | Multiply top two stack items |
|         | (list) | Sum of TOS |
| `+`     | (int, int) | Add top two stack items |
|         | (list) | Length of TOS |
| `i`     |        | Request the next (cyclic) input |
| `n`     |        | Current item in for loop (or `2` if outside of loop) |
| `s`     |        | swap top two stack items |
