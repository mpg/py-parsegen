#!/usr/bin/python3
# coding: utf-8

import unittest
from slr import SLR
from grammar import Grammar


A, S, R = SLR.ACCEPT, SLR.SHIFT, SLR.REDUCE
AP = SLR.AUG_PROD
END = Grammar.END


class KnownValues(unittest.TestCase):
    gram = ("E -> E + T | T", "T -> T * F | F", "F -> ( E ) | id")

    items = (
            (AP, 0), (AP, 1),
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
    start = (AP, 0)
    start_closure = {
            (AP, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
    }

    def test_closure(self):
        """SLR: check closure() against known value"""
        slr = SLR(Grammar(self.gram))
        t_closure = slr.closure({self.start})
        self.assertEqual(self.start_closure, t_closure)

    # [TRDB] example 4.35 p. 224
    goto_items = {(AP, 1), (0, 1)}
    goto_symbol = '+'
    goto_result = {(0, 2), (2, 0), (3, 0), (4, 0), (5, 0)}

    def test_goto(self):
        """SLR: check goto() against know value"""
        slr = SLR(Grammar(self.gram))
        t_result = slr.goto(self.goto_items, self.goto_symbol)
        self.assertEqual(self.goto_result, t_result)

    ccol = (
            ((AP, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)),
            ((AP, 1), (0, 1)),
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

    # [TRDB] Fig. 4.31 p. 219
    # /!\ for reduce, production numbers are shifted by 1
    actions = {
            (0, 'id'): (S, 5), (0, '('): (S, 4),
            (1, '+'): (S, 6), (1, END): (A, 0),
            (2, '+'): (R, 1), (2, '*'): (S, 7),
            (2, ')'): (R, 1), (2, END): (R, 1),
            (3, '+'): (R, 3), (3, '*'): (R, 3),
            (3, ')'): (R, 3), (3, END): (R, 3),
            (4, 'id'): (S, 5), (4, '('): (S, 4),
            (5, '+'): (R, 5), (5, '*'): (R, 5),
            (5, ')'): (R, 5), (5, END): (R, 5),
            (6, 'id'): (S, 5), (7, '('): (S, 4),
            (7, 'id'): (S, 5), (6, '('): (S, 4),
            (8, '+'): (S, 6), (8, ')'): (S, 11),
            (9, '+'): (R, 0), (9, '*'): (S, 7),
            (9, ')'): (R, 0), (9, END): (R, 0),
            (10, '+'): (R, 2), (10, '*'): (R, 2),
            (10, ')'): (R, 2), (10, END): (R, 2),
            (11, '+'): (R, 4), (11, '*'): (R, 4),
            (11, ')'): (R, 4), (11, END): (R, 4),
    }

    gotos = {
            (0, 'E'): 1, (0, 'T'): 2, (0, 'F'): 3,
            (4, 'E'): 8, (4, 'T'): 2, (4, 'F'): 3,
            (6, 'T'): 9, (6, 'F'): 3,
            (7, 'F'): 10,
    }

    def test_tables(self):
        """SLR: check parsing tables against know value (set by __init__)"""
        slr = SLR(Grammar(self.gram))
        self.assertEqual(self.actions, slr.actions)
        self.assertEqual(self.gotos, slr.gotos)

    bad_sentences = ("+ id", "id +", "id + + id")

    def test_bad_sentences(self):
        """SLR: parse() should raise on invalid sentences"""
        slr = SLR(Grammar(self.gram))
        for bs in self.bad_sentences:
            with self.assertRaises(SLR.NotInLanguage):
                slr.parse(bs.split())

    good_sentences = (
            "id",
            "id + id",
            "id + id + id",
            "id + id * id",
            "( id + id ) * id",
    )

    def test_good_sentences(self):
        """SLR: parse() should accept valid sentences"""
        slr = SLR(Grammar(self.gram))
        for s in self.good_sentences:
            slr.parse(s.split())

    sentence = "id + id * id"
    rightmost = (
            "E",
            "E + T",
            "E + T * F",
            "E + T * id",
            "E + F * id",
            "E + id * id",
            "T + id * id",
            "F + id * id",
            "id + id * id",
    )

    def test_parse(self):
        """SLR: check parse() against known result"""
        slr = SLR(Grammar(self.gram))
        tree = slr.parse(self.sentence.split())
        t_rightmost = tuple(tree.rightmost())
        self.assertEqual(t_rightmost, self.rightmost)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
