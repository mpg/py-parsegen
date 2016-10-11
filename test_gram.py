#!/usr/bin/python3
# coding: utf-8

import gram
import unittest
import collections


RefBasic = collections.namedtuple("RefBasic",
        ["rules", "nbprods", "start", "nonterms", "terms", "symbs"])

class KnownValues(unittest.TestCase):
    known_basics = [
            RefBasic(
                rules = ("S -> A | b |", "A -> A a | a"),
                nbprods = 5,
                start = "S",
                nonterms = {"S", "A"},
                terms = {"a", "b"},
                symbs = {"S", "A", "a", "b"},
                ),
            RefBasic(
                rules = (
                    "S -> A ( S ) B |",
                    "A -> S | S B | x |",
                    "B -> S B | y"),
                nbprods = 8,
                start = "S",
                nonterms = {"S", "A", "B"},
                terms = {"x", "y", "(", ")"},
                symbs = {"S", "A", "B", "x", "y", "(", ")"},
                ),
            ]

    def test_basic_params(self):
        """Creating the grammar should set basic parameters"""
        for basics in self.known_basics:
            g = gram.Grammar(basics.rules)
            self.assertEqual(basics.nbprods, len(g.productions))
            self.assertEqual(basics.start, g.start_symbol)
            self.assertEqual(basics.nonterms, g.non_terminals)
            self.assertEqual(basics.terms, g.terminals)
            self.assertEqual(basics.symbs, g.symbols)


if __name__ == "__main__":
    unittest.main()
