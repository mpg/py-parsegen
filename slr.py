#!/usr/bin/python3
# coding: utf-8

from itertools import chain


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

    def str_item(self, item):
        """Human-friendly formatting of an item"""
        prod_nb, cursor = item

        if prod_nb == self.AUG_PROD:
            lhs, rhs = "|", self.g.start_symbol
        else:
            lhs, rhs = self.g.productions[prod_nb]

        out = chain((lhs, '->'), rhs[:cursor], ('|',), rhs[cursor:])
        return ' '.join(out)


if __name__ == "__main__":  # pragma: no cover
    from grammar import Grammar
    import sys

    if not 2 <= len(sys.argv) <= 2:
        usage = "Usage: slr.py grammar_file\n"
        sys.stderr.write(usage)
        sys.exit(1)

    with open(sys.argv[1]) as gram_in:
        slr = SLR(Grammar(gram_in))

    print("LR(0) items:")
    for it in slr.items():
        print(slr.str_item(it))
    print()
