from agent import Agent

class Pursuer(Agent):
    def __init__(self, x, y, max_speed, acceleration, strategy):
        # Initialize
        super().__init__(x, y, max_speed, acceleration, strategy)
        self.evader = None
        self.pursuers = []

    def set_evader(self, evader):
        self.evader = evader
        
    def set_all_pursuers(self, pursuers):
        self.pursuers = pursuers

    def pursue(self, boundaries):
        if self.evader is None:
            return
        desired_direction = self.strategy.calculate_move(self, self.evader, boundaries)
        self.move(desired_direction)