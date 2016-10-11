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
                    "A -> S | S B | ex |",
                    "B -> S B | why"),
                nbprods = 8,
                start = "S",
                nonterms = {"S", "A", "B"},
                terms = {"ex", "why", "(", ")"},
                symbs = {"S", "A", "B", "ex", "why", "(", ")"},
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

    known_firsts = [
            (
                (
                    "S -> A ( S ) B |",
                    "A -> S | S B | x |",
                    "B -> S B | y",
                ),
                {
                    "x": {"x"},
                    "y": {"y"},
                    "(": {"("},
                    ")": {")"},
                    "S": {"", "x", "y", "("},
                    "A": {"", "x", "y", "("},
                    "B": {"", "x", "y", "("},
                },
            ),
            (
                (
                    "E -> T E'",
                    "E' -> + T E' |",
                    "T -> F T'",
                    "T' -> * F T' |",
                    "F -> ( E ) | id",
                ),
                {
                    "(": {"("},
                    ")": {")"},
                    "+": {"+"},
                    "*": {"*"},
                    "id": {"id"},
                    "E": {"(", "id"},
                    "T": {"(", "id"},
                    "F": {"(", "id"},
                    "E'": {"+", ""},
                    "T'": {"*", ""},
                },
            ),
        ]

    def test_first(self):
        """Creating the grammar should compute First sets"""
        for rules, first in self.known_firsts:
            g = gram.Grammar(rules)
            self.assertEqual(first.keys(), g.first.keys())
            for s in first:
                self.assertEqual(first[s], g.first[s])

    known_follows = [
            (
                (
                    "E -> T E'",
                    "E' -> + T E' |",
                    "T -> F T'",
                    "T' -> * F T' |",
                    "F -> ( E ) | id",
                ),
                {
                    "E": {")", gram.Grammar.END},
                    "E'": {")", gram.Grammar.END},
                    "T": {"+", ")", gram.Grammar.END},
                    "T'": {"+", ")", gram.Grammar.END},
                    "F": {"*", "+", ")", gram.Grammar.END},
                },
            ),
        ]

    def test_follow(self):
        """Creating the grammar should compute Follow sets"""
        for rules, follow in self.known_follows:
            g = gram.Grammar(rules)
            self.assertEqual(follow.keys(), g.follow.keys())
            for s in follow:
                self.assertEqual(follow[s], g.follow[s])


if __name__ == "__main__":
    unittest.main()
