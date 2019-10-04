#!/usr/bin/env bash

db=$1

for file in "${@:2}"; do
    name=$(basename $file .csv.tar.gz)

    sqlite3 $db "CREATE VIRTUAL TABLE IF NOT EXISTS $name USING FTS5(label,name,bio,id); DELETE FROM $name;"
    tar -Oxf $file | sqlite3 $db --csv ".import /dev/stdin $name"
done
