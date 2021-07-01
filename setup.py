"""
In the beginning, we conceived an entire forest that had been struck by lightning and started to catch fire then spread the fire, and soon after some trees had burned out they began to grow.
   So for these variables, we chose three recognizable colors to represent the changes in the forest, with the trees green, the fire red, and the burned-out gray in the animations.
   And then we set the grid_height and grid_width(integer),the probability of tree_growth and lightening(float). The three animations all consist of 100 frames as a loop.
   We put all three of them in the same line. From left to right:
   The subplot1 shows the whole forest animation. 
   The subplot2(line graph) shows the changes for trees and trees got fire. 
   The subplot3(bar chart) shows the density of each variable in the forest.
"""
#Importing modules
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import config
from weather import Weather

def initialise(GRID_HEIGHT = config.GRID_HEIGHT, GRID_WIDTH = config.GRID_WIDTH, lightning = config.lightning, tree_growth = config.tree_growth, istate = config.TREE):
    
    """
    This is the initialize function, it creates the base grids for animation, 3 grids are created - a grid of animation, a line graph and a bar chart
    
    
    Args: 
        GRID_HEIGHT (int): The grid height, default value set in the config
        GRID_WIDTH (int): The grid width, default value set in the config
        lightning (float): The probability that lightning, default value set in the config
        tree_growth (float): The probability that a new tree, default value set in the config
        istate (int): The initial state of cells 
    
    Returns:
        (matplotlib.figure.Figure): The figure instance used for animation
        
    Raises:
        ValueError: if any of the arguments are invalid. Check grid height and length are positive integers and the probability of lightning and new tree growth is between 0 and 1. Also checks if istate is in 0, 1 or 2.
    
    """
    #Checks the parameters are valid for setting up the grid. 
    #Check the grid height and width are positive and porbabilities of lightning and tree growth are between 0 and 1.
    if (GRID_HEIGHT <= 0 or GRID_WIDTH <= 0 or lightning > 1 or lightning < 0  or tree_growth > 1 or tree_growth < 0):
        raise ValueError("Invalid values!")
    #Check the initial state of cells are either 0, 1 or 2
    if(istate not in [0, 1, 2]):
        raise ValueError("Invalid initial state, only accept 0, 1 or 2!")
    
    #Set variables according to user inputs
    config.GRID_HEIGHT = GRID_HEIGHT
    config.GRID_WIDTH = GRID_WIDTH
    config.lightning = lightning
    config.tree_growth = tree_growth
    config.istate = istate

    # Sets up a color map for the figure. Trees are green, red is on fire and gray are empty, burnt out cells.
    cmap = ListedColormap(["tab:green", "tab:red", "tab:gray"])
    
    
    # Create a new figure and the figure size. Sets an id of 1, and figure size of 15 by 5 inches. The constrained layout makes sure the figure fits. This is where both the plots below will sit
    fig = plt.figure(1, constrained_layout=False, figsize = (24, 8))    
    
    ## Add subplot 1. This is forest animation.
    ax1 = fig.add_subplot(131)
    # Turn off axis
    ax1.axis("off")
    
    # #set up a new numpy array of zeros of the grid height and grid width, make sure these zeros are set as integers
    initial_grid = np.full((GRID_HEIGHT, GRID_WIDTH), istate, dtype = int)
    
    #If the initial state is empty, set a random cell to be a tree to avoid triggering the end of the animation
    if(istate == 2):
        #Set a random index 
        index = config.rng.integers(GRID_HEIGHT, size = 2)
        #Change it to list
        index = list(index)
        #Set the variable in config.py
        config.index = index
        #Set the indexed cell to 0
        initial_grid[index[0], index[1]] = 0
    
    # Display grid as an image. Use the color map as described above, the vmin and vmax values make sure the correct colormap values are used.
    config.grid_plot = ax1.imshow(initial_grid, cmap = cmap, vmin = 0, vmax = 2) 
    
    
    ## Add subplot 2. This is the graph animation.
    ax2 = fig.add_subplot(132, xlim=(0, config.frame), ylim=(0, 1)) 
    # Plot number of trees over time. This will be a green line.
    config.line1, = ax2.plot([], [], lw = 4, color = 'tab:green', label = ' Trees') 
    # Plot number of fires over time. This will be a red line.
    config.line2, = ax2.plot([], [], lw = 4, color = 'tab:red', label = 'Fire') 
    # Set x axis label
    ax2.set_xlabel('Frame Number') 
    # Show legend
    ax2.legend() 
    
    #Add subplot 3 for graphing bar chart to figure
    config.ax3 = fig.add_subplot(133, xlim=(0, 1), ylim=(0, 1), xticks=np.arange(0, 1.1, 0.1))
    
    # Hide grid
    plt.close()
    
    
    #return the final figure
    return fig



def init():
    """
   This function will set the grid up for the first display of the animation in the funcanimate function.
    
    Args: 
        NONE
        
    Outputs:
        grid_plot: (matplotlib.image.AxesImage) An image object drawn from numpy array of zeros with shape equal to the GRID_HEIGHT and GRIF_WIDTH
        
        line1: (matplotlib.lines.Line2D) A line object to plot the proportion of trees compared to the size of the grid
        
        line2: (matplotlib.lines.Line2D) A line object to plot the proportion of fire compared to the size of the grid
        
    """
    #set up a new numpy array of zeros with shape = GRID_HEIGHT and GRID_WIDTH set in config module or initialize function, make sure these zeros are set as integers
    grid = np.full((config.GRID_HEIGHT, config.GRID_WIDTH), config.istate, dtype = int)
    
    #If the initial state is empty, set a random cell to be a tree to avoid triggering the end of the animation
    if(config.istate == 2):
        grid[config.index[0], config.index[1]] = 0
        
     #Set the array of grid plot      
    config.grid_plot.set_array(grid)
    
    
    # Set empty list to be filled later for the proportion of trees ...
    config.line1.set_data([], [])
    
    # ... and also for the proportion of fires
    config.line2.set_data([], [])
    
    #return the image object to FuncAnimate 
    return config.grid_plot, config.line1, config.line2

def reset():
    """
    This function resets the variables in the config file to default after every iteration. This makes sure the next run of the simulation starts with the default variables
    
    """
    # Probability of new tree growth and lightning per empty cell is reset to 0.03 for each.
    config.tree_growth = 0.03
    config.lightning = 0.03
    
    
    #Resets both grid height and width to 0 so that they can be reset. This also makes sure the program fails if the new variables are not put in.
    config.GRID_HEIGHT = 0
    config.GRID_WIDTH = 0
    
    #Resets the initial state of cells to 0, start with a grid full of trees
    config.istate = 0
    
    #Reset the graphs
    config.grid_plot = None
    config.line1 = None
    config.line2 = None
    config.line3 = None
    
    # Resets boolean variable to record the first burn out event
    config.first_time = True

    # Reset index to None
    config.index = None
    
    # Lists to store the proportions of trees and fires relative to grid size in each frame for plotting purposes are cleared.
    config.prop_of_trees = []
    config.prop_of_fires = []
    config.prop_of_rain = []

    
    #Frame Number
    config.frame = 100

    # Frame number of the last frame
    config.last_frame = config.frame
    
    #Reset ax3 object
    config.ax3 = None
    
    # Resets weather condition 
    config.weather = None
    
    # Resets the cloud threshold
    config.cloud_th = 0.6
    
    
def initialise_with_rain(GRID_HEIGHT = config.GRID_HEIGHT, GRID_WIDTH = config.GRID_WIDTH, lightning = config.lightning, tree_growth = config.tree_growth, cloud_th = config.cloud_th):
    
    """
    This is the initialize function when adding rain to our animation, it creates the base grids for animation, 3 grids are created - a grid of animation, a line graph, and a bar chart
    
    
    Args: 
        GRID_HEIGHT (int): The grid height, default value set in the config
        GRID_WIDTH (int): The grid width, default value set in the config
        lightning (float): The probability that lightning, default value set in the config
        tree_growth (float): The probability that a new tree, default value set in the config
        cloud_th (float): The number above which becomes a cloud, default value set in the config
    
    Returns:
        (matplotlib.figure.Figure): The figure instance used for animation
        
    Raises:
        ValueError: if any of the arguments are invalid. Check grid height and length are positive integers and the probability of lightning, new tree growth and cloud threshold are between 0 and 1.
    
    """
    
    #Checks the parameters are valid for setting up the grid. 
    #Check the grid height and width are positive and probabilities of lightning and tree growth are between 0 and 1.
    if (GRID_HEIGHT <= 0 or GRID_WIDTH <= 0 or lightning > 1 or lightning < 0  or tree_growth > 1 or tree_growth < 0 or config.cloud_th > 1 or config.cloud_th < 0):
        raise ValueError("Invalid values!")
        
    #Set variables according to user inputs
    config.GRID_HEIGHT = GRID_HEIGHT
    config.GRID_WIDTH = GRID_WIDTH
    config.lightning = lightning
    config.tree_growth = tree_growth
    config.cloud_th = cloud_th
    
    # Initialise the weather class 
    config.weather = Weather(config.cloud_th, config.last_frame, GRID_WIDTH, GRID_HEIGHT)
    

    # Pick color for grid - 'tab:green' for 0, 'tab:red' for 1, 'tab:gray' for 2, '#00008B' is dark blue for 3
    cmap = ListedColormap(["tab:green", "tab:red", "tab:gray", "#00008B"])
    
    
    # Create a new figure and the figure size. Sets an id of 1, and figure size of 15 by 5 inches. The constrained layout makes sure the figure fits. This is where both the plots below will sit
    fig = plt.figure(1, constrained_layout=True, figsize = (15, 5))    
    
    ## Add subplot 1. This is the forest animation.
    ax1 = fig.add_subplot(131)
    # Turn off axis
    ax1.axis("off")
    # #set up a new numpy array of zeros of the grid height and grid width, make sure these zeros are set as intergers
    initial_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype = int) 
    # Display grid as image. Use the colour map as described above, the vmin and vmax values makes sure the correct colourmap values are used.
    config.grid_plot = ax1.imshow(initial_grid, cmap = cmap, vmin = 0, vmax = 3) 
    
    
    ## Add subplot 2. This is the graph animation.
    ax2 = fig.add_subplot(132, xlim=(0, config.frame), ylim=(0, 1)) 
    # Plot number of trees over time. This will be a green line.
    config.line1, = ax2.plot([], [], lw = 4, color = 'tab:green', label = ' Trees') 
    # Plot number of fires over time. This will be a red line.
    config.line2, = ax2.plot([], [], lw = 4, color = 'tab:red', label = 'Fire')
    # Plot percentage of rain over time. This will be a blue line.
    config.line3, = ax2.plot([], [], lw = 4, color = 'tab:blue', label = 'Rain') 
    # Set x axis label
    ax2.set_xlabel('Frame Number') 
    # Show legend
    ax2.legend() 
    
    #Add subplot 3 for graphing barchart to figure
    config.ax3 = fig.add_subplot(133, xlim=(0, 1), ylim=(0, 1), xticks=np.arange(0, 1.1, 0.1))
    
    
    # Hide grid
    plt.close()
    
    #return the final figure
    return fig
