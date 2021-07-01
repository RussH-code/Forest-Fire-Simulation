from numpy.random import default_rng

########## Variables ##############

## Setting up the variables for animations

# Probability of new tree growth and lightning per empty cell
tree_growth = 0.03
lightning = 0.03

#Keep rain and rain intensity = 0 when running the simulation for other parameters


#Default grid size is 10x10
GRID_WIDTH = 10
GRID_HEIGHT = 10

TILE_SIZE = 10 # Number of blocks per cell
BLOCK_SIZE = 5 # Number of pixels per block

grid_plot = None
line1 = None
line2 = None
line3 = None

### TILE STATES 
## 3 states - tree (0), fire (1), and burnt (2) for each tile represented by a number
TREE = 0
FIRE = 1
BURNT = 2

# Boolean variable to record the first burn out event
first_time = True

# Random number generator
rng = default_rng()

# Lists to store the proportions of trees and fires relative to grid size in each frame for plotting purposes
prop_of_trees = []
prop_of_fires = []
prop_of_rain = []

#Frame Number
frame = 100

# Frame number of the last frame
last_frame = frame

#Tree index for an empty plot
index = None

#axis 3 dynamic bar chart
ax3 = None

# will be used to store the weather class 
weather = None
# the cloud threshold, used when rain is added in the animation
cloud_th = 0.6
