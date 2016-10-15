#!/usr/bin/python3
# coding: utf-8

from itertools import chain


class SLR:
    """SLR(1) parser"""

    AUG_PROD = -1  # Added production S' -> S in the augmented grammar

    # For the action table
    ACCEPT = 0
    SHIFT = 1
    REDUCE = 2
    STR_ACTION = ("A", "S", "R")

    def __init__(self, grammar):
        """Generate SLR(1) parser corresponding to a Grammar object"""
        self.g = grammar
        self._init_ccol()
        self._init_tables()

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

        return frozenset(done)

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

    def _init_ccol(self):
        """Compute the canonical collection of sets of LR(0) items
        [TRDB] Fig 4.34 p. 224"""
        todo = {self.closure({(self.AUG_PROD, 0)})}
        done = set()

        while todo:
            cur = todo.pop()
            for s in self.g.symbols:
                new = self.goto(cur, s)
                if new and new not in done:
                    todo.add(new)
            done.add(cur)

        # for testing convenience, sort in the same order as [TRDB]
        ccol = [tuple(sorted(s, key=lambda t: (-t[1], t[0]))) for s in done]
        self.ccol = tuple(sorted(ccol, key=lambda tt: (tt[0][1], tt[0][0])))

        # reverse index, to convert goto() result to a state number
        self.ccol_idx = {frozenset(t): i for i, t in enumerate(self.ccol)}

    class GrammarNotSLR(ValueError):
        pass

    def _set_action(self, state, symbol, action, info=0):
        if symbol == '':
            symbol = self.g.END

        if (state, symbol) in self.actions:
            prev_action = self.actions[state, symbol]
            msg = "Reduce" if prev_action == action else "Shift"
            msg += "/reduce conflict for ({}, {})".format(state, symbol)
            raise self.GrammarNotSLR(msg)

        self.actions[state, symbol] = (action, info)

    def _init_tables(self):
        """Compute parsing tables [TRDB] Alg 4.8 p. 227"""
        self.actions = {}
        self.gotos = {}

        for i, set_i in enumerate(self.ccol):
            for item in set_i:
                prod_nb = item[0]
                sym = self._get_after_cursor(item)

                if sym in self.g.terminals:
                    set_j = self.goto(set_i, sym)
                    j = self.ccol_idx[set_j]
                    self._set_action(i, sym, self.SHIFT, j)

                elif sym == '' and prod_nb != self.AUG_PROD:
                    lhs = self.g.productions[prod_nb][0]
                    for f in self.g.follow[lhs]:
                        self._set_action(i, f, self.REDUCE, prod_nb)

                elif sym == '' and prod_nb == self.AUG_PROD:
                    self._set_action(i, sym, self.ACCEPT)

                elif sym in self.g.non_terminals:
                    set_j = self.goto(set_i, sym)
                    j = self.ccol_idx[set_j]
                    self.gotos[i, sym] = j


if __name__ == "__main__":  # pragma: no cover
    from grammar import Grammar
    import sys

    if not 2 <= len(sys.argv) <= 2:
        usage = "Usage: slr.py grammar_file\n"
        sys.stderr.write(usage)
        sys.exit(1)

    with open(sys.argv[1]) as gram_in:
        slr = SLR(Grammar(gram_in))

    print("Canonical collection of LR(0) items:")
    for i, items in enumerate(slr.ccol):
        print(i)
        for it in items:
            print(slr.str_item(it))
        print()

    def key(tup):
        state, symbol = tup
        if symbol == slr.g.END:
            symbol = '$'
        return state, symbol

    print("Action table:")
    for state, symbol in sorted(slr.actions, key=key):
        action, info = slr.actions[state, symbol]
        str_action = slr.STR_ACTION[action]
        print("{}\t{}\t{}{}".format(state, symbol, str_action, info))
    print()

    print("Goto table:")
    for state, symbol in sorted(slr.gotos):
        print("{}\t{}\t{}".format(state, symbol, slr.gotos[state, symbol]))
    print()
