# network.py
# Advanced Practice - Seed Internet Emulator
# Custom Network Topology: "Advanced Practice"
#
# This file defines a smaller custom Internet topology
# using the Seed Internet Emulator framework.
#
# Original Seed Emulator: https://github.com/seed-labs/seed-emulator

from seedemu.core import Emulator, Binding, Filter
from seedemu.layers import Base, Routing, Ebgp, Ibgp, Ospf, WebService
from seedemu.services import WebService
from seedemu.compiler import Docker

###############################################################################
# VARIABLES - These define the structure of our network
###############################################################################

# Autonomous System Numbers (ASNs)
# Each AS represents a different organisation/ISP on the Internet
AS_ADVANCED_PRACTICE = 100   # Our main AS - named "Advanced Practice"
AS_ISP_1             = 200   # Internet Service Provider 1
AS_ISP_2             = 300   # Internet Service Provider 2

# Internet Exchange Point
# This is where different AS networks connect and exchange traffic
IX_NUMBER = 1000

# Network prefixes (IP address ranges)
# Each network gets its own range of IP addresses
NETWORK_PREFIX_AS100 = '10.100.0.0/24'
NETWORK_PREFIX_AS200 = '10.200.0.0/24'
NETWORK_PREFIX_AS300 = '10.300.0.0/24'

# Number of hosts per network (kept small for this custom topology)
NUM_HOSTS_AS100 = 2   # Smaller quantity of nodes as required
NUM_HOSTS_AS200 = 2
NUM_HOSTS_AS300 = 1

###############################################################################
# CONFIGURATION - How the network is built
###############################################################################

def create_network():
    """
    Creates the main network topology.
    
    What is a variable? 
    A variable stores a value that can be changed. For example,
    NUM_HOSTS_AS100 = 2 means we have 2 hosts. Change it to 5 to get 5 hosts.
    
    What is configuration?
    Configuration defines HOW the network behaves - IP addresses,
    routing protocols, which networks connect to each other, etc.
    """
    
    # Create the emulator object - this is the main container for everything
    emu = Emulator()
    
    # Create the base layer - defines AS structure and physical topology
    base = Base()
    
    # Create the routing layer - handles how packets travel between networks
    routing = Routing()
    
    # Create BGP layer - Border Gateway Protocol
    # This is how different AS networks advertise routes to each other
    ebgp = Ebgp()

    ###########################################################################
    # CREATE AUTONOMOUS SYSTEMS
    ###########################################################################
    
    # AS100 - "Advanced Practice" (our main network)
    as100 = base.createAutonomousSystem(AS_ADVANCED_PRACTICE)
    
    # AS200 - ISP 1
    as200 = base.createAutonomousSystem(AS_ISP_1)
    
    # AS300 - ISP 2
    as300 = base.createAutonomousSystem(AS_ISP_2)

    ###########################################################################
    # CREATE NETWORKS INSIDE EACH AS
    ###########################################################################
    
    # Each AS has its own internal network
    net100 = as100.createNetwork('net0')
    net200 = as200.createNetwork('net0')
    net300 = as300.createNetwork('net0')

    ###########################################################################
    # ADD HOSTS (nodes) TO EACH NETWORK
    # This is where NUM_HOSTS variables are used
    # Change NUM_HOSTS_AS100 = 2 to a different number to add more hosts
    ###########################################################################
    
    # Add hosts to AS100 "Advanced Practice"
    for i in range(NUM_HOSTS_AS100):
        as100.createHost(f'host-{i}').joinNetwork('net0')
    
    # Add hosts to AS200
    for i in range(NUM_HOSTS_AS200):
        as200.createHost(f'host-{i}').joinNetwork('net0')
    
    # Add hosts to AS300
    for i in range(NUM_HOSTS_AS300):
        as300.createHost(f'host-{i}').joinNetwork('net0')

    ###########################################################################
    # ADD ROUTERS
    # Routers connect networks together and forward traffic
    ###########################################################################
    
    as100.createRouter('router0').joinNetwork('net0')
    as200.createRouter('router0').joinNetwork('net0')
    as300.createRouter('router0').joinNetwork('net0')

    ###########################################################################
    # CREATE INTERNET EXCHANGE (IX)
    # This is where AS networks meet and exchange routing information
    ###########################################################################
    
    base.createInternetExchange(IX_NUMBER)
    
    # Connect routers to the Internet Exchange
    as100.getRouter('router0').joinNetwork(f'ix{IX_NUMBER}')
    as200.getRouter('router0').joinNetwork(f'ix{IX_NUMBER}')
    as300.getRouter('router0').joinNetwork(f'ix{IX_NUMBER}')

    ###########################################################################
    # BGP PEERING - Define which AS networks talk to each other
    ###########################################################################
    
    # AS100 "Advanced Practice" peers with both ISPs
    ebgp.addPrivatePeering(IX_NUMBER, AS_ADVANCED_PRACTICE, AS_ISP_1,
                           abRelationship=PeerRelationship.Peer)
    ebgp.addPrivatePeering(IX_NUMBER, AS_ADVANCED_PRACTICE, AS_ISP_2,
                           abRelationship=PeerRelationship.Peer)
    # The two ISPs also peer with each other
    ebgp.addPrivatePeering(IX_NUMBER, AS_ISP_1, AS_ISP_2,
                           abRelationship=PeerRelationship.Peer)

    ###########################################################################
    # ASSEMBLE AND COMPILE
    ###########################################################################
    
    emu.addLayer(base)
    emu.addLayer(routing)
    emu.addLayer(ebgp)
    
    # Render the emulator
    emu.render()
    
    # Compile to Docker containers
    emu.compile(Docker(), './output-advanced-practice')
    
    print("✅ Network 'Advanced Practice' compiled successfully!")
    print("➡️  Run: cd output-advanced-practice && docker-compose up")

###############################################################################
# MAIN
###############################################################################

if __name__ == '__main__':
    create_network()
