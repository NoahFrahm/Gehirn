import os
import random
from typing import List
import pygame
import pickle
import neat
# from tetris_noah
from tetris_noah import shapes, GamePiece, create_grid, get_shape


# finish up normal tetris to add point multiplier for level
# this level multiplier will incentivize going further in the game
# this version will not draw any of the ui components and rather just play the game and train a model

class Player:
    def __init__(self) -> None:
        self.locked_positions = [[(0,0,0) for _ in range(10)] for _ in range(20)]
        self.grid = create_grid(self.locked_positions)
        self.change_piece = False
        self.run = True
        self.clock = pygame.time.Clock()
        self.piece_count = 0
        self.lines_cleared = 0
        self.level = 1
        self.current_piece = get_shape()
        self.next_piece = get_shape()
        self.fall_time = 0
        # remove this later since we dont use score but rather fitness
        self.score = 0



def main(genomes, config):
    nets: List[neat.nn.FeedForwardNetwork] = []
    ge = []
    my_players: List[Player] = []

    for _ , g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        new_player = Player()
        my_players.append(new_player)
        g.fitness = 0
        ge.append(g)

    point_key = {
        0:0,
        1:4,
        2:10,
        3:30,
        4:120,
    }

    fall_speed = 0.27
    piece_point_val = 2

    while run:
        if len(my_players) == 0:
            run = False
            break

        for index, player in enumerate(my_players):
            player.grid = create_grid(player.locked_positions)
            player.fall_time += player.clock.get_rawtime()
            player.clock.tick()

            if player.fall_time / 1000 > fall_speed:
                player.fall_time = 0
                player.change_piece = player.current_piece.move("DOWN", player.grid)
                    

            # moving our bird with neural network
            # position of our piece
            # piece_coors = ()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # locked tiles data
            locked_data = tuple(0 if player.locked_positions[y][x] == (0,0,0) else 1 for x in range(10) for y in range(20))
            # current piece data
            shape = player.current_piece.shape_id
            orientation = player.current_piece.orientation
            # next piece data
            next_shape = player.next_piece.shape_id
            next_orientation = player.next_piece.orientation

            data = (shape, orientation, next_shape, next_orientation) + locked_data

            output = nets[index].activate(inputs=data)

            max_val_index = 0
            maxi = 0
            for index, val in output:
                if val > maxi:
                    maxi = val
                    max_val_index = index
            
            if max_val_index == 0:
                _ = player.current_piece.move("LEFT", player.grid)
            elif max_val_index == 0:
                _ = player.current_piece.move("RIGHT", player.grid)
            elif max_val_index == 0:
                _ = player.current_piece.move("DOWN", player.grid)
            elif max_val_index == 0:
                _ = player.current_piece.move("UP", player.grid)
                

            for point in player.current_piece.current_shape:
                x,y = point
                if y > -1:
                    player.grid[y][x] = player.current_piece.color
                
            
            if player.change_piece:
                player.piece_count += 1
                to_pop = {}
                for pos in player.current_piece.current_shape:
                    if player.locked_positions[pos[1]][pos[0]] != (0,0,0):
                        ge[index].fitness -= 10
                        my_players.pop(index)
                        ge.pop(index)
                        nets.pop(index)
                    else:
                        player.locked_positions[pos[1]][pos[0]] = player.current_piece.color
                        # not fitness here but rather in the next part with scoring
                    y = pos[1]
                    if (0,0,0) not in player.locked_positions[y]:
                        to_pop[y] = 1

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
                player.next_piece = get_shape()
                player.change_piece = False


def run(configuration_file_path):
    # finish decinding params in config file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, configuration_file_path)

    p = neat.Population(config)

    # reporters, possibly remove later
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter(True))

    chicken_dinner = p.run(main, 50)
    import pickle
    with open('model_pickle','wb') as f:
        pickle.dump(chicken_dinner, f)

if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    configuration_file_path = os.path.join(local_directory, "config_neat_model.txt")
    run(configuration_file_path)
