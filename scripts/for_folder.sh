#!/bin/bash
for d in */ ; do
    [ -L "${d%/}" ] && continue
    echo "$d"
    cd "$d"
    touch main.tex
    cd ..
done
