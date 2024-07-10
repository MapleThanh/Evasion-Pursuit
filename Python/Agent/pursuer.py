from agent import Agent

class Pursuer(Agent):
    def __init__(self, x, y, max_speed, acceleration, strategy):
        # Initialize
        super().__init__(x, y, max_speed, acceleration)
        self.evader = None
        self.strategy = strategy

    def set_evader(self, evader):
        self.evader = evader

    def pursue(self, boundaries):
        if self.evader is None:
            return
        desired_direction = self.strategy.calculate_move(self, self.evader, boundaries)
        self.move(desired_direction)