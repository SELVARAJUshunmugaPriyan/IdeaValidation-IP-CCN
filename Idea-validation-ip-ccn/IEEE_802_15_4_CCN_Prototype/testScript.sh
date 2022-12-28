#!/usr/bin/bash
# Change the range for 'i' or X in XxX grid/matrix topology
for i in 7 8 9
do
# 'j' denotes adhoc(centralised networking) and mesh(distributed networking)
    for j in a m
    do
# 'k' denotes the loss percentage
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