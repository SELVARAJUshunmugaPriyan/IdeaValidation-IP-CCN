#!/usr/bin/bash
for i in 7 8 9
do
    for j in a m
    do
        for k in 0 2 5 10 15 20 30
        do
            ./nssetup_XxX.sh $i $j $k
            sleep 300
            ./nssetup_rm.sh $i
            mv log/wpan0.log "TestLogs/"$i"x"$i"_"$j"_"$k"L.log"
            ./nssetup_rm.sh $i y
        done
    done
done