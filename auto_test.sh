#!/bin/bash

> GameLog.txt
for (( i = 0; i < 100; i++ )); do
	echo $i
	python ChessGame.py -m 2 -a AI_MCTS AI_random -d 0
done
cp GameLog.txt ./results/result_MCTS_random.txt