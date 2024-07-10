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
    
    # Reset simulation
    sim.reset() 
    print("Simulation setup complete.")
    print("Creating visualizer...")
    
    # Create visualizer
    vis = Visualizer(sim)
    print("Visualizer created.")

    # Run animation indefinitely
    print("Starting animation...")
    vis.animate(frames=None)
    
    # Stop animation successfully  
    print("Animation complete.")

if __name__ == "__main__":
    main()