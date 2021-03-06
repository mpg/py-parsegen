#!/usr/bin/python3
# coding: utf-8


class Grammar:
    """A grammar and associated tools"""

    END = -1  # end marker, guaranteed distinct from actual symbols

    def __init__(self, rules):
        """
        Read grammar from an iterable containing strings like:
            non_term -> prod_1 | prod_2 | ... | prod_n
        and prod_i is a (possibly empty) space-separated list of symbols;
        ii n == 1, then prod_1 must not be empty;
        a symbol is a non-empty sequence of non-whitespace characters;
        non_term must be a symbol too.

        Sets of terminals and non-terminals are infered from the rules.
        The start symbol is taken as the lhs of the first production.
        """
        # store productions in a usable form
        self.productions = []
        for line in rules:
            (lhs, rhs) = line.split("->")
            for single_rhs in rhs.split("|"):
                rhs_elements = tuple(single_rhs.split())
                self.productions.append((lhs.strip(), rhs_elements))

        # infer remaining elements of the grammar
        self.start_symbol = self.productions[0][0]
        self.non_terminals = frozenset(prod[0] for prod in self.productions)
        rhs_symbols = frozenset(s for p in self.productions for s in p[1])
        self.terminals = rhs_symbols - self.non_terminals
        self.symbols = self.terminals | self.non_terminals

        # pre-compute First and Follow sets (always useful)
        self._init_first()
        self._init_follow()

    def first_of(self, sequence):
        """Compute the First set of a sequence of symbols
        [TRDB] Sec 4.4 (p. 189)"""
        result = set()

        for s in sequence:
            result |= self.first[s] - {""}
            if "" not in self.first[s]:
                return result

        result.add("")
        return result

    # helper for iteratively computing sets and tracking when we're done
    @staticmethod
    def _stable_update(cur, new):
        "Update cur with new elements and return whether it's unchanged"""
        if cur >= new:
            return True

        cur |= new
        return False

    def _init_first(self):
        """Compute the First set of each symbol
        [TRDB] Sec 4.4 (p. 189)"""
        self.first = {s: frozenset((s,)) if s in self.terminals else set()
                      for s in self.symbols}

        done = False
        while not done:
            done = True
            for lhs, rhs in self.productions:
                new = self.first_of(rhs)
                done &= self._stable_update(self.first[lhs], new)

    def _follow_for(self, lhs, symbol, after):
        """Partial Follow set for an occurence of symbol in a production.
        [TRDB] Sec 4.4 (p. 189)"""
        result = self.first_of(after)

        if "" in result:
            result.remove("")
            result |= self.follow[lhs]

        return result

    def _init_follow(self):
        """Compute the Follow set of each non-terminal"""
        self.follow = {n: {self.END} if n == self.start_symbol else set()
                       for n in self.non_terminals}

        done = False
        while not done:
            done = True
            for lhs, rhs in self.productions:
                for i in range(len(rhs)):
                    if rhs[i] in self.non_terminals:
                        new = self._follow_for(lhs, rhs[i], rhs[i+1:])
                        done &= self._stable_update(self.follow[rhs[i]], new)

    def pprod(self, i):
        """Pretty representation of production number i"""
        lhs, rhs = self.productions[i]
        return "{} -> {}".format(lhs, " ".join(rhs))


if __name__ == "__main__":  # pragma: no cover
    import fileinput
    from pprint import pprint

    gram = Grammar(fileinput.input())

    print("Productions:")
    pprint(gram.productions)
    print()

    print("First sets:")
    pprint(gram.first)
    print()

    print("Follow sets:")
    pprint(gram.follow)
    print()
