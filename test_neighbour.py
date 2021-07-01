"""
This module is used to test the fire spreading to each of the eight neighbours by the spread_fire function in the module grid_updator.
"""
#Importing modules
import pytest
import numpy as np
#This is the function to test
from grid_updater import spread_fire
#This has any of the parameters we may need
import config

#The variables to be tested.
@pytest.mark.parametrize("grid, output, height, width", [
   # A 3x3 grid of no trees on fire should return no trees on fire
    (np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), 
     np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
    3,3),
    
    #A 3x3 grid with one burning tree in the upper left-hand corner, should return trees around it on fire. Tests the corners.
    (np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]), 
     np.array([[2, 1, 0], [1, 1, 0], [0, 0, 0]]),
    3,3),
    
    #A 3x3 grid with one burning tree in the middle, should return the entire grid of trees burning, around should be all 3s
    (np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]), 
     np.array([[1, 1, 1], [1, 2, 1], [1, 1, 1]]),
    3,3),
    
    #A 4x4 grid with one burning tree, should return only the ones around on fire
    (np.array([[0, 0, 0,0 ], [0, 1, 0,0], [0, 0, 0,0 ], [0, 0, 0,0 ]]), 
     np.array([[1, 1, 1,0 ], [1, 2, 1,0], [1, 1, 1,0 ], [0, 0, 0,0 ]]),
     3,3),
])

def test_spread_fire(grid, output, height, width):
    """
    This is used to test the functionality of the spread_fire function in the basic model. 
    Different situations are used to test functionality and scenarios.
    
    Args:
        grid: the input grid
        
        output: the expected output
        
        height: the height of the grid
        
        width: the width of the grid
        
    Output:
        Boolean value: if the test result and expected output are equal
        
    """
    #runs the spread_fire function that spreads fire around the neighbours and stores this as a variable called test_result
    test_result = spread_fire(grid, height, width)
    #The np.array_equal function checks that the two numpy grids are equal, if they are returns "True" and if not "False". This compares the test_result and expected output. This line asserts this output will be True.
    assert np.array_equal(test_result, output) == True
