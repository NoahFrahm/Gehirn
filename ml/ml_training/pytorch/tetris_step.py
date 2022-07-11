import sys
sys.path.append('/Users/noahfrahm/Library/Mobile Documents/com~apple~CloudDocs/VScode workspaces/Gehirn/')

import os
import random
from typing import List, Tuple
import neat

from tetris_noah import shapes, create_grid, GamePiece


class Game:

    piece_point_val = 8 #2
    point_key = {
        0:0,
        1:40,
        2:100,
        3:300,
        4:1200,
    }

    def __init__(self) -> None:
        self.player = MyPlayer()
    

    def get_shape(self, num):
        random.seed(711)
        while num > 0:
            _ = random.randint(0,len(shapes)-1)
            num -= 1
        ind = random.randint(0,len(shapes)-1)
        return GamePiece(5, 0, ind, shapes[ind])


    def get_state(self):
        locked_data = tuple(0 if self.player.locked_positions[y][x] == (0,0,0) else 1 for x in range(10) for y in range(20))
        shape = self.player.current_piece.shape_id + 1
        orientation = self.player.current_piece.orientation + 1
        next_shape = self.player.next_piece.shape_id + 1
        next_orientation = self.player.next_piece.orientation + 1
        cur_x = self.player.current_piece.x
        cur_y = self.player.current_piece.y
        data = (shape, orientation, next_shape, next_orientation, cur_x, cur_y) + locked_data
        # return self.player
        return data
    

    def make_move(self, move):
        self.player.grid = create_grid(self.player.locked_positions)

        if self.player.frame % 2 == 1:
            self.player.change_piece = self.player.current_piece.move("DOWN", self.player.grid)
        
        if not self.player.change_piece:
            # code here to process move input
            if move == 0:
                _ = self.player.current_piece.move("LEFT", self.player.grid)
            elif move == 1:
                _ = self.player.current_piece.move("RIGHT", self.player.grid)
            elif move == 2:
                _ = self.player.current_piece.move("DOWN", self.player.grid)
            elif move == 3:
                _ = self.player.current_piece.move("UP", self.player.grid)

        for point in self.player.current_piece.current_shape:
            x,y = point
            if y > -1:
                self.player.grid[y][x] = self.player.current_piece.color
        
        if self.player.change_piece:
            to_pop = {}
            # terminated = False
            for pos in self.player.current_piece.current_shape:
                if self.player.locked_positions[pos[1]][pos[0]] != (0,0,0):
                    self.player.run = False
                else:
                    self.player.locked_positions[pos[1]][pos[0]] = self.player.current_piece.color
                y = pos[1]
                if (0,0,0) not in self.player.locked_positions[y]:
                    to_pop[y] = 1

            if self.player.run:
                
                popcorn = []
                for key in to_pop.keys():
                    popcorn.append(key)
                popcorn.sort()
                popcorn.reverse()

                self.player.score += (self.point_key[len(popcorn)] * self.player.level)
                self.player.score += (self.piece_point_val * self.player.level)
                self.player.lines_cleared += len(popcorn)
                self.player.level = self.player.lines_cleared // 5 + 1

                for pop_index in popcorn:
                    self.player.locked_positions.pop(pop_index)
                for _ in popcorn:
                    self.player.locked_positions.insert(0, [(0,0,0) for _ in range(10)])
                
                self.player.current_piece = self.player.next_piece
                self.player.piece_count += 1
                self.player.next_piece = self.get_shape(self.player.piece_count + 1)
                self.player.change_piece = False
        
        self.player.frame += 1


    def get_move(self):
        ...


class MyPlayer:
    def __init__(self) -> None:
        self.locked_positions = [[(0,0,0) for _ in range(10)] for _ in range(20)]
        self.grid = create_grid(self.locked_positions)
        self.change_piece = False
        self.run = True
        self.piece_count = 0
        self.lines_cleared = 0
        self.level = 1
        self.current_piece = get_shape(self.piece_count)
        self.next_piece = get_shape(self.piece_count + 1)
        self.frame = 0
        self.score = 0
    



def run(configuration_file_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, configuration_file_path)
    p = neat.Population(config)

    # reporters, possibly remove later
    p.add_reporter(neat.StdOutReporter(True))
    # p.add_reporter(neat.StatisticsReporter(True))

    chicken_dinner = p.run(main, 200)
    import pickle
    with open('model_pickle_solo_1.0','wb') as f:
        pickle.dump(chicken_dinner, f)


if __name__ == "__main__":
    config_path = '/Users/noahfrahm/Library/Mobile Documents/com~apple~CloudDocs/VScode workspaces/Gehirn/ml/config_files/config_solo.txt'
    local_directory = os.path.dirname(__file__)
    configuration_file_path = os.path.join(local_directory, config_path)
    run(configuration_file_path)
