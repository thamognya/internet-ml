#!/bin/sh

pdflatex main
bibtex main
pdflatex main
pdflatex main
open main.pdf