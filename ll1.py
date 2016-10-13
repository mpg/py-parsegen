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
                    self.table[lhs, t] = i
                first.remove('')

            for t in first:
                self.table[lhs, t] = i
