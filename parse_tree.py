#!/usr/bin/python3
# coding: utf-8

from itertools import chain


# helper for use in printing derivations
def _sym(tree):
    return tree.symbol


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

    def leftmost(self):
        """Iterator of steps in a leftmost derivation"""
        yield self.symbol

        # iterative DFS with explicit stack
        done = []  # terminals produced so far (leaves visited)
        todo = [self]  # nodes to be visited (reversed order)
        while todo:
            cur = todo.pop()
            if cur.children:
                for c in reversed(cur.children):
                    todo.append(c)

                yield ' '.join(map(_sym, chain(done, reversed(todo))))
            else:
                done.append(cur)

    def rightmost(self):
        """Iterator of steps in a rightmost derivation"""
        yield self.symbol

        # iterative DFS with explicit stack
        done = []  # terminals produced so far (leaves visited)
        todo = [self]  # nodes to be visited (reversed order)
        while todo:
            cur = todo.pop()
            if cur.children:
                for c in cur.children:
                    todo.append(c)

                yield ' '.join(map(_sym, chain(todo, reversed(done))))
            else:
                done.append(cur)

if __name__ == "__main__":  # pragma: no cover
    PT = ParseTree
    most_inner = PT("S", [PT("")])
    inner_tree = PT("S", [PT("("), most_inner, PT(")")])
    final_tree = PT("S", [PT("("), inner_tree, PT(")")])

    print(final_tree)
    print()

    print(" -> ".join(final_tree.leftmost()))
    print()
