#!/bin/sh

# very quick sanity check for the script parts

# eg, set to 'python -m coverage run -a' for coverage
: ${PYTHON:=python}

die() {
    echo "FAILED at line $1" >&2
    exit 1
}

exec >/dev/null

$PYTHON grammar.py examples/simple || die $LINENO
$PYTHON grammar.py < examples/simple || die $LINENO

$PYTHON parse_tree.py || die $LINENO

$PYTHON ll1.py 2>/dev/null && die $LINENO
$PYTHON ll1.py examples/g2 2>/dev/null && die $LINENO
$PYTHON ll1.py examples/a-star || die $LINENO
$PYTHON ll1.py examples/g1 || die $LINENO
$PYTHON ll1.py examples/g1 "id + id" || die $LINENO
$PYTHON ll1.py examples/g1 "id + id + id" 2>/dev/null && die $LINENO

$PYTHON slr.py 2>/dev/null && die $LINENO
$PYTHON slr.py examples/ex-4.34 || die $LINENO
$PYTHON slr.py examples/ambiguous 2>/dev/null && die $LINENO
$PYTHON slr.py examples/ex-4.34 "id + id * id" || die $LINENO
$PYTHON slr.py examples/ex-4.34 "oops" 2>/dev/null && die $LINENO

echo PASSED >&2
