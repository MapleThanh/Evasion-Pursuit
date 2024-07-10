import numpy as np
import random

from Agent.evader import Evader
from Agent.pursuer import Pursuer
from Strategy.evasion_strategy import NearestNeighborStrategy, DefaultEvasionStrategy
from Strategy.pursuit_trategy import PurePursuit, DefaultPursuitStrategy

class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.boundaries = (0, width, 0, height)  # (min_x, max_x, min_y, max_y)
        self.evader = None
        self.pursuers = []
        self.capture_distance = 1.0

    def reset(self):
        # Reset evader
        self.set_evader(random.uniform(0, self.width), 
                        random.uniform(0, self.height), 
                        max_speed=1.0, 
                        acceleration=0.5,
                        strategy=NearestNeighborStrategy)

        # Clear existing pursuers
        self.pursuers.clear()

        # Add random number of pursuers (between 1 and 5)
        num_pursuers = random.randint(1, 5)
        for _ in range(num_pursuers):
            self.add_pursuer(random.uniform(0, self.width), 
                            random.uniform(0, self.height), 
                            max_speed=0.8, 
                            acceleration=0.5,
                            strategy=PurePursuit)
            
    def set_evader(self, x, y, max_speed, acceleration, strategy=DefaultEvasionStrategy):
        self.evader = Evader(x, y, max_speed, acceleration, strategy)
        
    def add_pursuer(self, x, y, max_speed, acceleration, strategy=DefaultPursuitStrategy):
        pursuer = Pursuer(x, y, max_speed, acceleration, strategy)
        self.pursuers.append(pursuer)
        self.evader.add_pursuer(pursuer)
        pursuer.set_evader(self.evader)

    def step(self):
        self.evader.evade(self.boundaries)
        for pursuer in self.pursuers:
            pursuer.pursue(self.boundaries)
        
        # Boundary check
        self.evader.position = np.clip(self.evader.position, [self.boundaries[0], self.boundaries[2]], [self.boundaries[1], self.boundaries[3]])
        for pursuer in self.pursuers:
            pursuer.position = np.clip(pursuer.position, [self.boundaries[0], self.boundaries[2]], [self.boundaries[1], self.boundaries[3]])

    def is_captured(self):
        return any(np.linalg.norm(self.evader.position - p.position) < self.capture_distance for p in self.pursuers)

    def run(self, steps):
        for i in range(steps):
            self.step()
            if self.is_captured():
                print(f"Evader captured at step {i}")
                return i
        print("Evader escaped")
        return steps