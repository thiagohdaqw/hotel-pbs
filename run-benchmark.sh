#!/bin/bash

SAMPLES="$(ls ./samples)";

export DEBUG=0

>&2 echo "[$(date)] *************************************************"
for s in $SAMPLES; do
    >&2 echo -e "$s ================================================"
    time python3 -m hotel "./samples/$s" > "./result/$s";
    >&2 echo
done
