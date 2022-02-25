#!/usr/bin/bash
for i in `seq 2 6`
do
    for j in a m
    do
        for k in 0 1 8
        do
            ./nssetup_XxX.sh $i $j $k
            sleep 10
            ./nssetup_rm.sh $i
            mv log/wpan0.log "TestLogs/"$i"x"$i"_"$j"_"$k"L.log"
            ./nssetup_rm.sh $i y
        done
    done
done