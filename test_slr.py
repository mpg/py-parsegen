#!/usr/bin/python3
# coding: utf-8

import unittest
from slr import SLR
from grammar import Grammar


class KnownValues(unittest.TestCase):
    gram = ("E -> E + T | T", "T -> T * F | F", "F -> ( E ) | id")

    items = (
            (-1, 0), (-1, 1),
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 1),
            (2, 0), (2, 1), (2, 2), (2, 3),
            (3, 0), (3, 1),
            (4, 0), (4, 1), (4, 2), (4, 3),
            (5, 0), (5, 1),
    )

    def test_items(self):
        """SLR: check items() against know value"""
        slr = SLR(Grammar(self.gram))
        self.assertEqual(self.items, tuple(slr.items()))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
