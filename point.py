'''
Created on 08 August 2017
@author: Yahya Almardeny

This class represents a POINT(x,y) in order to ease the work (MQ sensors points calculation and manipulation..etc)
'''


class Point:

    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get(self):
        return [self.x, self.y]

    def __repr__(self):
        return "{},{}".format(self.x, self.y)
    
    
    
    