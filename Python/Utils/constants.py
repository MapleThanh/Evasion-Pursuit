# Simulation constants
SIMULATION_WIDTH = 250
SIMULATION_HEIGHT = 250

CAPTURE_DISTANCE = 1.0

# Evader constants
EVADER_RANDOM_MIN_SPEED = 1
EVADER_RANDOM_MAX_SPEED = 1.5

EVADER_ACCELERATION = 0.7

# Pursuer constants
PURSUER_RANDOM_MIN_SPEED = 0.8
PURSUER_RANDOM_MAX_SPEED = 1.7

PURSUER_ACCELERATION = 0.7

# Simulation run constants
MAX_STEPS_PER_EPISODE = 1000

MIN_PURSUERS = 1
MAX_PURSUERS = 3

# Visualization constants
EVADER_SIZE = 100
PURSUER_SIZE = 80

EVADER_COLOR = 'blue'

# Pursuer colors (from lightest to darkest)
PURSUER_COLORS = [
    '#FFEBEE',  # Very light red
    '#FFCDD2',  # Light red
    '#EF9A9A',  # Soft red
    '#E57373',  # Muted red
    '#EF5350',  # Bright red
    '#F44336',  # Standard red
    '#E53935',  # Vibrant red
    '#D32F2F',  # Deep red
    '#C62828',  # Rich red
    '#B71C1C'   # Very deep red
]
ANIMATION_INTERVAL = 10  # milliseconds
