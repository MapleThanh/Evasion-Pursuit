import random
import numpy as np
from constants import *

def get_random_evader_speed(min_speed, max_speed):
    return random.uniform(min_speed, max_speed)

def get_random_pursuer_speed(min_speed, max_speed):
    return random.uniform(min_speed, max_speed)

def get_random_evader_position(width, height):
    return np.array([random.uniform(0, width), random.uniform(0, height)])

def get_random_pursuer_position(width, height):
    return np.array([random.uniform(0, width), random.uniform(0, height)])

def get_random_pursuer_count(min, max):
    return random.randint(min, max)

def get_random_boolean(probability=0.5):
    return random.random() < probability

def get_random_gaussian(mean, std_dev):
    return random.gauss(mean, std_dev)
