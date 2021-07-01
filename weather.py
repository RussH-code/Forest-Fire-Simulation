"""
This module contains the Weather class which sets up where on the grid it is raining,
the wind direction in which the rain clouds are traveling and then draws the rain onto the grid plot. 
To get around the problem of circular imports, the object 'weather' is created in config such that weather attributes are accessed via calling config.weather,  which circumvents the need to import weather into many modules. 
"""

from resize import enlarge, shrink
from perlin_noise import PerlinNoise
import numpy as np
import cv2


class Weather: 
    def __init__(self, cloud_th, max_iterations, grid_width, grid_height):
        # perlin noise is an algorithm for generating random numbers in clusters that change gradually, creating 'smooth' trasitions between high and low  points, so is ideal for generating clouds! 
        self.noise = PerlinNoise(octaves=5)
        # Our rain cloud is just a 2d grid like our world grid.
        # It will be much bigger than the world grid but we will only show a small 'window' of it over the top of our world grid.
        # The rain window moves on each iteration, in the direction of the wind. Making it look like a rain cloud is moving across the word.
        # We generate a random wind direction to know which way the rain cloud will move across the grid
        self.wind = self.generate_random_wind()
        # the cloud threshold is the number above which the rain noise becomes a cloud, as it increases there is less chance for rain
        self.cloud_th = cloud_th
        # we need to know the max iterations so we can create a rain cloud big enough to move across the world constantly.
        self.max_iterations = max_iterations
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        # initialise the rain grid
        
        rain_grid_width, rain_grid_height = self.grid_width + 2 * self.max_iterations, self.grid_height + 2 * self.max_iterations
        # create the random rain grid
        self.rain_noise = np.array([[self.noise([i / rain_grid_width, j / rain_grid_height]) for j in range(rain_grid_width)] for i in range(rain_grid_height)])
        # normalise the random numbers in the rain grid.
        self.rain_noise = (self.rain_noise + (0 - self.rain_noise.min())) * (1 / (np.abs(self.rain_noise.max() - self.rain_noise.min())))
        # set everything in the rain grid to zero if it's lower than the threshold
        self.rain_noise[self.rain_noise < self.cloud_th] = 0
        
    def generate_random_wind(self):
        """
        This function selects a random wind direction. 

        Returns:
            (numpy array): a random wind direction 

        """
        #specifiy all the directions
        wind_direction = np.array([[ 1, 0],
                            [-1, 0],
                            [ 0, 1],
                            [ 0,-1],
                            [-1, -1],
                            [-1, 1],
                            [1, 1], 
                            [1, -1]])
        #choose one randomly, this will stay the same for the whole animation
        index = np.random.choice(wind_direction.shape[0], 1, replace=False)
        wind_random = wind_direction[index]
        return wind_random

    def generate_rain_clouds(self, frame_num):
        """
        This function creates instances of rain clouds.

        Args: 
            frame_num (int): The current frame number

        Returns:
            (numpy array): a grid of rain intensity values that complements each cell on our grid plot 

        """
        #will update every frame to move the rain noise grid in the direction of the wind
        arr = self.rain_noise[self.max_iterations + frame_num * self.wind[0][0]: -(self.max_iterations - frame_num * self.wind[0][0]), 
                              self.max_iterations + frame_num * self.wind[0][1]: -(self.max_iterations - frame_num * self.wind[0][1])]
        return arr
    
    def add_rain(self, big_arr, rain_intensity):
        """
        This function draws blue rain onto our grid.

        Args: 
            big_arr (numpy array): the grid plot that has been enlarged to have more pixels per cell
            rain_intensity (numpy array): a grid the same size as our grid plot, with a rain intensity value (between 0 and 1) for each cell

        Returns:
            (numpy array): our grid plot but with rain (blue dots in the shape of clouds)

        """
        new_arr = big_arr.copy()  
        # need to enlarge the rain_intensity array so that it matches the size of the grid we're plotting
        # we need to multiply the rain intensity values by 100 otherwise the enlarge function will round them to 0
        big_rain = enlarge(rain_intensity * 100)  / 100 
        # create an array of random numbers the same size as the rain array
        rand_arr = np.random.random(big_rain.shape)
        # where the array of random values is smaller than the rain array, we set that pixel to dark blue 
        # the rain array is divided by two as we want to randomly take some of the raindrops out of each cell - don't want the whole cell to be blue
        rain_mask = rand_arr < big_rain / 2
        new_arr[rain_mask] = 3 # 3 is dark blue 
        return new_arr


        

        
        
