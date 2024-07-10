import numpy as np

from strategy import PursuitStrategy

class DefaultPursuitStrategy(PursuitStrategy):
    @staticmethod
    def calculate_move(evader, pursuers, boundaries):
        return np.zeros(2)
    
class PurePursuit(PursuitStrategy):
    @staticmethod
    def calculate_move(pursuer, evader, boundaries):
        direction = evader.position - pursuer.position
        distance = np.linalg.norm(direction)
        
        if distance < 1e-5:
            return np.zeros(2)
        
        pursuit_direction = direction / distance
        
       
        
        return pursuit_direction * pursuer.max_speed