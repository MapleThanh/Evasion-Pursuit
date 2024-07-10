from agent import Agent

class Evader(Agent):
    def __init__(self, x, y, max_speed, acceleration, strategy):
        # Initialize
        super().__init__(x, y, max_speed, acceleration)
        self.pursuers = []
        self.strategy = strategy

    def add_pursuer(self, pursuer):
        if pursuer not in self.pursuers:
            self.pursuers.append(pursuer)

    def remove_pursuer(self, pursuer):
        if pursuer in self.pursuers:
            self.pursuers.remove(pursuer)

    def evade(self, boundaries):
        desired_direction = self.strategy.calculate_move(self, self.pursuers, boundaries)
        self.move(desired_direction)