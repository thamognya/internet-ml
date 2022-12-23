#!/bin/bash
for d in */ ; do
    [ -L "${d%/}" ] && continue
    echo "$d"
    cd "$d"
    touch __init__.py
    cd ..
done
