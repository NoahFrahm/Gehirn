import sys
sys.path.append('/Users/noahfrahm/Library/Mobile Documents/com~apple~CloudDocs/VScode workspaces/Gehirn/')

import os
import random
from typing import List, Tuple
import neat

from tetris_noah import shapes, create_grid, GamePiece


def get_shape(num):
    random.seed(711)
    while num > 0:
        _ = random.randint(0,len(shapes)-1)
        num -= 1
    ind = random.randint(0,len(shapes)-1)
    return GamePiece(5, 0, ind, shapes[ind])


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
    

def main(genomes, config):
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

    piece_point_val = 8 #2
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
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         run = False
            #         break
            #         # raise Exception
            if not run: break

            # ge[index].fitness += 1
            player.grid = create_grid(player.locked_positions)

            if player.frame % 2 == 1:
                player.change_piece = player.current_piece.move("DOWN", player.grid)
            
            if not player.change_piece:
                locked_data = tuple(0 if player.locked_positions[y][x] == (0,0,0) else 1 for x in range(10) for y in range(20))
                shape = player.current_piece.shape_id + 1
                orientation = player.current_piece.orientation + 1
                next_shape = player.next_piece.shape_id + 1
                next_orientation = player.next_piece.orientation + 1
                cur_x = player.current_piece.x
                cur_y = player.current_piece.y
                data = (shape, orientation, next_shape, next_orientation, cur_x, cur_y) + locked_data
                # (shape, orientation, next_shape, next_orientation)
                
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
                    if player.locked_positions[pos[1]][pos[0]] != (0,0,0):
                        ge[index].fitness -= 60
                        dead_nets.add(index)
                        terminated = True
                    else:
                        player.locked_positions[pos[1]][pos[0]] = player.current_piece.color
                    y = pos[1]
                    if (0,0,0) not in player.locked_positions[y]:
                        to_pop[y] = 1

                if not terminated:
                    ge[index].fitness += 0.1
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
                    player.level = player.lines_cleared // 5 + 1

                    for pop_index in popcorn:
                        player.locked_positions.pop(pop_index)
                    for _ in popcorn:
                        player.locked_positions.insert(0, [(0,0,0) for _ in range(10)])

                    
                    player.current_piece = player.next_piece
                    player.piece_count += 1
                    player.next_piece = get_shape(player.piece_count + 1)
                    player.change_piece = False
            
            player.frame += 1
        
        dead_nets = sorted(dead_nets)
        dead_nets.reverse()
        for ind in dead_nets:
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

    chicken_dinner = p.run(main, 200)
    import pickle
    with open('model_pickle_solo_1.0','wb') as f:
        pickle.dump(chicken_dinner, f)


if __name__ == "__main__":
    config_path = '/Users/noahfrahm/Library/Mobile Documents/com~apple~CloudDocs/VScode workspaces/Gehirn/ml/config_files/config_solo.txt'
    local_directory = os.path.dirname(__file__)
    configuration_file_path = os.path.join(local_directory, config_path)
    run(configuration_file_path)
