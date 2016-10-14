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

    class GrammarNotLL1(ValueError):
        pass

    def _table_add(self, lhs, term, prod_idx):
        if (lhs, term) in self.table:
            msg = "Conflict for ({}, {}): '{}' vs '{}'".format(
                    lhs, term,
                    self.g.pprod(prod_idx),
                    self.g.pprod(self.table[lhs, term]))
            raise self.GrammarNotLL1(msg)
        self.table[lhs, term] = prod_idx

    class NotInLanguage(ValueError):
        pass

    def parse(self, sentence):
        """Read a sentence (iterable of terminals), and:
        - if it's in the language, do nothing (for now),
        - otherwise, raise NotInLanguage
        [TRDB] Algorithm 4.3 p. 187
        """

        stack = [self.g.END, self.g.start_symbol]
        tok_stream = iter(sentence)
        token = next(tok_stream, self.g.END)

        while stack:
            state = stack.pop()
            if state in self.g.non_terminals:
                if (state, token) not in self.table:
                    msg = "In state '{}', got '{}'".format(state, token)
                    raise self.NotInLanguage(msg)

                prod_idx = self.table[state, token]
                rhs = self.g.productions[prod_idx][1]
                stack.extend(list(reversed(rhs)))
            else:
                if token != state:
                    msg = "Expected '{}', got '{}'".format(state, token)
                    raise self.NotInLanguage(msg)

                token = next(tok_stream, self.g.END)


if __name__ == "__main__":  # pragma: no cover
    from grammar import Grammar
    import sys

    if len(sys.argv) not in (2, 3):
        sys.stderr.write("Usage: ll1.py grammar_file [string_to_parse]\n")
        sys.exit(1)

    with open(sys.argv[1]) as gram_in:
        try:
            ll1 = LL1(Grammar(gram_in))
        except LL1.GrammarNotLL1 as err:
            sys.stderr.write("Grammar is not LL1:\n{}\n".format(err))
            sys.exit(1)

    if len(sys.argv) == 2:
        print("LL(1) parsing table:")
        for lhs, term in ll1.table:
            prod = ll1.g.pprod(ll1.table[lhs, term])
            print("{}\t{}\t{}".format(lhs, term, prod))
        sys.exit(0)

    sentence = sys.argv[2]
    try:
        ll1.parse(sentence.split())
    except LL1.NotInLanguage as err:
        sys.stderr.write("Sentence not in language:\n{}\n".format(err))
        sys.exit(1)

    print("Sentence accepted")
