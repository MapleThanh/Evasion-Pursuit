import numpy as np

from strategy import EvasionStrategy

# Default placeholder strategy for evasion
class DefaultEvasionStrategy(EvasionStrategy):
    @staticmethod
    def calculate_move(evader, pursuers, boundaries):
        # Stay still
        return np.zeros(2)
    
class NearestNeighborStrategy(EvasionStrategy):
    @staticmethod
    def calculate_move(evader, pursuers, boundaries):
        if not pursuers:
            return np.zeros(2)

        pursuer_positions = np.array([p.position for p in pursuers])
        directions = evader.position - pursuer_positions
        distances = np.linalg.norm(directions, axis=1)
        distances = np.maximum(distances, 1e-5)
        
        evasion_direction = np.sum(directions / distances[:, np.newaxis]**2, axis=0)
        
        # Boundary handling: "Bounce" off walls
        min_x, max_x, min_y, max_y = boundaries
        if evader.position[0] <= min_x or evader.position[0] >= max_x:
            evasion_direction[0] *= -1
        if evader.position[1] <= min_y or evader.position[1] >= max_y:
            evasion_direction[1] *= -1
        
        if np.linalg.norm(evasion_direction) > 0:
            evasion_direction = evasion_direction / np.linalg.norm(evasion_direction)
        
        return evasion_direction * evader.max_speed
