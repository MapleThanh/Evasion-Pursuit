import numpy as np
import random

from Agent.evader import Evader
from Agent.pursuer import Pursuer
from Strategy.evasion_strategy import NearestNeighborStrategy, DefaultEvasionStrategy
from Strategy.pursuit_trategy import PurePursuit, DefaultPursuitStrategy, VoronoiPursuitStrategy
from Utils.constants import *
from Utils.random import *

class Simulation:
    def __init__(self, width=SIMULATION_WIDTH, height=SIMULATION_HEIGHT):
        self.width = width
        self.height = height
        self.boundaries = (0, width, 0, height)  # (min_x, max_x, min_y, max_y)
        self.evader = None
        self.pursuers = []
        self.capture_distance = CAPTURE_DISTANCE
        
        # Initialize strategies
        self.pursuit_strategy = None
        self.evasion_strategy = None
        self.voronoi_strategy = None

    def reset(self):
        # Set evader
        evader_speed = get_random_evader_speed(EVADER_RANDOM_MIN_SPEED, EVADER_RANDOM_MAX_SPEED)
        evader_position = get_random_evader_position(self.width, self.height)
        self.set_evader(evader_position[0], evader_position[1], 
                        max_speed=evader_speed, 
                        acceleration=EVADER_ACCELERATION,
                        strategy=self.evasion_strategy)

        # Clear existing pursuers
        self.pursuers.clear()

        # Set pursuers
        num_pursuers = get_random_pursuer_count(MIN_PURSUERS, MAX_PURSUERS)
        for _ in range(num_pursuers):
            pursuer_speed = get_random_pursuer_speed(PURSUER_RANDOM_MIN_SPEED, PURSUER_RANDOM_MAX_SPEED)
            pursuer_position = get_random_pursuer_position(self.width, self.height)
            self.add_pursuer(pursuer_position[0], pursuer_position[1], 
                            max_speed=pursuer_speed, 
                            acceleration=PURSUER_ACCELERATION,
                            strategy=self.pursuit_strategy)
            
        # Update references to pursuers for each pursuer
        self.update_pursuer_references()
            
    def set_evader(self, x, y, max_speed, acceleration, strategy):
        self.evader = Evader(x, y, max_speed, acceleration, strategy)
        
    def add_pursuer(self, x, y, max_speed, acceleration, strategy):
        pursuer = Pursuer(x, y, max_speed, acceleration, strategy)
        self.pursuers.append(pursuer)
        self.evader.add_pursuer(pursuer)
        pursuer.set_evader(self.evader)
        
    def set_pursuit_strategy(self, strategy):
        match strategy:
            case "voronoi":
                if self.voronoi_strategy is None:
                    self.voronoi_strategy = VoronoiPursuitStrategy(20, self.boundaries)
                self.pursuit_strategy = self.voronoi_strategy
            case "pure":
                self.pursuit_strategy = PurePursuit()
            case "default":
                self.pursuit_strategy = DefaultPursuitStrategy()
            case _:
                raise ValueError(f"Unknown pursuit strategy: {strategy}")

    def set_evasion_strategy(self, strategy):
        match strategy:
            case "nearest-neighbor":
                self.evasion_strategy = NearestNeighborStrategy()
            case "default":
                self.evasion_strategy = DefaultEvasionStrategy()
            case _:
                raise ValueError(f"Unknown evasion strategy: {strategy}")

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
                    
        # Check for capture
        if self.is_captured():
            print("Evader captured! Resetting simulation...")
            self.reset()
            return True  # Indicate that a reset occurred
        return False
    
    def update_pursuer_references(self):
        for pursuer in self.pursuers:
            other_pursuers = [p for p in self.pursuers if p is not pursuer]
            pursuer.set_all_pursuers(other_pursuers)
            
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