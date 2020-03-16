'''
Created on 08 August 2017
@author: Yahya Almardeny

This helper file to find the local linearity between every two points
for every gas that a given MQ sensor can detect, it simulates a derivative
between every two points in the curve, that shall increase the accuracy
especially for a curve with some scattered points which probably
generate incorrect slope between the very first point and the last point
'''

from math import log10
from point import Point

############################### Local Linearities #############################
# Input: gases_points
# Output: all_gases
# Remarks: collect the local linearity for every pair of points in each gas
# and return a dic of the gas name as a key -> list of lists [[x0,y0,slope],..]
# each inner list contains the local linearity for two points, the first is x0 & y0
# and the second is the next one on the curve (which is omitted from the result
# as it won't involve in calculations)
###############################################################################
def local_linearities(gases_points, ratio):
    all_gases = {}    
    for gas, points in gases_points.items():
        points.insert(0,Point(1,ratio)) # at the first point (1, ratio)
        all_gases[gas] = __local_linearity(points)
        
    return all_gases



############################### Local Linearity ###############################
# Input: points
# Output: local_linearity
# Remarks: find the local linearity for every pair of points on each gas curve
###############################################################################          
def __local_linearity(points):
    local_linearity = []
    for i in range(len(points)-1):
        two_points = [points[i],points[i+1]]
        local_linearity.append([two_points[0],  __derivative(two_points)])
    
    return local_linearity
    

        
############################### Derivative ###################################
# Input: two_points
# Output: slope (derivative)
# Remarks: find the derivative for every given pair of points
##############################################################################
def __derivative(two_points):
    return log10(two_points[1].get_y()/float(two_points[0].get_y())) / log10(two_points[1].get_x()/float(two_points[0].get_x()))



############ Approximation of Local Linearity at Specific Point ##############
# Input: gas, all_gases, y
# Output: local linearity
# Remarks: for a value at y-axis of a given point, search and return
# the derivative and the point(x0,y0) of a given gas from all_gases dic
##############################################################################
def local_line(gas, all_gases, y):
    gas_linearities = all_gases[gas]
    for line in range(len(gas_linearities)-1,-1, -1):
        if (y <= gas_linearities[line][0].get_y()):
            return gas_linearities[line]
    # in case it's greater than Rs/R0 in clean air   
    if(y >= gas_linearities[0][0].get_y()):
        return gas_linearities[0]
    
