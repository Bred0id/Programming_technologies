#!/bin/bash

INPUT="$1"
L_PATH="$2"
U_PATH="$3"
PRECISION="$4"

declare -A A
n=0

while IFS= read -r line || [[ -n "$line" ]]; do
    IFS=',' read -ra args <<< "$line"
    cols=${#args[@]}

    for ((j=0; j<cols; j++)); do
        A[$n,$j]="${args[j]}"
    done

    ((n++))
done < "$INPUT"

declare -A L U
scale=20

for ((i=0; i<n; i++)); do
    for ((j=i; j<n; j++)); do
        sum="0"

        for ((k=0; k<i; k++)); do
            l_val="${L[$i,$k]}"
            u_val="${U[$k,$j]}"
            sum="$sum + $l_val * $u_val"
        done

        a_val="${A[$i,$j]}"
        u_val=$(echo "scale=$scale; $a_val - ($sum)" | bc)
        U[$i,$j]="$u_val"
    done

    L[$i,$i]="1"

    for ((j=i+1; j<n; j++)); do
        sum="0"

        for ((k=0; k<i; k++)); do
            l_val="${L[$j,$k]}"
            u_val="${U[$k,$i]}"
            sum="$sum + $l_val * $u_val"
        done

        a_val="${A[$j,$i]}"
        u_ii="${U[$i,$i]}"
        l_val=$(echo "scale=$scale; ($a_val - ($sum)) / $u_ii" | bc)
        L[$j,$i]="$l_val"
    done
done

write_matrix() {
    local -n mat=$1
    local file=$2
    local prec=$3

    > "$file"

    for ((i=0; i<n; i++)); do
        line=""

        for ((j=0; j<n; j++)); do
            val=$(LC_NUMERIC=C printf "%.${prec}f" "${mat[$i,$j]}")
            if [ $j -eq 0 ]; then
                line="$val"
            else
                line="$line,$val"
            fi
        done

        echo "$line" >> "$file"
    done
}

write_matrix L "$L_PATH" "$PRECISION"
write_matrix U "$U_PATH" "$PRECISION"
