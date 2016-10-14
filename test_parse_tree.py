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
        """ParseTree: check lines() against know result"""
        t_lines = tuple(self.sample_tree.lines())
        self.assertEqual(t_lines, self.sample_lines)

    sample_str = "('E', 2 children)"

    def test_str(self):
        """ParseTRee: check str() against known result"""
        self.assertEqual(str(self.sample_tree), self.sample_str)

    sample_leftmost = (
            "E",
            "T E'",
            "F T' E'",
            "id T' E'",
            "id  E'",
            "id  + T E'",
            "id  + F T' E'",
            "id  + id T' E'",
            "id  + id * F T' E'",
            "id  + id * id T' E'",
            "id  + id * id  E'",
            "id  + id * id  ",
    )

    def test_leftmost(self):
        """ParseTree: check leftmost() against known result"""
        t_leftmost = tuple(self.sample_tree.leftmost())
        self.assertEqual(self.sample_leftmost, t_leftmost)

    sample_rightmost = (
            "E",
            "T E'",
            "T + T E'",
            "T + T ",
            "T + F T' ",
            "T + F * F T' ",
            "T + F * F  ",
            "T + F * id  ",
            "T + id * id  ",
            "F T' + id * id  ",
            "F  + id * id  ",
            "id  + id * id  ",
    )

    def test_rightmost(self):
        """ParseTree: check rightmost() against known result"""
        t_rightmost = tuple(self.sample_tree.rightmost())
        self.assertEqual(self.sample_rightmost, t_rightmost)

    sample_unparse = "id + id * id"

    def test_unparse(self):
        """ParseTree: check unparse against known result"""
        t_unparse = self.sample_tree.unparse()
        self.assertEqual(self.sample_unparse, t_unparse)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
