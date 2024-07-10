import os
import sys

# Add the project root and subdirectories to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'Agent'))
sys.path.append(os.path.join(current_dir, 'Application'))
sys.path.append(os.path.join(current_dir, 'Strategy'))

from Application.simulation import Simulation
from Application.visualization import Visualizer

def main():
    print("Starting simulation setup...")
    # Create simulation
    sim = Simulation(500, 500)
    sim.reset()  # This will set up the initial evader and pursuers
    print("Simulation setup complete.")

    print("Creating visualizer...")
    # Create visualizer
    vis = Visualizer(sim)
    print("Visualizer created.")

    print("Starting animation...")
    # Run animation indefinitely
    vis.animate(frames=None)  # None means the animation will run until the window is closed
    print("Animation complete.")

if __name__ == "__main__":
    main()