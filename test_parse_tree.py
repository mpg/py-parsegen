#!/usr/bin/python3
# coding: utf-8

from parse_tree import ParseTree as PT
import unittest


class KnownValues(unittest.TestCase):
    # this is the parse tree of "id + id * id" using
    # grammar 4.11 p 176 (see also Fig 4.16 p. 188) of [TRDB]
    sample_tree = PT("E", [
        PT("T", [
            PT("F", [PT("id")]),
            PT("T'", [PT("")]),
            ]),
        PT("E'", [
            PT("+"),
            PT("T", [
                PT("F", [PT("id")]),
                PT("T'", [
                    PT("*"),
                    PT("F", [PT("id")]),
                    PT("T'", [PT("")]),
                ]),
            ]),
            PT("E'", [PT("")]),
        ]),
    ])

    sample_lines = (
            "E",
            "| T",
            "| | F",
            "| | | id",
            "| | T'",
            "| | | ε",
            "| E'",
            "| | +",
            "| | T",
            "| | | F",
            "| | | | id",
            "| | | T'",
            "| | | | *",
            "| | | | F",
            "| | | | | id",
            "| | | | T'",
            "| | | | | ε",
            "| | E'",
            "| | | ε",
    )

    def test_lines(self):
        """Check lines() method against know result"""
        t_lines = tuple(self.sample_tree.lines())
        self.assertEqual(t_lines, self.sample_lines)

    sample_str = """E
| T
| | F
| | | id
| | T'
| | | ε
| E'
| | +
| | T
| | | F
| | | | id
| | | T'
| | | | *
| | | | F
| | | | | id
| | | | T'
| | | | | ε
| | E'
| | | ε"""

    def test_str(self):
        """Check str() against known result"""
        self.assertEqual(str(self.sample_tree), self.sample_str)


if __name__ == "__main__":  # pragma: no branch
    unittest.main()
