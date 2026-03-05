#!/bin/bash

LIMIT=10
ORDER="up"
DIR=""

correct_date() {
    local day month year max
    IFS=':' read -r day month year <<< "$1"
    day=$((10#$day))
    month=$((10#$month))
    year=$((10#$year))
    case $month in
        1|3|5|7|8|10|12)
            max=31 ;;
        4|6|9|11)
            max=30 ;;
        2)
            if (( (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0) )); then
                max=29
            else
                max=28
            fi
            ;;
        *)
            return 1 ;;
    esac
    if [ "$day" -lt 1 ] || [ "$day" -gt "$max" ]; then
        return 1
    fi
    return 0
}

while [ $# -gt 0 ]; do
    if [ "$1" = "-l" ] || [ "$1" = "--lines" ]; then
        LIMIT="$2"
        shift 2
    elif [ "$1" = "-o" ] || [ "$1" = "--order" ]; then
        ORDER="$2"
        shift 2
    else
        DIR="$1"
        shift
    fi
done

tmpfile=$(mktemp)
trap "rm -f $tmpfile" EXIT

regularka='^\[ (INFO|DEBUG|WARNING|ERROR) \][[:space:]][0-9]{2}:[0-9]{2}:[0-9]{4}[[:space:]](0|[1-9][0-9]*)([[:space:]][a-zA-Z_]+)?$'

grep -rhE --include="*.log" "$regularka" "$DIR" > "$tmpfile"

if [ -s "$tmpfile" ]; then
    if [ "$ORDER" = "up" ]; then
        sort -k5,5 -nr "$tmpfile" | head -n "$LIMIT"
    else
        sort -k5,5 -nr "$tmpfile" | tail -n "$LIMIT"
    fi
fi