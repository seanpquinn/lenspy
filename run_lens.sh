#!/bin/bash

declare -i mode
declare -i ii
mode=1
ii=$$
while true; do
  case $mode in
  1)
    python lens_circ.py &
    lenspid=$!
    trap "kill $lenspid;kill -s KILL $ii" SIGINT SIGTERM
    sleep 2m
    mode=2
    kill $lenspid
    ;;
  2)
    python lens_lem.py &
    lenspid=$!
    trap "kill $lenspid;kill -s KILL $ii" SIGINT SIGTERM
    sleep 2m
    mode=3
    kill $lenspid
    ;;
  3)
    python lens_rand.py &
    lenspid=$!
    trap "kill $lenspid;kill -s KILL $ii" SIGINT SIGTERM
    sleep 2m
    mode=1
    kill $lenspid
    ;;
  esac
done
