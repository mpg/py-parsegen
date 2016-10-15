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

    # [TRDB] example 4.34 p. 222
    start = (-1, 0)
    start_closure = {
            (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
    }

    def test_closure(self):
        """SLR: check closure() against known value"""
        slr = SLR(Grammar(self.gram))
        t_closure = slr.closure({self.start})
        self.assertEqual(self.start_closure, t_closure)

    # [TRDB] example 4.35 p. 224
    goto_items = {(-1, 1), (0, 1)}
    goto_symbol = '+'
    goto_result = {(0, 2), (2, 0), (3, 0), (4, 0), (5, 0)}

    def test_goto(self):
        """SLR: check goto() against know value"""
        slr = SLR(Grammar(self.gram))
        t_result = slr.goto(self.goto_items, self.goto_symbol)
        self.assertEqual(self.goto_result, t_result)

    ccol = (
            ((-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)),
            ((-1, 1), (0, 1)),
            ((1, 1), (2, 1)),
            ((3, 1),),
            ((4, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)),
            ((5, 1),),
            ((0, 2), (2, 0), (3, 0), (4, 0), (5, 0)),
            ((2, 2), (4, 0), (5, 0)),
            ((4, 2), (0, 1)),
            ((0, 3), (2, 1)),
            ((2, 3),),
            ((4, 3),),
    )

    def test_ccol(self):
        """SLR: check ccol against known value (set by __init__)"""
        slr = SLR(Grammar(self.gram))
        self.assertEqual(self.ccol, slr.ccol)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
