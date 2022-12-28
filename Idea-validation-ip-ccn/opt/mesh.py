#!/usr/bin/python
import sys
from mininet.node import Controller
from mn_wifi.node import OVSKernelAP
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology():
	"Create a network."
	net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference, controller=Controller)
	info("*** Creating nodes\n")
	sta44 = net.addStation('sta44', position='400,400,0')
	sta45 = net.addStation('sta45', position='450,400,0')
	sta54 = net.addStation('sta54', position='400,450,0')
	sta55 = net.addStation('sta55', position='450,450,0')
		
	ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', wlans=2,
												 channel='1', position='500,500,0')
	c1 = net.addController('c1', controller=Controller)

	info("*** Configuring Propagation Model\n")
	net.setPropagationModel(model="logDistance", exp=4)

	info("*** Configuring wifi nodes\n")
	net.configureWifiNodes()

	info("*** Creating links\n")
	net.addLink(sta44, cls=mesh, ssid='meshNet', intf='sta44-wlan0', channel=5)
	net.addLink(sta45, cls=mesh, ssid='meshNet', intf='sta45-wlan0', channel=5)
	net.addLink(sta54, cls=mesh, ssid='meshNet', intf='sta54-wlan0', channel=5)
	net.addLink(sta55, cls=mesh, ssid='meshNet', intf='sta55-wlan0', channel=5)
	net.addLink(ap1, cls=mesh, ssid='meshNet', intf='ap1-wlan2', channel=5)
	
	info("*** Starting network\n")
	net.build()
	net.addNAT().configDefault()
	c1.start()
	ap1.start([c1])
	

	info("*** Running CLI\n")
	CLI(net)	

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()