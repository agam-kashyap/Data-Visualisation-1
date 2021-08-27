#!/bin/bash

X=600
Y=248
Z=248

# $2 is the x=c plane
for((i=0; i< $Y*$Z; i++))
do
	echo "$i"
	cat $1 | tail +$(($2 + i*X)) | head -n 1 >> trialX.txt
done
