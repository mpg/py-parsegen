#!/usr/bin/python3
# coding: utf-8


class SLR:
    """SLR(1) parser"""

    AUG_PROD = -1  # Added production S' -> S in the augmented grammar

    def __init__(self, grammar):
        """Generate SLR(1) parser corresponding to a Grammar object"""
        self.g = grammar

    def items(self):
        """Iterator for LR(0) items of the augmented grammar
        An item is a pair (production number, cursor position)"""
        yield (self.AUG_PROD, 0)
        yield (self.AUG_PROD, 1)
        for i, prod in enumerate(self.g.productions):
            lhs, rhs = prod
            for cursor in range(len(rhs) + 1):
                yield (i, cursor)
