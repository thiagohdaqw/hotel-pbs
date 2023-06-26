#!/bin/bash

SAMPLES_FOLDER="${1:-samples}"
SAMPLES="$(ls ./$SAMPLES_FOLDER)";

export DEBUG=1

>&2 echo "[$(date)]: $SAMPLES_FOLDER *************************************************"
for s in $SAMPLES; do
    >&2 echo -e "$s ================================================"
    time python3 -m hotel "$SAMPLES_FOLDER/$s" > "./result/$s";
    >&2 echo
done
