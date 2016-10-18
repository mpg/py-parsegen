This is just me playing with grammars, parser generators, etc.

References used:
[TRDB] The Red Dragon Book
    Aho, Sethi, Ullman: Compilers: Principles, Techniques and Tools, 1st Ed
[A2C2] Alex Aiken's Compilers Course
    https://lagunita.stanford.edu/courses/Engineering/Compilers/Fall2014/about
    https://web.stanford.edu/class/cs143/

All the code here is written by Manuel Pégourié-Gonnard in 2016
and distributed under the terms of the WTFPL v2.

This is a project for fun and self-education, as a consequence:
- it has 100% test coverage
- input/error handling is quite primitive

In particular when writing grammars, as well as sentences to be parsed,
tokens need to be separated by whitespace, eg "( id + id ) * id",
not "(id + id) * id". I know it's annoying, but see above.
