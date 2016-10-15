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
        """SLR: check items() against known value"""
        slr = SLR(Grammar(self.gram))
        self.assertEqual(self.items, tuple(slr.items()))

    str_items = (
            "| -> | E", "| -> E |",
            "E -> | E + T", "E -> E | + T", "E -> E + | T", "E -> E + T |",
            "E -> | T", "E -> T |",
            "T -> | T * F", "T -> T | * F", "T -> T * | F", "T -> T * F |",
            "T -> | F", "T -> F |",
            "F -> | ( E )", "F -> ( | E )", "F -> ( E | )", "F -> ( E ) |",
            "F -> | id", "F -> id |",
    )

    def test_str_items(self):
        """SLR: check str_item() against known value"""
        slr = SLR(Grammar(self.gram))
        t_str_items = tuple(slr.str_item(it) for it in slr.items())
        self.assertEqual(self.str_items, t_str_items)

    start = (-1, 0)
    start_closure = {
            (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
    }

    def test_closure(self):
        """SLR: check closure() against known value"""
        slr = SLR(Grammar(self.gram))
        t_closure = slr.closure({self.start})
        self.assertEqual(self.start_closure, t_closure)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
