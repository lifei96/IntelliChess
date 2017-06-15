#!/bin/bash

> GameLog.txt
for (( i = 0; i < 100; i++ )); do
	echo $i
	python ChessGame.py -m 2 -a AI_search AI_random -d 0
done
cp GameLog.txt ./results/result_search_random.txt