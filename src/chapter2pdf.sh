#!/bin/bash

BASE="../out/"
START=0
END=0

# check args
if [ $# -eq 1 ]
then
    START=$1
    END=$1
elif [ $# -eq 2 ]
then
    START=$1
    END=$2
else
    # if no or too many args are set quit the script
    echo "invalid number of arguments"
    exit 1
fi

# generate pdf file for each chapter
for (( i=$START; i<=$END; i++ ))
do
    # stitch directory name
    DIR=$BASE$i"/*"
    # stitch file name
    FILE=$BASE"Kapitel_"$i".pdf"
    # stitch final convert call
    CALL="convert "$DIR" "$FILE
    # make call
    echo "convert chapter "$i"..."
    $($CALL)
done
