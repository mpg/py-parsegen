#!/usr/bin/python3
# coding: utf-8

from itertools import chain


# helper for use in printing derivations
def _sym(tree):
    return tree.symbol

# helper for selecting side in derivations
def _norev(it):
    return it

class ParseTree:
    """Simple tree structure to use as output by the parsers"""
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children if children else []

    def lines(self, prefix=""):
        """Iterator of lines of a representation of the tree"""
        sym = self.symbol if self.symbol else "ε"
        yield prefix + sym
        for child in self.children:
            yield from child.lines(prefix + "| ")

    def __str__(self):
        """String representation"""
        return "\n".join(self.lines())

    def _derive(self, rev):
        """Iterator of steps in a left- or rightmost derivation"""
        yield self.symbol

        # iterative DFS with explicit stack
        todo = [self]  # nodes to be visited (stack: next on top)
        done = []  # terminals produced so far (most recent on top)
        beg, end = tuple(rev((todo, done))) # for display
        while todo:
            cur = todo.pop()
            if cur.children:
                for c in rev(cur.children):
                    todo.append(c)

                yield ' '.join(map(_sym, chain(beg, reversed(end))))
            else:
                done.append(cur)

    def leftmost(self):
        """Iterator of steps in a leftmost derivation"""
        yield from self._derive(reversed)

    def rightmost(self):
        """Iterator of steps in a rightmost derivation"""
        yield from self._derive(_norev)


if __name__ == "__main__":  # pragma: no cover
    PT = ParseTree
    most_inner = PT("S", [PT("")])
    inner_tree = PT("S", [PT("("), most_inner, PT(")")])
    final_tree = PT("S", [PT("("), inner_tree, PT(")")])

    print(final_tree)
    print()

    print(" -> ".join(final_tree.leftmost()))
    print()
