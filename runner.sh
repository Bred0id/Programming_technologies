#!/bin/bash

cd server

./service-init.sh
trap "./service-shutdown.sh" EXIT

sum=0

for color in "$@"; do
    echo "$color" > in.fifo
    now=$(cat out.fifo)
    sum=$((sum + now))
done

echo "$sum"
