#!/bin/bash

X=600
Y=248
Z=248

strt=$((X*Y*$2))
slice=$((X*Y))

echo $strt
echo $slice

cat "$1.txt" |tail +$strt |head -n $slice > ../PlaneSliceData/"$1.XY.slice$2.txt"
