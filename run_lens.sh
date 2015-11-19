#!/bin/bash

declare -i mode
declare -i ii
mode=1
ii=$$
while true; do
  case $mode in
  1)
    python lenspy.py circ &
    lenspid=$!
    trap "kill $lenspid;kill -s KILL $ii" SIGINT SIGTERM
    sleep 1m
    mode=2
    kill $lenspid
    ;;
  2)
    python lenspy.py lem &
    lenspid=$!
    trap "kill $lenspid;kill -s KILL $ii" SIGINT SIGTERM
    sleep 1m
    mode=3
    kill $lenspid
    ;;
  3)
    python lenspy.py rand &
    lenspid=$!
    trap "kill $lenspid;kill -s KILL $ii" SIGINT SIGTERM
    sleep 1m
    mode=4
    kill $lenspid
    ;;
  4)
    python lenspy.py lissajous &
    lenspid=$!
    trap "kill $lenspid;kill -s KILL $ii" SIGINT SIGTERM
    sleep 1m
    mode=5
    kill $lenspid
  5)
    python lenspy.py cray &
    lenspid=$!
    trap "kill $lenspid;kill -s KILL $ii" SIGINT SIGTERM
    sleep 1m
    mode=6
    kill $lenspid
  6)
    python lenspy.py hypotrochoid &
    lenspid=$!
    trap "kill $lenspid;kill -s KILL $ii" SIGINT SIGTERM
    sleep 1m
    mode=1
    kill $lenspid
  esac
done
