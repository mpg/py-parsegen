#!/usr/bin/python3
# coding: utf-8

import fileinput
from pprint import pprint

# end marker disting from any symbol
END = -1
# a set containing just the empty string
EPS = frozenset("")

# Read grammar with the following on each line:
#   non_term -> prod_1 | prod_2 | ... | prod_n
# and prod_i is any sequence of space-separated symbols
productions = []
for line in fileinput.input():
    (lhs, rhs) = line.split("->")
    for actual_rhs in rhs.split("|"):
        productions.append((lhs.strip(), tuple(actual_rhs.split())))

print("Productions:")
pprint(productions)
print()

# infer useful info about the grammar
start_symbol = productions[0][0]
non_terminals = frozenset(prod[0] for prod in productions)
rhs_symbols = frozenset(s for prod in productions for s in prod[1])
terminals = rhs_symbols - non_terminals
symbols = rhs_symbols | non_terminals

# compute First sets

def stable_update(cur, new):
    "Update cur with new elements and return whether it's unchanged"""
    if cur >= new:
        return True

    cur |= new
    return False

def first_of(sentence):
    result = set()
    elements = list(reversed(sentence))

    while elements:
        s = elements.pop()
        result |= first[s] - EPS
        if "" not in first[s]:
            return result

    result.add("");
    return result

first = {s: frozenset(s) if s in terminals else set() for s in symbols}

done = False
while not done:
    done = True
    for lhs, rhs in productions:
        done &= stable_update(first[lhs], first_of(rhs))

print("First sets:")
pprint(first)
print()

# compute follow sets

def follow_fragment(lhs, symbol, after):
    result = first_of(after)

    if "" in result:
        result -= EPS
        result |= follow[lhs]

    return result


follow = {n: {END} if n == start_symbol else set() for n in non_terminals}

done = False
while not done:
    done = True
    for lhs, rhs in productions:
        for i in range(len(rhs)):
            if rhs[i] in non_terminals:
                new = follow_fragment(lhs, rhs[i], rhs[i+1:])
                done &= stable_update(follow[rhs[i]], new)

print("Follow sets:")
pprint(follow)
print()
