import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Utils.constants import *
class Visualizer:
    def __init__(self, simulation):
        self.simulation = simulation
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, simulation.width)
        self.ax.set_ylim(0, simulation.height)
        self.evader_dot, = self.ax.plot([], [], 'ro', markersize=EVADER_SIZE, label='Evader')
        self.pursuer_dots = []
        self.ax.legend()

    def init(self):
        self.evader_dot.set_data([], [])
        for dot in self.pursuer_dots:
            dot.set_data([], [])
        return [self.evader_dot] + self.pursuer_dots

    def update(self, frame):
        # Call step() function in simulation
        self.simulation.step()
        
        # Update evader
        self.evader_dot.set_data([self.simulation.evader.position[0]], [self.simulation.evader.position[1]])
        
        # Update pursuers
        while len(self.pursuer_dots) < len(self.simulation.pursuers):
            new_dot, = self.ax.plot([], [], 'bo', markersize=PURSUER_SIZE)
            self.pursuer_dots.append(new_dot)
        
        for i, pursuer in enumerate(self.simulation.pursuers):
            self.pursuer_dots[i].set_data([pursuer.position[0]], [pursuer.position[1]])
        
        # Remove excess dots
        for dot in self.pursuer_dots[len(self.simulation.pursuers):]:
            dot.set_data([], [])
        
        # Check for collision
        if self.simulation.is_captured():
            print("Evader captured! Resetting simulation...")
            
            # Reset the simulation
            self.simulation.reset()
        
        return [self.evader_dot] + self.pursuer_dots

    def animate(self, frames):
        anim = FuncAnimation(self.fig, self.update, frames=frames, init_func=self.init, blit=True, interval=ANIMATION_INTERVAL)
        plt.show(block=True)  # This will keep the plot open