"""
This module contains the animate function that updates the animation frame by frame and animate_with_rain which does the same but updates the animation with rain included. 

"""

#Importing modules
import config
import numpy as np
from grid_updater import update_grid, update_grid_with_rain
from resize import enlarge, shrink

def animate(i):
    """
    This function is called for each frame of the animation
    It is where the data of the grid gets updated
    
    Args:
        i: the current frame number
        
    Output:
        grid_plot (numpy_array) : the new grid
        
        line1 (matplotlib.lines.Line2D): Plot point for the graph showing the proportion of trees compared to the grid
        
        line2 (matplotlib.lines.Line2D): Plot point for the graph showing propotion of trees on fire compared to the grid
    """
    #Collect the grid and make this the old one, we need a new one now...
    old_grid = config.grid_plot.get_array().copy()
    #... call the update grid function on this old grid to get our new one!
    new_grid = update_grid(old_grid, i)
    
    
    #This is for the graphing
    #Set the x axis to be the new frame number
    x = np.arange(i + 1)
    #Make the first line (green) on the graph to be the proportion of trees we found in the update grid function against the current frame number
    y = np.array(config.prop_of_trees)
    config.line1.set_data(x, y)
    #Make the second line (red) on the graph to be the proportion of trees on fire we found in the update grid function against the current frame
    z = np.array(config.prop_of_fires)
    config.line2.set_data(x, z)
    
    
    #Set the plot to be this new grid
    config.grid_plot.set_array(new_grid)
    
    #Clear axis of barchart and replot to give dynamic effect
    config.ax3.clear()
    #count_dict - a dictionary to keep track of the relative proportion of tree, fires and empty cell in each frame
    count_dict = {
        'Tree': [config.prop_of_trees[-1], "tab:green"],
        'Fire': [config.prop_of_fires[-1], "tab:red"],
        'Empty': [1 - (config.prop_of_trees[-1] + config.prop_of_fires[-1]), "tab:grey"],
    }
    #Sort dict in descending order for ranking 
    order_dict = sorted(count_dict.items(),key=lambda x:x[1][0],reverse=False)
    #Replot barchart 
    config.ax3.barh([i[0] for i in order_dict], [1, 1, 1], alpha=0)
    config.ax3.barh([i[0] for i in order_dict], [i[1][0] for i in order_dict], color=[i[1][1] for i in order_dict])
    
    #Return the plot for the grid and the lines we need for the graph
    return config.grid_plot, config.line1, config.line2,  

def animate_with_rain(i):
    """
    This function is called for each frame of the animation when including rain 
    It is where the data of the grid gets updated
    
    Args:
        i: the current frame number
        
    Output:
        grid_plot (numpy_array) : the new grid
        
        line1 (matplotlib.lines.Line2D): Plot point for the graph showing the proportion of trees compared to the grid
        
        line2 (matplotlib.lines.Line2D): Plot point for the graph showing the proportion of trees on fire compared to the grid
        
        line3 (matplotlib.lines.Line2D): Plot point for the graph showing the proportion of cells with rain compared to the grid
    """
    
    global big_arr 
    
    # if it's the first frame, we initialise big_arr with the grid plot array
    if i == 0:
        big_arr = config.grid_plot.get_array()
   
    
    
    # shrink our big array to size update grid is expecting (not necessary for the first frame)
    smll_arr = shrink(big_arr)
    
     #... call the update grid function on this old grid to get our new one and to also get a rain_intensity array
    new_smll_arr, rain_intensity = update_grid_with_rain(smll_arr, i) 
    
    # enlarge our array so there are more pixels per cell  
    big_arr = enlarge(new_smll_arr)
    
    # draw rain on our grid 
    big_arr_with_rain = config.weather.add_rain(big_arr, rain_intensity)
    
    #Set the plot to be this new grid with rain
    config.grid_plot.set_array(big_arr_with_rain)
    
    #This is for the graphing
    #Set the x axis to be the new frame number
    x = np.arange(i + 1)
    #Make the first line (green) on the graph to be the proportion of trees we found in the update grid function against the current frame number
    y = np.array(config.prop_of_trees)
    config.line1.set_data(x, y)
    #Make the second line (red) on the graph to be the proportion of trees on fire we found in the update grid function against the current frame
    z = np.array(config.prop_of_fires)
    config.line2.set_data(x, z)
    #Find the proportion of cells that have rain compared to the size of the enlarged grid
    config.prop_of_rain.append(np.sum(big_arr_with_rain == 3)/((config.GRID_HEIGHT * config.BLOCK_SIZE) * (config.GRID_WIDTH * config.BLOCK_SIZE)))
    #Make the third line (blue) on the graph to be the proportion of cells with rain in the update grid function against the current frame
    r = np.array(config.prop_of_rain)
    config.line3.set_data(x, r)
    
    
   
    
    #Clear axis of barchart and replot to give dynamic effect
    config.ax3.clear()
    #count_dict - a dictionary to keep track of the relative proportion of tree, fires and empty cell in each frame
    count_dict = {
        'Tree': [config.prop_of_trees[-1], "tab:green"],
        'Fire': [config.prop_of_fires[-1], "tab:red"],
        'Empty': [1 - (config.prop_of_trees[-1] + config.prop_of_fires[-1]), "tab:grey"],
    }
    #Sort dict in descending order for ranking 
    order_dict = sorted(count_dict.items(),key=lambda x:x[1][0],reverse=False)
    #Replot barchart 
    config.ax3.barh([i[0] for i in order_dict], [1, 1, 1], alpha=0)
    config.ax3.barh([i[0] for i in order_dict], [i[1][0] for i in order_dict], color=[i[1][1] for i in order_dict])
    
    #Return the plot for the grid and the lines we need for the graph
    return config.grid_plot, config.line1, config.line2, config.line3
