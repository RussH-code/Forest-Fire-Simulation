"""
This module contains: simulation(), simulation_combine() and sim_plot(). The simulation and simulation_combine functions run the forest fire simulation. The simulation function only changes one parameter at a time, this is useful for studying the effect of one parameter on the function. The simulation_combine function can take values to change both the lightning and new tree growth probabilities, this is useful for looking at the effect of changing both these parameters. The sim_plot is used for creating graphs of these simulations: a line graph showing the changing proportion of trees on fire and alive trees, and a dynamic bar chart representing the number of cells in the grid that are empty, on fire or alive.
"""

#Import all the needed modules
from animation import animate, animate_with_rain
from setup import initialise, init, reset, initialise_with_rain
import config

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def simulation(parameter, sim_values, times = 1, GRID_HEIGHT = config.GRID_HEIGHT, GRID_WIDTH = config.GRID_WIDTH, lightning = config.lightning, tree_growth = config.tree_growth, frame_num = config.frame, cloud_th = config.cloud_th, rain = False):
    """
    Runs forest fire simulation for a parameter over the specified values for specified number of times.
    Note: the parameters that are not changed will be run as specified in config.py so this should be checked before running
    
    Args:
    
        parameter : (int) the parameter to be changed in the simulation
                    0 = tree_growth
                    1 = lightning
                    2 = GRID_HEIGHT and GRID_WIDTH
                    3 = rain
        
        sim_values : (numpy ndarray) a 1D array corresponding to the probabilities/values of the parameter(s) to be used in simulation
        
        times : (int) number of times to repeat the simulation, defaults to 10
        
        GRID_HEIGHT (int): The grid height, default value set in the config
        GRID_WIDTH (int): The grid width, default value set in the config
        lightning (float): The probability that lightning, default value set in the config
        tree_growth (float): The probability that a new tree, default value set in the config
        frame_num (int): The number of frames to run the simulation 
        rain (boolean): If true, the simulation will be run with the effect of rain, defaults to false
    
    Returns:
    
        mean_remaining_trees : (list) a list of floats containing the mean values of the remaining number of trees 
                                 one mean value is returned for each value in sim_values
        
        mean_last_frame : (list) a list of floats containing the mean values of the last frame number 
                            one mean value is returned for each value in sim_values
                            
    Raises:
    
        ValueError: If any of the arguments are of the correct type but not a valid value
        
        TypeError: If any of the arguments are not of the correct data type
    
    """
    #Checks the number of the times argument is above 0
    if times <= 0:
        raise ValueError("Number of times must be at least 1!")
        
    #Checks the simulation values are stored in a numpy array
    elif (type(sim_values) != np.ndarray):
        raise TypeError("Invalid simulation value type, only accepts 1D numpy array!")
        
    #Checks there is at least one value in the values for the testing
    elif (sim_values.size <= 0 ):
        raise ValueError("Must have at least one value in simualation values!")
        
    #Checks the paramater value is valid (either 0, 1, 2 or 3)    
    elif (parameter > 3 or parameter < 0):
        raise ValueError("Invalid parameter values, see documentation.")
        
    #Check the grid height and width are positive and probabilities of lightning and tree growth are between 0 and 1.
    elif (GRID_HEIGHT <= 0 or GRID_WIDTH <= 0 or lightning > 1 or lightning < 0  or tree_growth > 1 or tree_growth < 0):
        raise ValueError("Invalid values!")
        
    #If parameter is 3 (simulating rain) and rain is false, raises an error, 
    elif (parameter == 3 and rain == False):
        raise ValueError("Conflicting rain argument!")
        
    #If the frame number is smaller than 1, raise an error
    elif(frame_num < 1):
        raise ValueError("Invalid frame number, frame number must be at least 1!")
    
    #Creates two empty arrays
    #This first array will store the proportion of the grid that are still alive trees for each value in the parameter. A mean is taken for
    #each value.
    mean_remaining_trees = [] 
    #This array will store the value of the last frame. This is either the frame the simulation has burnt out at or the max frame number as
    #previously set. A mean is taken for each value.
    mean_last_frame = []
    
    #Iterate over each value in the simulation values so each one is tested.
    for param in list(sim_values):
        
        #Set empty list for this value
        #This array will store the proportion of the grid that are still trees in each simulation for one value when the simulation has
        #ended. This can either be ending by the grid burning out or the max number of frames is reached.
        remaining_trees_per_sim = []  
        #This array will store the number of the last frame that the simulation ends on. This can either be when the simulation burns out
        #or when the max number of frames has ended.
        last_frame_per_sim = [] 

        #Repeat this simulation the number of times set as specified in the "times" argument
        for time in range(times):
            
            #Reset the variables in config.py
            reset() 
            
            #Change the frame number and last_frame in config.py    
            config.frame = frame_num
            config.last_frame = frame_num

            #If rain effect is not activated
            if(rain == False):

                #Checks which parameter is to be tested and sets the appropriate parameter.
                #If it is 0: in the initialize function set tree growth to be the value in the list
                if (parameter == 0):
                    fig = initialise(tree_growth = param, GRID_HEIGHT = GRID_HEIGHT, GRID_WIDTH = GRID_WIDTH, lightning = lightning)

                #If it is 1: in the initialize function set to lightning to be the value in the list
                elif (parameter == 1):
                    fig = initialise(lightning = param, GRID_HEIGHT = GRID_HEIGHT, GRID_WIDTH = GRID_WIDTH, tree_growth = tree_growth)

                #If it is 2: in the initialize function set it to grid height and width
                #Note: as this grid is a square only one value is used for both grid height, grid width
                elif (parameter == 2):
                    fig = initialise(GRID_HEIGHT = param, GRID_WIDTH = param, lightning = lightning, tree_growth = tree_growth)
            
                #Run the FuncAnimation function from the MatPlot Library (see packages imported) using the appropriate parameters
                #Fig makes sure the output is placed in a figure
                #animate_with_rain calls the animate_with_rain function (see modules imported)
                #the number of frames is set to the value declared in the config module
                #Interval of 1 to proceed through the animation faster
                #The init function (see the init module) is called first to set up the plot.
                anim = FuncAnimation(fig, animate, frames=config.frame, interval=1, init_func = init)
                #Display this in HTML
                HTML(anim.to_jshtml())
            
            #If rain is in effect
            else:
                
                #Checks which parameter is to be tested and sets the appropriate parameter.
                #If it is 0: in the initialize function set tree growth to be the value in the list
                if (parameter == 0):
                    fig = initialise_with_rain(tree_growth = param, GRID_HEIGHT = GRID_HEIGHT, GRID_WIDTH = GRID_WIDTH, lightning = lightning, cloud_th = cloud_th)

                #If it is 1: in the initialize function set to lightning to be the value in the list
                elif (parameter == 1):
                    fig = initialise_with_rain(lightning = param, GRID_HEIGHT = GRID_HEIGHT, GRID_WIDTH = GRID_WIDTH, tree_growth = tree_growth, cloud_th = cloud_th)

                #If it is 2: in the initialize function set it to grid height and width
                #Note: as this grid is a square only one value is used for both grid height, grid width
                elif (parameter == 2):
                    fig = initialise_with_rain(GRID_HEIGHT = param, GRID_WIDTH = param, lightning = lightning, tree_growth = tree_growth, cloud_th = cloud_th)
            
                #If it is 3 set it to cloud threshold 
                elif (parameter == 3):
                    fig = initialise_with_rain(cloud_th = 1-param, GRID_HEIGHT = GRID_HEIGHT, GRID_WIDTH = GRID_WIDTH, lightning = lightning, tree_growth = tree_growth)
                # we do 1 minus the cloud threshold so we can plot the rain probability and the trend is easier to interoperate
                #Run the FuncAnimation function from the MatPlot Library (see packages imported) using the appropriate parameters
                #Fig makes sure the output is placed in a figure
                #animate calls the animate function (see modules imported)
                #the number of frames is set to the value declared in the config module
                #Interval of 1 to proceed through the animation faster
                #The init function (see the init module) is called first to set up the plot.
                anim = FuncAnimation(fig, animate_with_rain, frames=config.frame, interval=1, init_func = init)
                #Display this in HTML
                HTML(anim.to_jshtml())
            
            #Set the remaining trees to be the proportion of alive trees in the last frame. This value is appended to the array storing the
            #number of remaining trees in the simulations
            remaining_trees_per_sim.append(config.prop_of_trees[-1])
            #Set the last frame in a simulation and add this to the array storing number of the last frames.
            last_frame_per_sim.append(config.last_frame)
        
        #There is now an array for one value in the parameter list. A mean of each list is then taken to find the mean number of trees 
        #remaining and mean value for the last frame. This value is then appended to the arrays containing the mean for each value.
        mean_remaining_trees.append(np.mean(np.array(remaining_trees_per_sim)))
        mean_last_frame.append(np.mean(np.array(last_frame_per_sim)))
    

    #Return the mean remaining tree number and mean last frame lists.
    return mean_remaining_trees, mean_last_frame





def simulation_combine(light_values, tree_values, times = 1, frame_num = config.frame):
    """
    Runs forest fire simulation over specified values for the specified number of times. Each lightning probability is tested against each new
    tree value for the number of times specified.
    
    Args:
    
        light_values : (numpy ndarray) a 1D array corresponding to the probabilities/values of lightning to be used in the simulation
        
        tree_values : (numpy ndarray) a 1D array corresponding to the probabilities/values of new tree growth to be used in the simulation
        
        times : (int) number of times to repeat the simulation, defaults to 10
        
        frame_num (int): The number of frames to run simulation 
    
    Returns:
    
        mean_remaining_trees : (list) a list of floats containing the mean values of the remaining number of trees 
                                 one mean value is returned for each value combination of lightning values and new tree values
        
        mean_last_frame : (list) a list of floats containing the mean values of the last frame number 
                            one mean value is returned for each value combination of lightning values and new tree values
                 
        condition: (list) a list of pairs of values representing the lightning and new tree probabilities used as (lightning, new tree)
                            
    Raises:
    
        ValueError: If any of the arguments are of the correct type but not a valid value
        
        TypeError: If any of the arguments are not of the correct data type
    
    """
    
    #Checks the number of the times argument is above 0
    if times <= 0:
        raise ValueError("Number of times must be at least 1!")
        
    #Checks the simulation values are stored in a numpy array
    elif (type(light_values) != np.ndarray):
        raise TypeError("Invalid simulation value type, only accepts 1D numpy array!")
        
    #Checks there is at least one value in the values for the testing
    elif (light_values.size <= 0 ):
        raise ValueError("Must have at least one value in simualation values!")
        
    #Checks the simulation values are stored in a numpy array
    elif (type(tree_values) != np.ndarray):
        raise TypeError("Invalid simulation value type, only accepts 1D numpy array!")
        
    #Checks there is at least one value in the values for the testing
    elif (tree_values.size <= 0 ):
        raise ValueError("Must have at least one value in simualation values!")
    
    #If the frame number is smaller than 1, raise an error
    elif(frame_num < 1):
        raise ValueError("Invalid frame number, frame number must be at least 1!")
        
    
    #Creates two empty arrays
    #This first array will store the proportion of the grid that are still alive trees for each value in parameter. A mean is taken for
    #each value.
    mean_remaining_trees = [] 
    #This array will store the value of the last frame. This is either the frame the simulation has burnt out at or the max frame number as
    #previously set. A mean is taken for each value.
    mean_last_frame = []
    #This array will store each condition for tabulating and visualising the data.
    condition = []
    
    
    #Iterate over each value in the simulation values so each one is tested.
    for lightning_value in list(light_values):
        #for each value in the lightning list iterate over the new tree probability list and test each one.
        for tree_value in list(tree_values):
        
            #Set empty list for this value
            remaining_trees_per_sim = []  
            last_frame_per_sim = [] 
                    
            #Repeat this simulation the number of times set as specified in the "times" argument
            for time in range(times):
            
                #Reset the variables in config.py
                reset()             
                
                #Change the frame number in config.py    
                config.frame = frame_num 
                config.last_frame = frame_num
            
                #Set the probabilities of new tree growth and lightning to be the values specified in the lists using the initialize
                #function (see the initialize module)
                fig = initialise(tree_growth = tree_value, lightning = lightning_value)
                
            
                #Run the FuncAnimation function from the MatPlot Library (see packages imported) using the appropriate parameters
                #Fig makes sure the output is placed in a figure
                #animate calls the animate function (see modules imported)
                #the number of frames is set to the value declared in config module
                #Interval of 1 to proceed through the animation faster
                #The init function (see the init module) is called first to set up the plot.
                anim = FuncAnimation(fig, animate, frames=config.frame, interval=1, init_func = init)
                #Display this in HTML so can be displayed in a Jupiter Notebook
                HTML(anim.to_jshtml())
            
            
                #Set the remaining trees to be the proportion of alive trees in the last frame. This value is appended to the array storing
                #the number of remaining of trees in the simulations
                remaining_trees_per_sim.append(config.prop_of_trees[-1])
                #Set the last frame in a simulation and add this to the array storing number of the last frames.
                last_frame_per_sim.append(config.last_frame)
                
                
                
            #There is now an array for set of conditions. A mean of each list is then taken to find the mean number of trees 
            #remaining and mean value for the last frame. This value is then appended to the arrays containing the mean for each value.
            mean_remaining_trees.append(np.mean(np.array(remaining_trees_per_sim)))
            mean_last_frame.append(np.mean(np.array(last_frame_per_sim)))
            #The condition tested is then appended to the list of conditions
            condition.append((lightning_value, tree_value))
    
    
    #Return the mean remaining tree number, mean last frame and conditions
    return mean_remaining_trees, mean_last_frame, condition




def sim_plot(sim_values, rem_trees, last_frame, x_axis):
    """
    This function plots the proportion of trees in the last frame and the number of frames in the simulation and is used after the simulation function to visualise the results.
    
    Args: 
        sim_values: (numpy ndarray) a 1D array corresponding to the probabilities/values of the parameter(s) to be used in simulation
        
        rem_trees: (list) a list of floats containing the mean values of the remaining number of trees
        
        last_frame: (list) a list of floats containing the mean values of the last frame number
        
        x_axis: (string) label for the x axis of the plot
        
    
    Raises:
        Type Error: An incorrect data type is passed into the parameters, simulation values must be added as a numpy array.
        
        Value Error: The lists or array are not the same length and so could not be plotted together.
        
    """
    
    #Checks that the simulation values are in a numpy array
    if (type(sim_values) != np.ndarray):
        raise TypeError("Invalid simulation value type, only accepts 1D numpy array!")
        
    #Checks all arguments are of the same length and so can be plotted together
    elif (sim_values.size != len(rem_trees) or sim_values.size != len(last_frame)):
        raise ValueError("Arguments are of differen size/lengths!")
    
    
    #Creates two subplots and sets the figure size to be 12x5
    size_sim, axes = plt.subplots(1, 2, sharex = True, figsize = (12, 5))
    
    #For the first plot:
    #Plot the simulation values against the list of values contaning the remaining trees
    axes[0].plot(list(sim_values), rem_trees)
    #Add a title to the plot
    axes[0].set_title("No. of remaining trees in last frame")
    #Set the y axis label
    axes[0].set_ylabel("Proportion of trees")
    
    #For the second plot:
    #Plot the simulation values against the list of values containing the last frame numbers
    axes[1].plot(list(sim_values), last_frame)
    #Add a title to the plot
    axes[1].set_title("No. of frames in simulation")
    #Set the y axis label
    axes[1].set_ylabel("Frame number")
    
    #Add an x axis label for the simulation values and set this at the bottom of the plot in the center
    size_sim.text(0.5, 0.04, x_axis, ha='center')
    
    
    #Display the plot
    plt.show()
