# minigolf
A minimalist stack-based esolang inspired by Nibbles and Vyxal's corpus.

It uses a custom 8-character octal 'codepage' (currently not implemented):
| 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | 
| `,` | `:` | `;` | `*` | `+` | `i` | `s` | `n` |

It currently has 8 instructions:
| Command | Overload | Description |
| :-----: | :------: | :---------: |
| `,`     | (int)    | for loop `[1..n]` |
|         | (list)   | foreach loop over TOS |
| `:`     | (any)    | duplicate TOS |
| `;`     |          | End a for loop structure |
| `*`     | (int, int) | Multiply top two stack items |
|         | (list) | Sum of TOS |
| `+`     | (int, int) | Add top two stack items |
|         | (list) | Length of TOS |
| `i`     |        | Request the next (cyclic) input (or `-1` if input is empty)|
| `n`     |        | Current item in for loop (or `2` if outside of loop) |
| `s`     |        | swap top two stack items |

Input is separated by newlines. It can contain lists of ints or integers.

The entire stack is implicitly outputted after the program.

The for loop is written like `, ... ;`.

## TODO
* Make `s+` push `-1`
* Swap foreach w/ map and make foreach a 2-octet operation.
* Add implicit input
* Add implicit `;` completion
* Implement `+` and `*` vectorization
* Implement some more flags
* Implement source code octal encoding / decoding
* Maybe make `n` and `s` introduce 2-octet instructions.
* Charcode I/O flag.
  * strings would push list of codepoints (ord)
  * an integer list (of codepoints) would output a string (chr)
