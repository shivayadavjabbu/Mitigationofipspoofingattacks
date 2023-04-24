from mininet.network import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink

# create the network
network = Mininet(controller=RemoteController, switch=OVSKernelSwitch, link=TCLink)

# add the controller
controller0 = network.addController('controller0', controller=RemoteController, ip='127.0.0.1', port=6633)

# add the switches
switch1 = network.addSwitch('switch1',cls=OVSKernelSwitch, namespace='switch1-ns')
switch2 = network.addSwitch('switch2',cls=OVSKernelSwitch, namespace='switch2-ns')
switch3 = network.addSwitch('switch3',cls=OVSKernelSwitch, namespace='switch3-ns')


# add the nodes
client = network.addHost('client',ip='10.0.0.1')
attacker1 = network.addHost('attacker1',ip='10.0.0.2')
attacker2 = network.addHost('attacker2',ip='10.0.0.3')
attacker3 = network.addHost('attacker3',ip='10.0.0.4')
attacker4 = network.addHost('attacker4',ip='10.0.0.5')
attacker5 = network.addHost('attacker5',ip='10.0.0.6')
attacker6 = network.addHost('attacker6',ip='10.0.0.7')
attacker7 = network.addHost('attacker7',ip='10.0.0.8')
server = network.addHost('server',ip='10.0.0.9')

# add the links
network.addLink(switch1, client, bw=10)
network.addLink(switch1, attacker1, bw=10)
network.addLink(switch1, attacker2, bw=10)
network.addLink(switch2, attacker3, bw=10)
network.addLink(switch2, attacker4, bw=10)
network.addLink(switch2, attacker5, bw=10)
network.addLink(switch3, attacker6, bw=10)
network.addLink(switch3, attacker7, bw=10)
network.addLink(switch3, server, bw=10)
network.addLink(switch1, switch2, bw=10)
network.addLink(switch2, switch3, bw=10)

# start the network
network.start()

# start the controller
network.controllers[0].start()

# run the command line interface
network.interact()

# stop the network
network.stop()
