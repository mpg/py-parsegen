#!/usr/bin/python3
# coding: utf-8


class ParseTree:
    """Simple tree structure to use as parsing output"""
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
