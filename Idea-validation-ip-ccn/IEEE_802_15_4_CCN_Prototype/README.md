Title               :       Prototype for Content Centric Networking in IEEE 802.15.4 wireless technology
Scope               :       To build and evaluate the network performance of CCN in WSN, through Linux based network simulation and using
                            wpan sockets available in latest Linux kernels. 

Technical Reoport   :       S. P. Selvaraju, A. Balador, H. Fotouhi, and M. Björkman, ‘Performance Analysis of SDN based network 
                            management in Content Centric Networks for WSN’, Mälardalen Real-Time Research Centre (MRTC), Västerås, 2022. (https://www.diva-portal.org/smash/get/diva2:1652946/FULLTEXT01.pdf)

Objective           :       To design, implement, evaluate and analyse the performance of CCN in WSN, using network simulation under 
                            mesh networking with grid/matrix topology.

Usage               :       

> testScript.sh
>   #/usr/bin/bash
>   # Change the range for 'i' or X in XxX grid/matrix topology
>   for i in 7 8 9
>   do
>   # 'j' denotes adhoc(centralised networking) and mesh(distributed networking)
>      for j in a m
>      do
>   # 'k' denotes the loss percentage
>        for k in 0 2 5 10 15 20 30
>        do
>            ./nssetup_XxX.sh $i $j $k
>            sleep 300
>            ./nssetup_rm.sh $i
>            mv log/wpan0.log "TestLogs/"$i"x"$i"_"$j"_"$k"L.log"
>            ./nssetup_rm.sh $i y
>        done
>     done
>   done
