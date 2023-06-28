#!/bin/bash

SAMPLES_FOLDER="${1:-samples}"
SAMPLES="$(ls ./$SAMPLES_FOLDER)";

export DEBUG=0

>&2 echo "[$(date)]: $SAMPLES_FOLDER *************************************************"
for s in $SAMPLES; do
    >&2 echo -e "$s ================================================"
    timeout 600s time python3 -m hotel "$SAMPLES_FOLDER/$s" > "./result/$s";
    if [[ "$?" != "0" ]]; then
        >&2 echo "TLE";
    fi;
    >&2 echo
done
