#!/usr/bin/python3
# coding: utf-8

from grammar import Grammar
import unittest
import collections


RefBasic = collections.namedtuple("RefBasic",
                                  ["rules", "nbprods", "start",
                                   "nonterms", "terms", "symbs"])


class KnownValues(unittest.TestCase):
    known_basics = [
            RefBasic(
                rules=("S -> A | b |", "A -> A a | a"),
                nbprods=5,
                start="S",
                nonterms={"S", "A"},
                terms={"a", "b"},
                symbs={"S", "A", "a", "b"},
                ),
            RefBasic(
                rules=(
                    "S -> A ( S ) B |",
                    "A -> S | S B | ex |",
                    "B -> S B | why"),
                nbprods=8,
                start="S",
                nonterms={"S", "A", "B"},
                terms={"ex", "why", "(", ")"},
                symbs={"S", "A", "B", "ex", "why", "(", ")"},
                ),
            ]

    def test_basic_params(self):
        """Creating the grammar should set basic parameters"""
        for basics in self.known_basics:
            g = Grammar(basics.rules)
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
                    "B": {"x", "y", "("},
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
            (
                (
                    "R -> a R' | ( R ) R'",
                    "R' -> | X R'",
                    "X -> . R | + R | *",
                ),
                {
                    "(": {"("},
                    ")": {")"},
                    "+": {"+"},
                    "*": {"*"},
                    ".": {"."},
                    "a": {"a"},
                    "R": {"a", "("},
                    "R'": {"", ".", "+", "*"},
                    "X": {".", "+", "*"},
                }
            )
        ]

    def test_first(self):
        """Creating the grammar should compute First sets"""
        for rules, first in self.known_firsts:
            g = Grammar(rules)
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
                    "E": {")", Grammar.END},
                    "E'": {")", Grammar.END},
                    "T": {"+", ")", Grammar.END},
                    "T'": {"+", ")", Grammar.END},
                    "F": {"*", "+", ")", Grammar.END},
                },
            ),
            (
                (
                    "R -> a R' | ( R ) R'",
                    "R' -> | X R'",
                    "X -> . R | + R | *",
                ),
                {
                    "R": {Grammar.END, ")", ".", "+", "*"},
                    "R'": {Grammar.END, ")", ".", "+", "*"},
                    "X": {Grammar.END, ")", ".", "+", "*"},
                }
            )
        ]

    def test_follow(self):
        """Creating the grammar should compute Follow sets"""
        for rules, follow in self.known_follows:
            g = Grammar(rules)
            self.assertEqual(follow.keys(), g.follow.keys())
            for s in follow:
                self.assertEqual(follow[s], g.follow[s])

    pprod = (
            ("S -> A | b |", "A -> A a | a"),
            ("S -> A", "S -> b", "S -> ", "A -> A a", "A -> a"),
            )

    def test_pprod(self):
        """Pretty-printing productions"""
        rules, pprods = self.pprod
        g = Grammar(rules)
        g_pprods = tuple(g.pprod(i) for i in range(len(g.productions)))
        self.assertEqual(pprods, g_pprods)

if __name__ == "__main__":
    unittest.main()
