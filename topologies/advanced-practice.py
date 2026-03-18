# advanced-practice.py
# Final deployment topology named "Advanced Practice"
# Week 3 Task - Deploy your own network named IE as 'Advanced Practice'

from seedemu.core import Emulator
from seedemu.layers import Base, Routing, Ebgp, PeerRelationship
from seedemu.compiler import Docker

def main():
    emu = Emulator()
    base = Base()
    routing = Routing()
    ebgp = Ebgp()

    # Create AS "Advanced Practice" (AS100)
    as100 = base.createAutonomousSystem(100)
    net = as100.createNetwork('advanced-practice-net')
    
    # Add 2 hosts (smaller quantity of nodes)
    as100.createHost('host-0').joinNetwork('advanced-practice-net')
    as100.createHost('host-1').joinNetwork('advanced-practice-net')
    as100.createRouter('router0').joinNetwork('advanced-practice-net')

    # Create a second AS for connectivity
    as200 = base.createAutonomousSystem(200)
    net2 = as200.createNetwork('net0')
    as200.createHost('host-0').joinNetwork('net0')
    as200.createRouter('router0').joinNetwork('net0')

    # Internet Exchange
    base.createInternetExchange(100)
    as100.getRouter('router0').joinNetwork('ix100')
    as200.getRouter('router0').joinNetwork('ix100')

    # BGP Peering
    ebgp.addPrivatePeering(100, 100, 200,
                           abRelationship=PeerRelationship.Peer)

    emu.addLayer(base)
    emu.addLayer(routing)
    emu.addLayer(ebgp)
    emu.render()
    emu.compile(Docker(), './output-advanced-practice')
    
    print("Advanced Practice network deployed successfully!")

if __name__ == '__main__':
    main()
