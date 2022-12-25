#!/bin/sh
bibtex-tidy --curly --numeric --tab --align=13 --duplicates=key --no-escape --no-remove-dupe-fields ./ref.bib && pdflatex main
pdflatex main
bibtex main
pdflatex main
pdflatex main
open main.pdf
