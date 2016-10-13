#!/usr/bin/python3
# coding: utf-8

from ll1 import LL1
from grammar import Grammar
import unittest


class KnownValues(unittest.TestCase):
    # this is grammar (4.11) p. 176 of [TRDB],
    # whose LL(1) table is Fig. 4.15 p. 188
    gram = (
            "E -> T E'",        # 0
            "E' -> + T E' |",   # 1, 2
            "T -> F T'",        # 3
            "T' -> * F T' |",   # 4, 5
            "F -> ( E ) | id",  # 6, 7
    )

    table = {
            ("E", 'id'): 0,
            ("E", '('): 0,
            ("E'", '+'): 1,
            ("E'", ')'): 2,
            ("E'", Grammar.END): 2,
            ("T", 'id'): 3,
            ("T", '('): 3,
            ("T'", '+'): 5,
            ("T'", '*'): 4,
            ("T'", ')'): 5,
            ("T'", Grammar.END): 5,
            ("F", 'id'): 7,
            ("F", '('): 6,
    }

    def test_table(self):
        """Check LL1 table against known value"""
        parser = LL1(Grammar(self.gram))
        self.assertEqual(parser.table, self.table)


if __name__ == '__main__':  # pragma: no branch
    unittest.main()
