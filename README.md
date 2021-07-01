# FIRE!! - A Forest Fire Simulation with Cellular Automata

To view the simulations, go to Forest_Fire_Model.ipynb.
To implement the project, keep reading!

## Table of Contents
1. [Introduction](#Introduction)
2. [Requirements](#Requirements)
3. [Getting Started](#Getting-Started)
4. [Authors](#Authors)

## INTRODUCTION
The objective of this project is to model the propagation and extinguishing of fire in a forest. Here we apply cellular automata to predict the temporal and spatial effect four factors have on forest fire dynamics.

## Requirements

### Basics
- **Python 3.x:** To download the latest version of Python 3, please visit [Python website](https://www.python.org/downloads/).
- **Jupyter Notebook:** Jupyter notebook can be easily accessed through [Anaconda](https://www.anaconda.com/products/individual#Downloads).

### Libraries
The following libraries are required to run the simulation. Please make sure they are installed before trying to run the program.
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [pytest](https://docs.pytest.org/en/latest/)
- [IPython](http://ipython.org/)
- [Pandas](https://pandas.pydata.org/)
- [PerlinNoise](https://pypi.org/project/perlin-noise/)
- [cv2](https://pypi.org/project/opencv-python/)

The general format to install Python packages 
```
pip install -r requirements.txt
```

### Modules

Please make sure the following modules are in the same directory as the forest_fire.ipynb Jupyter Notebook file.

|Module names  | Function                | Description 									   							                    						       | Module imported by |
| ------------ | ---------------         |--------------																	    						       |------------|
|animation     | `animate`               | Called by `FuncAnimation`, control the animation by updating the grid each frame 									    						       | Forest_fire.ipynb, simulation |
|animation     | `animate_with_rain`     | Called by `FuncAnimation`, control the animation by updating the grid each frame, called instead of animate when rain is a parameter 		   						       | Forest_fire.ipynb, simulation |
|config        | *NA*                    | Contains all the variables needed to run the simulation 												    						       | Forest_fire.ipynb, animation, grid_updater, setup, simulation, test_neighbour |
|grid_updater  | `spread_fire` 		 | Called by `update_grid` function, spread fire to neighbours 												    						       | animation |
|grid_updater  | `update_grid`		 | Called by `animate` function, Changes the states of each cell on the grid based on probabilities 							    						       | animation |
|grid_updater  | `update_grid_with_rain` | Called by `animate` function, Changes the states of each cell on the grid based on probabilities, called instead of update_grid when rain is a parameter 						       | animation |
|setup         | `initialise` 		 | Initialize the base grids needed for animation, also allow users to set the values of parameters to model different forest fire conditions 		    						       | Forest_fire.ipynb, simulation |
|setup         | `initialise_with_rain`  | Initialize the base grids needed for animation, also allow users to set the values of parameters to model different forest fire conditions, used instead of initialise when rain is included as a parameter | Forest_fire.ipynb, simulation |
|setup         | `init` 		 | Called by `FuncAnimation`, setup the first frame of animation 											    			    			       | Forest_fire.ipynb, simulation |
|setup         | `reset` 		 | Resets the variables to default in config files after every iteration the model is run 								    						       | Forest_fire.ipynb, simulation |
|sims          | `simulation` 		 | Repeat forest fire simulation for a parameter over specified values for specified number of times 						    							       | Forest_fire.ipynb |
|sims          | `sim_plot` 		 | Used after `simulation` function to plot simulation results as graphs 										    						       | Forest_fire.ipynb |
|sims          | `simulation_combine` 	 | Runs simulation for combination of lightning and tree growth probabilities 										    						       | Forest_fire.ipynb |
|test_neighbour| `test_spread_fire` 	 | A test function to test the `spread_fire` function, can be invoked by calling `pytest` in terminal 						            						       | *NA* |
|resize        | `shrink` 		 | Called by `animate_with_rain` function, shrinks the size of a grid to the size `update_grid` is expecting 						    						       | animation, weather |
|resize        | `enlarge` 		 | Called by `animate_with_rain` function, enlarges the size of a grid to allow rain to be visualised in multiple pixels per cell 			    						       | animation, weather |
|weather       | `generate_random_wind`  | Called by the `Weather` class upon initialisation, selects a random wind direction that the rain clouds will travel in each animation 		    						       |  setup |
|weather       | `generate_random_clouds`| Called by the `update_grid_with_rain` function, sets up where it is raining on the grid each frame 							    						       |  setup |
|weather       | `add_rain`		 | Called by the `animate_with_rain` function, draws blue rain clouds onto the grid 									    						       |  setup |


## Getting Started

Forest_fire.ipynb is the main file you will work with, it calls all the necessary dependencies (i.e. libraries, modules) in the beginning. Run the three code cells in section "2. Building the model" for a demonstration of this model and the first in "3. Simulation of parameters" to run the simulations. 
Run the two code cells at the beginning of section "8. Rainfall" for a demonstration of this model with the added parameter of rain. 

# Authors: 
- Russell Hung, Ellie Carr, Emily Cryer and Boshen Cai
- We are MSc Bioinformatics students at the University of Bristol, Year 2020 - 2021

