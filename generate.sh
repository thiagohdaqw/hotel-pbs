#!/bin/bash

# Usage:
#       bash generate.sh <file>
#
# Example:
#       bash generate.sh sample/root.desc


FILE="${1:-samples/root.desc}"
OUTPUT_FILE="formulae/$(basename $FILE | sed s/\\.desc$//)"
RESULT_FILE="result/$(basename $OUTPUT_FILE)"

echo "Generating formulae for $FILE...";

python3 hotel/main.py $FILE  > $OUTPUT_FILE.clasp 2> $RESULT_FILE.symbols;
clasp $OUTPUT_FILE.clasp > $RESULT_FILE.clasp;
python3 hotel/clasp_translate.py $RESULT_FILE > $RESULT_FILE.vars;

cat $RESULT_FILE.vars
