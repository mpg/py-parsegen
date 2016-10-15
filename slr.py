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

    def _get_prod(self, nb):
        """Get production by number in the augmented grammar"""
        if nb == self.AUG_PROD:
            return "|", self.g.start_symbol
        return self.g.productions[nb]

    def str_item(self, item):
        """Human-friendly formatting of an item"""
        prod_nb, cursor = item
        lhs, rhs = self._get_prod(prod_nb)
        out = chain((lhs, '->'), rhs[:cursor], ('|',), rhs[cursor:])
        return ' '.join(out)

    def _get_after_cursor(self, item):
        """Return the symbol after the cursor in item"""
        prod_nb, cursor = item
        lhs, rhs = self._get_prod(prod_nb)
        return rhs[cursor] if cursor < len(rhs) else ''

    def closure(self, items):
        """Return the closure of s set of items [TRDB] Fig 4.33 p. 223"""
        todo = set(items)
        done = set()

        while todo:
            it = todo.pop()
            after_cursor = self._get_after_cursor(it)
            if after_cursor in self.g.non_terminals:
                for i, prod in enumerate(self.g.productions):
                    if prod[0] == after_cursor:
                        new_it = (i, 0)
                        if new_it not in done:
                            todo.add(new_it)
            done.add(it)

        return done

    def goto(self, items, symbol):
        """Return the set of new items reachable from items after symbol
        [TRDB] Fig 4.34 p. 224"""
        new_items = set()

        for it in items:
            after_cursor = self._get_after_cursor(it)
            if after_cursor == symbol:
                prod_nb, cursor = it
                new_items.add((prod_nb, cursor + 1))

        return self.closure(new_items)


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
