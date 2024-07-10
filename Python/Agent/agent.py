import numpy as np

class Agent:
    def __init__(self, x, y, max_speed, acceleration):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0], dtype=float)
        self.max_speed = max_speed
        self.acceleration = acceleration

    def move(self, desired_direction):
        # Normalize desired direction
        if np.linalg.norm(desired_direction) > 0:
            desired_direction = desired_direction / np.linalg.norm(desired_direction)

        # Calculate acceleration vector
        acceleration_vector = desired_direction * self.acceleration

        # Update velocity
        self.velocity += acceleration_vector

        # Limit speed to max_speed
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = self.velocity / speed * self.max_speed

        # Update position
        self.position += self.velocity