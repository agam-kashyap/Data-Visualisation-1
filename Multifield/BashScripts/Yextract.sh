#!/bin/bash

X=600
Y=248
Z=248
# $1 is the extracted text file without the txt extension. It runs faster for a file than unzipping every time
# $2 is plane y=c
for((i=0; i<$Z; i++))
do
	strt=$((X*Y*$i + X*$2))
	echo "$i ---- $strt"
	cat "$1.txt" |tail +$strt |head -n $X >> ../PlaneSliceData/"$1.XZ.slice$2.txt"
done
