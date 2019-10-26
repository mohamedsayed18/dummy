#!/bin/bash
for i in {0..7}
do
	python3 client.py &
	echo $i
done

