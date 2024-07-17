import numpy as np
import random

from Agent.evader import Evader
from Agent.pursuer import Pursuer
from Strategy.evasion_strategy import NearestNeighborStrategy, DefaultEvasionStrategy
from Strategy.pursuit_trategy import PurePursuit, DefaultPursuitStrategy
from Utils.constants import *
class Simulation:
    def __init__(self, width=SIMULATION_WIDTH, height=SIMULATION_HEIGHT):
        self.width = width
        self.height = height
        self.boundaries = (0, width, 0, height)  # (min_x, max_x, min_y, max_y)
        self.evader = None
        self.pursuers = []
        self.capture_distance = CAPTURE_DISTANCE

    def reset(self):
        # Set evader
        self.set_evader(random.uniform(0, self.width), 
                        random.uniform(0, self.height), 
                        max_speed=EVADER_MAX_SPEED, 
                        acceleration=EVADER_ACCELERATION,
                        strategy=NearestNeighborStrategy)

        # Clear existing pursuers
        self.pursuers.clear()

        # Set pursuers
        num_pursuers = random.randint(MIN_PURSUERS, MAX_PURSUERS)
        for _ in range(num_pursuers):
            self.add_pursuer(random.uniform(0, self.width), 
                            random.uniform(0, self.height), 
                            max_speed=PURSUER_MAX_SPEED, 
                            acceleration=PURSUER_ACCELERATION,
                            strategy=PurePursuit)
            
    def set_evader(self, x, y, max_speed, acceleration, strategy=DefaultEvasionStrategy):
        self.evader = Evader(x, y, max_speed, acceleration, strategy)
        
    def add_pursuer(self, x, y, max_speed, acceleration, strategy=DefaultPursuitStrategy):
        pursuer = Pursuer(x, y, max_speed, acceleration, strategy)
        self.pursuers.append(pursuer)
        self.evader.add_pursuer(pursuer)
        pursuer.set_evader(self.evader)

    def step(self):
        # Step update for evader
        self.evader.evade(self.boundaries)
        
        # Step update for pursuers
        for pursuer in self.pursuers:
            pursuer.pursue(self.boundaries)
        
        # Boundary check for evader
        self.evader.position = np.clip(self.evader.position, [self.boundaries[0], self.boundaries[2]], [self.boundaries[1], self.boundaries[3]])
        
        # Boundary check for pursuers
        for pursuer in self.pursuers:
            pursuer.position = np.clip(pursuer.position, [self.boundaries[0], self.boundaries[2]], [self.boundaries[1], self.boundaries[3]])

    def is_captured(self):
        # Collision check between evader and every pursuer
        return any(np.linalg.norm(self.evader.position - p.position) < self.capture_distance for p in self.pursuers)

    # Used to run without visualization
    def run(self, steps):
        for i in range(steps):
            self.step()
            if self.is_captured():
                print(f"Evader captured at step {i}")
                return i
        print("Evader escaped")
        return steps