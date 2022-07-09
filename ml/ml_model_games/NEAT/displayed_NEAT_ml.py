import sys
sys.path.append('/Users/noahfrahm/Library/Mobile Documents/com~apple~CloudDocs/VScode workspaces/Gehirn/')
from tetris_noah import create_grid, get_shape, screen_height, screen_width
import os
import random
from typing import List, Tuple
import pygame
import neat


class MyPlayer:
    def __init__(self) -> None:
        self.locked_positions = [[(0,0,0) for _ in range(10)] for _ in range(20)]
        self.grid = create_grid(self.locked_positions)
        self.change_piece = False
        self.run = True
        self.piece_count = 0
        self.lines_cleared = 0
        self.level = 1
        self.current_piece = get_shape()
        self.next_piece = get_shape()
        self.frame = 0
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.score = 0


def main(genomes, config):
    
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tetris')

    nets: List[neat.nn.FeedForwardNetwork] = []
    ge: List[neat.DefaultGenome] = []
    players: List[MyPlayer] = []

    for _, g in genomes:
        new_player = MyPlayer()
        players.append(new_player)
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)
    
    print(len(ge))
    print("players: " + str(len(players)))

    fall_speed = 0.07
    piece_point_val = 2
    run = True
    point_key = {
        0:0,
        1:40,
        2:100,
        3:300,
        4:1200,
    }

    while run:
        dead_nets = set()
        if len(players) == 0:
            run = False
            break
        
        for index, player in enumerate(players):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    raise Exception

            ge[index].fitness += 1
            player.grid = create_grid(player.locked_positions)
            
            # player.fall_time += player.clock.get_rawtime()
            # player.clock.tick()

            # if player.fall_time  > fall_speed:
            #     player.fall_time = 0
            #     player.change_piece = player.current_piece.move("DOWN", player.grid)

            if player.frame % 2 == 1:
                # player.fall_time = 0
                player.change_piece = player.current_piece.move("DOWN", player.grid)
            
            if not player.change_piece:
                # locked_data = tuple(0 if player.locked_positions[y][x] == (0,0,0) else 1 for x in range(10) for y in range(20))
                shape = player.current_piece.shape_id + 1
                orientation = player.current_piece.orientation + 1
                next_shape = player.next_piece.shape_id + 1
                next_orientation = player.next_piece.orientation + 1
                data = (shape, orientation, next_shape, next_orientation) #  + locked_data
                
                output = nets[index].activate(data)
                max_val_index, maxi = 0, 0
                for i, val in enumerate(output):
                    if val > maxi:
                        maxi = val
                        max_val_index = i
                if max_val_index == 0:
                    _ = player.current_piece.move("LEFT", player.grid)
                elif max_val_index == 1:
                    _ = player.current_piece.move("RIGHT", player.grid)
                elif max_val_index == 2:
                    _ = player.current_piece.move("DOWN", player.grid)
                elif max_val_index == 3:
                    _ = player.current_piece.move("UP", player.grid)

            for point in player.current_piece.current_shape:
                x,y = point
                if y > -1:
                    player.grid[y][x] = player.current_piece.color
            
            if player.change_piece:
                to_pop = {}
                terminated = False
                for pos in player.current_piece.current_shape:
                    # print(pos)
                    # print("shape ID: ", player.current_piece.shape_id)
                    # print("shape points: ", player.current_piece.current_shape)
                    # print("orientation: ", player.current_piece.orientation)
                    if player.locked_positions[pos[1]][pos[0]] != (0,0,0):
                        ge[index].fitness -= 1
                        dead_nets.add(index)
                        terminated = True
                    else:
                        player.locked_positions[pos[1]][pos[0]] = player.current_piece.color
                    y = pos[1]
                    if (0,0,0) not in player.locked_positions[y]:
                        to_pop[y] = 1

                if not terminated:
                    ge[index].fitness += 5
                    popcorn = []
                    for key in to_pop.keys():
                        popcorn.append(key)
                    popcorn.sort()
                    popcorn.reverse()

                    player.score += (point_key[len(popcorn)] * player.level)
                    ge[index].fitness += point_key[len(popcorn)] * player.level

                    player.score += (piece_point_val * player.level)
                    ge[index].fitness += piece_point_val * player.level

                    player.lines_cleared += len(popcorn)
                    ge[index].fitness += len(popcorn) * 50
                    player.level = player.lines_cleared // 5 + 1


                    for pop_index in popcorn:
                        player.locked_positions.pop(pop_index)
                    for _ in popcorn:
                        player.locked_positions.insert(0, [(0,0,0) for _ in range(10)])

                    player.current_piece = player.next_piece
                    player.next_piece = get_shape()
                    player.change_piece = False
            
            player.frame += 1
            # if index == 0:
            #     draw_window(win, player.grid, player.score)
            # pygame.display.update()
        
        dead_nets = sorted(dead_nets)
        dead_nets.reverse()
        for ind in dead_nets:
            # print(dead_nets)
            # print("pop index: " + str(ind))
            # print("players: ", players)
            players.pop(ind)
            ge.pop(ind)
            nets.pop(ind)
        

def run(configuration_file_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, configuration_file_path)
    p = neat.Population(config)

    # reporters, possibly remove later
    p.add_reporter(neat.StdOutReporter(True))
    # p.add_reporter(neat.StatisticsReporter(True))

    chicken_dinner = p.run(main, 50)
    import pickle
    with open('model_pickle_solo_1.0','wb') as f:
        pickle.dump(chicken_dinner, f)


if __name__ == "__main__":
    f_path = '/Users/noahfrahm/Library/Mobile Documents/com~apple~CloudDocs/VScode workspaces/Gehirn/ml/config_files/config_solo.txt'
    local_directory = os.path.dirname(__file__)
    configuration_file_path = os.path.join(local_directory, f_path)
    run(configuration_file_path)
