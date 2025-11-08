#!/bin/bash
#

D="/mnt/c/Users/limed/Saved Games/Frontier Developments/Elite Dangerous"

F=`find "$D" -mtime -7 -name 'Journal.*' | sort -r | head -1`

echo
date
echo $F:
echo

cat "$F" | jq .
