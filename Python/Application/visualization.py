import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

from Utils.constants import *

class Visualizer:
    def __init__(self, simulation):
        self.simulation = simulation
        self.fig, self.ax = plt.subplots(figsize=(12, 9))   
        self.pursuer_dots = []    
        self.legend = None 
        self.setup_plot()

    def setup_plot(self):
        self.ax.clear()
        self.ax.set_xlim(0, self.simulation.width)
        self.ax.set_ylim(0, self.simulation.height)
        
        self.pursuer_cmap = LinearSegmentedColormap.from_list("pursuer_reds", PURSUER_COLORS)
        
        self.init_evader_legend()
        self.init_pursuer_legend()
        
        self.init_evader_text()
        self.init_pursuer_text()
        
        self.update_legend()

    def init(self):
        return [self.evader_dot] + self.pursuer_dots + [self.evader_text] + self.pursuer_texts

    def update(self, frame):
        reset_occurred = self.simulation.step()
        
        if reset_occurred:
            self.setup_plot()
        else:
            self.update_evader()
            self.update_pursuers()
        
        return [self.evader_dot] + self.pursuer_dots + [self.evader_text] + self.pursuer_texts

    def animate(self, frames):
        anim = FuncAnimation(
            self.fig, 
            self.update, 
            frames=frames, 
            init_func=self.init, 
            blit=True, 
            interval=ANIMATION_INTERVAL,
            cache_frame_data=False
        )
        plt.tight_layout()
        plt.show(block=True)
        
    def update_legend(self):
        if self.legend:
            self.legend.remove()
        handles = [self.evader_dot] + self.pursuer_dots
        labels = ['Evader'] + [f'Pursuer {i+1}' for i in range(len(self.pursuer_dots))]
        self.ax.legend(handles, labels, loc='upper right', bbox_to_anchor=(1.3, 1))
        self.fig.canvas.draw_idle()
    
    def init_evader_text(self):
        self.evader_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, fontsize=8, verticalalignment='top')
        
    def init_pursuer_text(self):
        self.pursuer_texts = [self.ax.text(0.02, 0.94 - i*0.04, '', transform=self.ax.transAxes, fontsize=8, verticalalignment='top') 
                              for i in range(MAX_PURSUERS)]
        
    def init_evader_legend(self):
        self.evader_dot = self.ax.scatter([], [], c=EVADER_COLOR, s=EVADER_SIZE, label='Evader')

    def init_pursuer_legend(self):
        self.pursuer_dots.clear()
        for i, pursuer in enumerate(self.simulation.pursuers):
            color = self.get_pursuer_color(pursuer.max_speed)
            dot = self.ax.scatter([], [], c=[color], s=PURSUER_SIZE, label=f'Pursuer {i+1}')
            self.pursuer_dots.append(dot)
        
    def get_pursuer_color(self, speed):
        pursuer_speeds = [p.max_speed for p in self.simulation.pursuers]
        current_min_speed = min(pursuer_speeds)
        current_max_speed = max(pursuer_speeds)
        
        if current_max_speed == current_min_speed:
            normalized_speed = 0.5
        else:
            normalized_speed = (speed - current_min_speed) / (current_max_speed - current_min_speed)
        return self.pursuer_cmap(normalized_speed)

    def update_evader(self):
        evader = self.simulation.evader
        self.evader_dot.set_offsets([evader.position])
        self.evader_text.set_text(f"Evader: Speed={evader.max_speed:.2f}, Acc={evader.acceleration:.2f}, Pos=({evader.position[0]:.1f}, {evader.position[1]:.1f})")
        
    def update_pursuers(self):
        for i, (pursuer, dot) in enumerate(zip(self.simulation.pursuers, self.pursuer_dots)):
            dot.set_offsets([pursuer.position])
            self.pursuer_texts[i].set_text(f"Pursuer {i+1}: Speed={pursuer.max_speed:.2f}, Acc={pursuer.acceleration:.2f}, Pos=({pursuer.position[0]:.1f}, {pursuer.position[1]:.1f})")
        
        # Hide unused pursuer texts
        for i in range(len(self.simulation.pursuers), MAX_PURSUERS):
            self.pursuer_texts[i].set_text('')