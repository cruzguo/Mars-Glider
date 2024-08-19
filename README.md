**Project Description**
The Mars Glider project simulates a glider navigating the Martian surface. The glider receives noisy sensor data including altitude and radar distance to the ground. The goal is to estimate the glider's position and navigate it towards a target position on the map.

**Key Objectives**
Estimate the Glider's Position: Implement a particle filter to estimate the glider's position based on noisy sensor measurements.
**Navigate the Glider:** Implement a control strategy to steer the glider towards (0,0) using calculated steering angles.
Files
**marsglider.py:** Contains the implementation of the particle filter and navigation functions. This is the primary file for the project.
**glider.py:** Contains the simulation of the glider. Do not modify this file but use it to understand the glider's behavior.
**opensimplex.py:** Provides a function to generate the Martian surface map. Do not modify this file.
generate_params_marsglider.py: (Optional) Use this script to generate additional test cases for testing your implementation.
**Functions**
estimate_next_position(height, radar, mapFunc, OTHER=None)
Estimates the next (x, y) position of the glider using a particle filter.

**Parameters:**

**height:** The barometric height of the glider above sea level (with noise).
**radar:** The distance from the glider to the ground (with noise).
**mapFunc:** A function that returns the elevation of the ground at a specific (x, y) location.
**OTHER:** An optional parameter for passing and storing particle filter state between calls.
**Returns:**

(xy_estimate, OTHER, optional_points_to_plot): The estimated position, updated particle filter state, and optional points for visualization.
next_turn_angle(height, radar, mapFunc, OTHER=None)
Determines the turn angle needed to navigate the glider towards (0,0).

**Parameters:**

**height:** The barometric height of the glider above sea level (with noise).
**radar:** The distance from the glider to the ground (with noise).
**mapFunc:** A function that returns the elevation of the ground at a specific (x, y) location.
**OTHER:** An optional parameter for passing and storing particle filter state between calls.
**Returns:**

**steering_angle:** The angle to turn the glider to steer it towards the target (0,0).
**OTHER:** The updated particle filter state.
