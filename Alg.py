import random
from collections import defaultdict

SUSCEPTIBLE = "S" # Not infected
INFECTED = "I" # Infected
RECOVERED = "R" # Recovered

class Airport:
    def __init__(self, code):
        self.code = code
        self.state = SUSCEPTIBLE

class FlightNetwork:
    def __init__(self):
        self.airports = {}
        self.edges = defaultdict(list)

    def add_airport(self, code):
        self.airports[code] = Airport(code)

    def add_flight(self, src, dst):
        self.edges[src].append(dst)


class Simulation:
    def __init__(self, network, infection_chance=0.3, recovery_chance=0.1):
        self.network = network
        self.infection_chance = infection_chance
        self.recovery_chance = recovery_chance
        self.time = 0
        self.history = []

    def step(self):
        self.time += 1
        new_infections = []

        for code, airport in self.network.airports.items():
            if airport.state != INFECTED:
                continue

            for neighbor_code in self.network.edges[code]:
                neighbor = self.network.airports[neighbor_code]
                if neighbor.state == SUSCEPTIBLE:
                    if random.random() < self.infection_chance:
                        new_infections.append(neighbor_code) # Mark for infection

            if random.random() < self.recovery_chance: # Recover
                airport.state = RECOVERED

        for code in new_infections:
            if self.network.airports[code].state == SUSCEPTIBLE:
                self.network.airports[code].state = INFECTED

        counts = {SUSCEPTIBLE: 0, INFECTED: 0, RECOVERED: 0} # Count states to keep history
        
        for a in self.network.airports.values():
            counts[a.state] += 1
            
        self.history.append(counts)

    def run(self, steps):
        for _ in range(steps):
            self.step()

def run():
    net = FlightNetwork()

    for code in ["ATL", "JFK", "LAX", "MIA", "SFO"]:
        net.add_airport(code)

    net.add_flight("ATL", "JFK")
    net.add_flight("JFK", "LAX")
    net.add_flight("LAX", "SFO")
    net.add_flight("SFO", "MIA")
    net.add_flight("MIA", "ATL")

    net.airports["ATL"].state = INFECTED # Initial infection

    sim = Simulation(net, infection_chance=0.4, recovery_chance=0.2)
    sim.run(20) # Run for 20 time steps 

    # Could write a function to pretty print this for later
    # Like what airports are actually infeced at each step
    for t, counts in enumerate(sim.history):
        print(f"t={t}: {counts}")

run()