#!/usr/bin/python3
# coding: utf-8


class LL1:
    """LL(1) parser"""
    def __init__(self, grammar):
        """Generate LL(1) parser corresponding to a Grammar object
        [TRDB] Algorithm 4.4 (p. 190)"""
        self.g = grammar
        self.table = {}
        for i, prod in enumerate(self.g.productions):
            lhs, rhs = prod
            first = self.g.first_of(rhs)

            if '' in first:
                for t in self.g.follow[lhs]:
                    self._table_add(lhs, t, i)
                first.remove('')

            for t in first:
                self._table_add(lhs, t, i)

    def _table_add(self, lhs, term, prod_idx):
        if (lhs, term) in self.table:
            msg = "Conflict for ({}, {}): '{}' vs '{}'".format(
                    lhs, term,
                    self.g.pprod(prod_idx),
                    self.g.pprod(self.table[lhs, term]))
            raise ValueError(msg)
        self.table[lhs, term] = prod_idx
