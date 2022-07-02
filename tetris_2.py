import random
from typing import List, Tuple
import pygame

screen_width = 800
screen_height = 700
play_width = 300
play_height = 600
block_size = 30

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height

t = [
    [(0,0),(1,0),(0,1),(0,-1)],
    [(0,0),(0,1),(1,0),(-1,0)],
    [(0,0),(-1,0),(0,-1),(0,1)],
    [(0,0),(0,-1),(-1,0),(1,0)]
    ]
l = [
    [(0,0), (-1,0),(1,0),(1,-1)],
    [(0,0), (0,1),(0,-1),(1,1)],
    [(0,0),(-1,0),(1,0),(-1,1)],
    [(0,0),(0,-1),(0,1),(-1,-1)]
    ]

shapes = [t,l]
tetriminos = []
drawy_grid = [[0 for j in range(5)] for i in range(5)]


class GamePiece:

    def __init__(self, x, y, orientations) -> None:
        self.x = x
        self.y = y
        self.shape_orientations = orientations
        self.orientation = 0
        self.current_shape = self.pointify(x, y, orientations[0])
        self.color = (0, 255, 0)
    
    def pointify(x,y,orientation):
        """converts orienatation into grid points"""
        coors = []
        for point in orientation:
            my_point = (point[0] + x, point[1] + y)
            coors.append(my_point)
        return coors
    
    def rotate(self, grid) -> None:
        """Rotates the piece based on orientation number"""
        new_orientation = (self.orientation + 1) % 4
        new_shape = self.pointify(self.x, self.y, self.shape_orientations[new_orientation])
        if self.inBounds(grid, new_shape):
            self.orientation = (self.orientation + 1) % 4
            self.current_shape = new_shape
        
    
    def move(self, direction, grid) -> bool:
        """changes the x,y of our piece"""
        # returns true if we move DOWN and collide with something else false
        if direction == "LEFT":
            shifted_shape = self.pointify(self.x - 1, self.y, self.shape_orientations[self.orientation])
            if self.inBounds(grid, shifted_shape):
                self.x -= 1
        if direction == "RIGHT":
            shifted_shape = self.pointify(self.x + 1, self.y, self.shape_orientations[self.orientation])
            if self.inBounds(grid, shifted_shape):
                self.x += 1
        if direction == "DOWN":
            shifted_shape = self.pointify(self.x, self.y - 1, self.shape_orientations[self.orientation])
            if self.inBounds(grid, shifted_shape):
                self.y += 1
            else: return True
        if direction == "UP":
            # make sure we can always rotate if there is enough room
            # long piece cant rotate if hugging the wall
            self.rotate(grid)
        return False


    def inBounds(self, grid, shape) -> bool:
        """makes sure that a given x,y is valid for game bounds"""
        # we grab all tiles that do not have shapes on them
        accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        # add check for no collision on grid

        for point in shape:
            if point not in accepted_pos:
                # for when we start off screen shape we are good so only > -1
                if point[1] > -1:
                    return False
        return True