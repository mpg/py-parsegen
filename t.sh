#!/bin/sh

set -e

nosetests --with-coverage --cover-package=. --cover-branches -v
sh test_scripts.sh

pep8 *.py
pyflakes *.py
