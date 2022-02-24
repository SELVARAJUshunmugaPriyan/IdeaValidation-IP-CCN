#!/usr/bin/python

'This example shows how to create multiple interfaces in stations'

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.wmediumdConnector import interference


def topology():
	"Create a network."
	net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

	info("*** Creating nodes\n")
	sta55 = net.addStation('sta55', position='200,200,0')
	sta56 = net.addStation('sta56', position='250,200,0')
	sta65 = net.addStation('sta65', position='200,250,0')
	sta66 = net.addStation('sta66', position='250,250,0', wlans=2)
	ap1 = net.addAccessPoint('ap1', ssid='ssid_1', mode='g', channel='5',
							 failMode="standalone", position='300,300,0')

	info("*** Configuring Propagation Model\n")
	net.setPropagationModel(model="logDistance", exp=4)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	info("*** Associating...\n")
	net.addLink(ap1, sta66)
	net.addLink(sta55, cls=adhoc, ssid='adhocNet', intf='sta55-wlan0')
	net.addLink(sta56, cls=adhoc, ssid='adhocNet', intf='sta56-wlan0')
	net.addLink(sta65, cls=adhoc, ssid='adhocNet', intf='sta65-wlan0')
	net.addLink(sta66, cls=adhoc, ssid='adhocNet', intf='sta66-wlan1')

	info("*** Starting network\n")
	net.build()
	net.addNAT().configDefault()
	ap1.start([])

	info("*** Addressing...\n")
	sta55.setIP('192.168.10.55/24', intf="sta55-wlan0")
	sta56.setIP('192.168.10.56/24', intf="sta56-wlan0")
	sta65.setIP('192.168.10.65/24', intf="sta65-wlan0")
	sta66.setIP('192.168.10.66/24', intf="sta66-wlan1")

	net.plotGraph(max_x=300, max_y=300)

	sta55.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	sta66.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	ap1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

	sta55.cmd("ip r a 192.168.1.7/24 via 192.168.10.66")
	sta66.cmd("ip r a 192.168.1.7/24 via 10.0.0.5")

	ap1.cmd("ip r a 192.168.10.55/32 via 10.0.0.4")

	info("*** Running CLI\n")
	CLI(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
