import copy
######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

import random
import numpy as np

# These import statements give you access to library functions which you may
# (or may not?) want to use.
from math import *
from glider import *

# If you see (vastly) different scores locally and on Gradescope this may be an indication
# that you are uploading a different file than the one you are executing locally.
# If this local ID doesn't match the ID on Gradescope then you uploaded a different file.
OUTPUT_UNIQUE_FILE_ID = False
if OUTPUT_UNIQUE_FILE_ID:
    import hashlib, pathlib

    file_hash = hashlib.md5(pathlib.Path(__file__).read_bytes()).hexdigest()
    print(f'Unique file ID: {file_hash}')


# This is the function you will have to write for part A.
# -The argument 'height' is a floating point number representing
# the number of meters your glider is above the average surface based upon
# atmospheric pressure. (You can think of this as height above 'sea level'
# except that Mars does not have seas.) Note that this sensor may be
# slightly noisy.
# This number will go down over time as your glider slowly descends.
#
# -The argument 'radar' is a floating point number representing the
# number of meters your glider is above the specific point directly below
# your glider based off of a downward facing radar distance sensor. Note that
# this sensor has random Gaussian noise which is different for each read.

# -The argument 'mapFunc' is a function that takes two parameters (x,y)
# and returns the elevation above "sea level" for that location on the map
# of the area your glider is flying above.  Note that although this function
# accepts floating point numbers, the resolution of your map is 1 meter, so
# that passing in integer locations is reasonable.
#
#
# -The argument OTHER is initially None, but if you return an OTHER from
# this function call, it will be passed back to you the next time it is
# called, so that you can use it to keep track of important information
# over time.
#

# Idea is to first use the particle filter to find out where the glider is approximately
# Once we approximately know where the glider is, we move the glider to land close enough to the origin
# Use a heap to store particles based on initial evaluation to the landmark to the target, then
# use heap to store the particles after weighting and resampling the particles

# I don't know if we should have a particle.z because we can keep track of z in a time loop?

def estimate_next_position(height, radar, mapFunc, OTHER=None):
    """Estimate the next (x,y) position of the glider."""

# initializes particles to random values
    if OTHER is None:
        OTHER = []
        for i in range(50000):
            OTHER.append(glider())
            OTHER[i].x = random.uniform(-250, 250)
            OTHER[i].y = random.uniform(-250, 250)
            OTHER[i].z = random.uniform(4950, 5050)
            OTHER[i].heading = random.gauss(0, pi/4)
    else:
        for particle in OTHER:
            particle.z = height - mapFunc(particle.x, particle.y)
            particle.heading = particle.heading + random.gauss(0, .01)

    elevation = height - radar
    weights = []
    for particle in OTHER:
        weights.append(weighting(particle.x, particle.y, elevation, mapFunc, 50))
    max_weight = maxWeighting(weights)
    OTHER = resample(OTHER, weights, max_weight)
    for i in range(len(OTHER)):
        # fuzzing the particles. "1.0" is a placeholder.
        fuzzing(OTHER[i], 1.2, 1.2, 1.2, 0.01)
    for i in range(len(OTHER)):
        OTHER[i] = OTHER[i].glide()
    # try max weight?
    mean_x = np.mean([p.x for p in OTHER])
    mean_y = np.mean([p.y for p in OTHER])
    xy_estimate = (mean_x, mean_y)

    optionalPointstoPlot = []
    for particle in OTHER:
        optionalPointstoPlot.append((particle.x, particle.y, particle.heading))

    return xy_estimate, OTHER, optionalPointstoPlot

def Gaussian(mu, sigma, x):
    return (1 / (sqrt(2 * pi) * sigma)) * exp(-0.5 * ((x - mu) / sigma) ** 2)

def weighting(x, y, elevation, mapFunc, sigma):
    weight = 1.0
    particle_measurement = mapFunc(x, y)
    weight *= Gaussian(elevation, sigma, particle_measurement)
    return weight

def maxWeighting(weights):
    max_weight = 0.0
    for weight in weights:
        max_weight = max(weight, max_weight)
    return max_weight

def resample(particles, weights, maxWeight):
    resampled = []
    beta = 0
    index = int(random.uniform(0, len(particles)))
    for i in range(2000):
        beta = beta + random.uniform(0, 2 * maxWeight)
        while(weights[index] < beta):
            beta = beta - weights[index]
            index = (index + 1) % len(particles)
        resampled.append(particles[index])
    return resampled

def fuzzing(particle, x_noise, y_noise, z_noise, heading_noise):
    particle.x += random.gauss(0, x_noise)
    particle.y += random.gauss(0, y_noise)
    particle.z += random.gauss(0, z_noise)
    particle.heading += random.gauss(0, heading_noise)


# This is the function you will have to write for part B. The goal in part B
# is to navigate your glider towards (0,0) on the map steering # the glider
# using its rudder. Note that the Z height is unimportant.

#
# The input parameters are exactly the same as for part A.

def next_turn_angle(height, radar, mapFunc, OTHER=None):
    # How far to turn this timestep, limited to +/-  pi/8, zero means no turn.
    steering_angle = 0.0

    # You may optionally also return a list of (x,y)  or (x,y,h) points that
    # you would like the PLOT_PARTICLES=True visualizer to plot.
    #
    # optionalPointsToPlot = [ (1,1), (20,20), (150,150) ]  # Sample plot points
    # return steering_angle, OTHER, optionalPointsToPlot

    return steering_angle, OTHER


def who_am_i():
    # Please specify your GT login ID in the whoami variable (ex: jsmith122).
    whoami = 'cguo309'
    return whoami
