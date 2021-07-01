"""
This module contains functions that change the grid animation according to rules and probabilities that grow and burn trees. 

"""
#Importing modules
import config
import numpy as np

def spread_fire(grid, width, height):
    """
    This function makes sure the burning cell spreads to all 8 of its neighbours, except when it borders with edges.
    
    Args:
        grid (numpy array) : the grid that the last frame ended on
        width (int) : the width of the grid
        height (int): the height of the grid
    
    Output:
        grid_copy (numpy array): the new grid ready for the rest of the update grid function. 
        
    Example:
        >>> spread_fire(np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]))
        np.array([[2, 1, 0], [1, 1, 0], [0, 0, 0]])
    """
    #make a copy of the previous grid
    grid_copy = grid.copy()
    
    #Directions to map neighbouring cells
    neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
    
    #Iterate over every cell in the grid by rows and columns
    for x in range(width):
        for y in range(height):
            
            #check if a fire is present
            if grid[y,x] == config.FIRE:
                
                #If fire is present, iterate over its neighbours
                for (dy,dx) in (neighbourhood):
                    
                    #If neighbours are not edges and are trees, change them to be on fire
                    if (y + dy < height and y + dy >= 0 and x + dx < width and x + dx >= 0 and grid[(y + dy),(x + dx)] == config.TREE):
                        grid_copy[(y + dy),(x + dx)] = config.FIRE
                        
                        
                # The original cell that is on fire will become burnt
                grid_copy[y,x] = config.BURNT
                
    #Return the updated grid
    return grid_copy

#Changes to the grid(e.g. fire, tree growth...)
def update_grid(grid, frame_num):
    """
    This is the function that changes the grid each time-dependent on probabilities and the previous grid
    
    Args: 
        grid (numpy array): The grid from the previous frame (or initialise function)
        
        frame_num: The current frame number
        
    Output: grid (numpy array): The new grid for this frame
    """
    #Copy the grid from the previous frame to work on and become the new frame.    
    grid = grid.copy()
    
    #Set the size of the grid to be the height of the grid times the width.
    size = config.GRID_HEIGHT*config.GRID_WIDTH
    
    #Spread the fire to all the neighbours of a cell if it is on fire.
    grid = spread_fire(grid, config.GRID_HEIGHT, config.GRID_WIDTH)
    
    #Lightning strike!
    #Calculate random floats between 0 and 1 and compare these to the probability of lightning set in the beginning.
    #This returns a grid of boolean values the same size of the grid.
    lightning_prob = config.rng.random(size = size).reshape(config.GRID_HEIGHT, config.GRID_WIDTH) > (1-config.lightning)
        #If at any point the boolean value is true and in the subsequent space in the grid, there is not an on-fire or burnt-out tree- set it on fire!
    grid[(lightning_prob == True) & (grid == config.TREE)] = config.FIRE
    
    #New tree spawns!
    #Calculate random floats between 0 and 1 and compare these to the probability of a new tree growing set in the beginning.
    #This returns a grid of boolean values the same size of the grid.
    new_tree_prob = config.rng.random(size = size).reshape(config.GRID_HEIGHT, config.GRID_WIDTH) > (1-config.tree_growth) 
    #If at any point the boolean value is true and in the subsequent space in the grid there is a burnt out tree- grow a new tree!
    grid[(new_tree_prob == True) & (grid == config.BURNT)] = config.TREE
    
    
    #These are used to plot the graph as the animation goes on
    #Find the proportion of trees that are still alive compared to the size of the grid
    config.prop_of_trees.append(np.sum(grid == 0)/size)
    #Find the proportion of trees that are on fire compared to the size of the grid
    config.prop_of_fires.append(np.sum(grid == 1)/size)
    
    
    #Stop animation if all cells are burnt
    #Take an average of the status of all the trees (if it is less than 2 some trees must still be alive or on fire)
    trees = grid.mean(dtype = int)
    
    #Check if all the trees are burnt out and if it is the first time...
    if (trees == 2 and config.first_time == True):
        
        #Set the last_frame = frame number when the first burn out event occurs
        config.last_frame = frame_num
        
        #Set first time to false to prevent overwriting last_frame variable 
        config.first_time = False
        
    #return the new grid so the function may continue     
    return grid

def update_grid_with_rain(grid, frame_num):
    """
    This is the function that changes the grid each time dependent on probabilities and the previous grid.
    It is the same as update_grid but with rain. 
    
    Args: 
        grid (numpy array): The grid from the previous frame (or initialise function)
        
        frame_num: The current frame number
        
    Output: grid (numpy array): The new grid for this frame
    """
    #Copy the grid from the previous frame to work on and become the new frame.    
    grid = grid.copy()
    
    #Set the size of the grid to be the height of the grid times the width.
    size = config.GRID_HEIGHT*config.GRID_WIDTH
    
    ## Rainfall!
    # generate where it's raining on the grid for this frame
    rain_intensity = config.weather.generate_rain_clouds(frame_num)
    
    
    # the rain intensity increases tree growth and reduces fire chance
    # tree growth and lightning are normal (config) values where there are no clouds
    new_tree_growth_arr = config.tree_growth * (1 + rain_intensity)
    new_lightning_prob_arr = config.lightning * (1 - rain_intensity)
    
    #Spread the fire to all the neighbours of a cell if it is on fire.
    grid = spread_fire(grid, config.GRID_HEIGHT, config.GRID_WIDTH)
    
    #Lightning strike!
    #Calculate random floats between 0 and 1 and compare these to the probability of lightning set in the beginning.
    #This returns a grid of boolean values the same size of the grid.
    lightning_prob = config.rng.random(size = size).reshape(config.GRID_HEIGHT, config.GRID_WIDTH) > (1-new_lightning_prob_arr)
        #If at any point the boolean value is true and in the subsequent space in the grid, there is not an on-fire or burnt out a tree- set it on fire!
    grid[(lightning_prob == True) & (grid == config.TREE)] = config.FIRE
    
    #New tree spawns!
    #Calculate random floats between 0 and 1 and compare these to the probability of a new tree growing set in the beginning.
    #This returns a grid of boolean values the same size of the grid.
    new_tree_prob = config.rng.random(size = size).reshape(config.GRID_HEIGHT, config.GRID_WIDTH) > (1-new_tree_growth_arr) 
    #If at any point the boolean value is true and in the subsequent space in the grid, there is a burnt-out tree- grow a new tree!
    grid[(new_tree_prob == True) & (grid == config.BURNT)] = config.TREE
    
    
    #These are used to plot the graph as the animation goes on
    #Find the proportion of trees that are still alive compared to the size of the grid
    config.prop_of_trees.append(np.sum(grid == 0)/size)
    #Find the proportion of trees that are on fire compared to the size of the grid
    config.prop_of_fires.append(np.sum(grid == 1)/size)
    
    
    
    #Stop animation if all cells are burnt
    #Take an average of the status of all the trees (if it is less than 2 some trees must still be alive or on fire)
    trees = grid.mean(dtype = int)
    #Check if all the trees are burnt out and if it is the first time...
    if (trees == 2 and config.first_time == True):
        
        #Set the last_frame = frame number when first burn out event occurs
        config.last_frame = frame_num
        
        #Set first time to false to prevent overwriting last_frame variable 
        config.first_time = False
        
    #return the new grid so the function may continue and the rain intensity array to use to generate rain in animate   
    return grid, rain_intensity
