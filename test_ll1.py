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
        """LL1: Check table against known value"""
        parser = LL1(Grammar(self.gram))
        self.assertEqual(parser.table, self.table)

    bad_grams = (
            ("S -> S a | a",),  # left-recursive
            ("S -> a S | a",),  # non left-factored
            ("S -> A | B", "A -> x", "B -> x"),  # ambigous
    )

    def test_bad_grammars(self):
        """LL1: init should raise when fed a non-LL(1) grammar"""
        for g in self.bad_grams:
            with self.assertRaises(LL1.GrammarNotLL1):
                LL1(Grammar(g))

    simple_grammar = ("S -> a b",)
    bad_sentences = ("a", "a b c", "b")

    def test_bad_sentences(self):
        """LL1: parse() should raise on invalid sentences"""
        ll1 = LL1(Grammar(self.simple_grammar))
        for bs in self.bad_sentences:
            with self.assertRaises(LL1.NotInLanguage):
                ll1.parse(bs.split())

    # for self.gram
    good_sentences = (
            "id",
            "id + id",
            "id + id + id",
            "id + id * id",
            "( id + id ) * id",
    )

    def test_good_sentences(self):
        """LL1: parse() should accept valid sentences"""
        ll1 = LL1(Grammar(self.gram))
        for s in self.good_sentences:
            ll1.parse(s.split())

    ref_parse = (
            ("E -> id T | ( E ) T", "T -> + id | * id",),
            "( id + id ) * id",
            (
                "E",
                "( E ) T",
                "( id T ) T",
                "( id + id ) T",
                "( id + id ) * id",
            )
    )

    def test_parse(self):
        """LL1: check parse() against know result"""
        gram, sentence, ref_leftmost = self.ref_parse
        ll1 = LL1(Grammar(gram))
        tree = ll1.parse(sentence.split())
        t_leftmost = tuple(tree.leftmost())
        self.assertEqual(t_leftmost, ref_leftmost)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
