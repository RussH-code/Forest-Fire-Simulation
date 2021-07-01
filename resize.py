"""
This module contains functions to resize the grid plot.
"""

import cv2
import numpy as np
from config import GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE


def shrink(arr):
    """
    This function reduces the size of a grid so that 1 cell has 1 pixel 
    
    Args:
        arr (numpy array): a grid to shrink
        
    Output:
        arr (numpy_array) : the new grid that has been shrunk
    """
    # create a copy of the array to shrink
    arr_ = arr.copy()
    # use cv2 to resize this grid to the size of grid height x grid width
    return cv2.resize(arr_.astype(np.uint8), (GRID_HEIGHT, GRID_WIDTH), interpolation = cv2.INTER_AREA)


def enlarge(arr):
    """
    This function enlarges an array so that each cell has multiple pixels
    
    Args:
        arr (numpy array): a grid to enlarge
        
    Output:
        arr (numpy_array) : the new grid that has been enlarged
    """
    # create a copy of the array to enlarge
    arr_ = arr.copy()
     # use cv2 to resize this grid 
    return cv2.resize(arr_.astype(np.uint8), (GRID_HEIGHT * BLOCK_SIZE, GRID_WIDTH * BLOCK_SIZE), interpolation = cv2.INTER_AREA)