#!/usr/bin/bash
cd TestLogs/
for i in `cat ../rfnFileList.txt`
do
    sed -i "$(( $(wc -l <$i)-2+1 )),$ d" $i
    #sed -i -e 1,2d $i
done