#! /usr/bin/env bash

python $@ &
entry_pid=$!
echo "$entry_pid" > /tmp/entry_pid
echo "Started with pid $entry_pid"
cat | entr -c -s "kill -TERM \$(cat /tmp/entry_pid );  python $@ & echo \$! > /tmp/entry_pid"