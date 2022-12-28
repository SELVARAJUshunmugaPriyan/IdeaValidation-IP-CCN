#!/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo "ERROR: REQUIRED Run as root user"
	exit
fi

if [ -z "$1" ]; then
	echo "ERROR: REQUIRED No value for X in X x X grid network"
	exit
fi

rmmod mac802154_hwsim
rmmod mac802154
rmmod ieee802154_6lowpan
rmmod ieee802154
modprobe mac802154_hwsim

numberOfNodes=`echo $1'*'$1 | bc`

for i in `seq 0 $numberOfNodes`
	do	wpan-hwsim add
done

# BUILD TOPOLOGY
for i in `seq 0 $numberOfNodes`; do	
	# CONFIGURE NETWORK NAMESPACE
	ip netns add wpan$i
	
	if [ $i == 0 ]; then
		eval "wpan-hwsim edge add "$i' '`expr $i + 1`
	    eval "wpan-hwsim edge add "`expr $i + 1`' '$i
		# CONFIGURE VIRTUAL LINK TOWARDS SDN CONTROLLER
		#ip link add tunnel_start type veth peer name tunnel_end
		#ip link set tunnel_end netns wpan0
		#ip link set dev tunnel_start up
		#ip a add 10.0.254.1/24 dev tunnel_start
		#ip netns exec wpan0 ip link set dev tunnel_end up
		#ip netns exec wpan0 ip a add 10.0.254.2/24 dev tunnel_end
	else
		if [ `expr "$i" % $1` != 0 ]; then
			# East
			eval "wpan-hwsim edge add "$i' '`expr $i + 1`
		    eval "wpan-hwsim edge add "`expr $i + 1`' '$i
		fi
		if [ `expr "$i" % $1` != 0 -a $i -lt `expr $numberOfNodes - $1 + 1` ]; then
			# SouthEast
			eval "wpan-hwsim edge add "$i' '`expr $i + $1 + 1`
		    eval "wpan-hwsim edge add "`expr $i + $1 + 1`' '$i
		fi
		if [ $i -lt `expr $numberOfNodes - $1 + 1` ];then
			# South
			eval "wpan-hwsim edge add "$i' '`expr $i + $1`
		    eval "wpan-hwsim edge add "`expr $i + $1`' '$i
		fi
		if [ `expr "$i" % $1` != 1 -a $i -lt `expr $numberOfNodes - $1 + 1` ];then
			# SouthWest
			eval "wpan-hwsim edge add "$i' '`expr $i + $1 - 1`
		    eval "wpan-hwsim edge add "`expr $i + $1 - 1`' '$i
		fi
	fi

	# CONFIGURE NETWORK INTERFACE
	iwpan phy phy$i set netns name wpan$i
	ip netns exec wpan$i ip link set dev wpan$i down
	ip netns exec wpan$i ip link set dev wpan$i address 00:12:37:00:00:00:00:$i
	ip netns exec wpan$i iwpan dev wpan$i set pan_id 0xbeef
	ip netns exec wpan$i ip link set dev wpan$i up

	if [ $i == 0 ]; then
		# STARTING THE NODE PYTHON PROCESS
		# IMPORTANT : Kindly change the directory path in line 73 and 75 to point towards the absolute path of 'wpaNodeSock.py' and change the output location for log file in line 73
		ip netns exec wpan$i /home/priyan/github-repo-offline/IdeaValidation-IP-CCN/Idea-validation-ip-ccn/IEEE_802_15_4_CCN_Prototype/src/wpaNodeSock.py $i $1 $2 $3 &>>/home/priyan/github-repo-offline/IdeaValidation-IP-CCN/Idea-validation-ip-ccn/IEEE_802_15_4_CCN_Prototype/logs/wpan$i.log &
	else
		ip netns exec wpan$i /home/priyan/github-repo-offline/IdeaValidation-IP-CCN/Idea-validation-ip-ccn/IEEE_802_15_4_CCN_Prototype/src/wpaNodeSock.py $i $1 $2 $3 &>>/dev/null &
	fi
done