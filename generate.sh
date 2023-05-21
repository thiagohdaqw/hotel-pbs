#!/bin/bash

# Usage:
#       bash generate.sh <file>
#
# Example:
#       bash generate.sh sample/root.desc


FILE="${1:-sample/root.desc}"
OUTPUT_FILE="formulae/$(basename $FILE | sed s/\\.desc$//)"

echo "Generating formulae for $FILE...";

cat $FILE | python -m generator.py > $OUTPUT_FILE
