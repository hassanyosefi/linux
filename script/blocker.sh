#! /bin/bash
log_path=$1
n=$2
echo "`awk '{print $1}' $log_path | sort | uniq -c | awk -v no=$n '($1 >= no) {print $2}'`"
