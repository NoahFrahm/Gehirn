
import os
import pygame
import neat
from tetris_noah import GamePiece, create_grid, get_shape, draw_grid, screen_width, screen_height, top_left_x, play_width, play_height, top_left_y, block_size


def draw_window(surface, grid, score):
    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render(str(score), 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width * 1.5 - (label.get_width() / 2), play_height / 2))

    # pygame.font.init()
    # font = pygame.font.SysFont('comicsans', 40)
    # label = font.render("fitness: " + str(fitness), 1, (255, 255, 255))
    # surface.blit(label, (top_left_x + play_width * 1.5 - (label.get_width() / 2), play_height / 2 + 40))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    
    pygame.draw.rect(surface, (255, 0, 0),(top_left_x, top_left_y, play_width, play_height), 4)
    draw_grid(surface, grid)
    pygame.display.update()


def main(win, score, genomes, config):
    model = neat.nn.FeedForwardNetwork.create(genomes[0][1], config)
    locked_positions = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    grid = create_grid(locked_positions)
    point_key = {
        0:0,
        1:40,
        2:100,
        3:300,
        4:1200,
    }
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    piece_count = 0
    lines_cleared = 0
    level = 1
    piece_point_val = 20

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            change_piece = current_piece.move("DOWN", grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if not change_piece:
            locked_data = tuple(0 if locked_positions[y][x] == (0,0,0) else 1 for x in range(10) for y in range(20))
            shape = current_piece.shape_id + 1
            orientation = current_piece.orientation + 1
            next_shape = next_piece.shape_id + 1
            next_orientation = next_piece.orientation + 1
            cur_x = current_piece.x
            cur_y = current_piece.y
            data = (shape, orientation, next_shape, next_orientation, cur_x, cur_y) + locked_data
            output = model.activate(data)
            max_val_index, maxi = 0, 0
            for i, val in enumerate(output):
                if val > maxi:
                    maxi = val
                    max_val_index = i
            if max_val_index == 0:
                _ = current_piece.move("LEFT", grid)
            elif max_val_index == 1:
                _ = current_piece.move("RIGHT", grid)
            elif max_val_index == 2:
                _ = current_piece.move("DOWN", grid)
            elif max_val_index == 3:
                _ = current_piece.move("UP", grid)

        for point in current_piece.current_shape:
            x,y = point
            if y > -1:
                grid[y][x] = current_piece.color
        
        if change_piece:
            piece_count += 1
            to_pop = {}
            for pos in current_piece.current_shape:
                if locked_positions[pos[1]][pos[0]] != (0,0,0):
                    run = False
                else:
                    locked_positions[pos[1]][pos[0]] = current_piece.color
                y = pos[1]
                if (0,0,0) not in locked_positions[y]:
                    to_pop[y] = 1

            popcorn = []
            for key in to_pop.keys():
                popcorn.append(key)
            popcorn.sort()
            popcorn.reverse()

            score += (point_key[len(popcorn)] * level)
            score += (piece_point_val * level)
            lines_cleared += len(popcorn)
            level = lines_cleared // 5 + 1


            for pop_index in popcorn:
                locked_positions.pop(pop_index)
            for _ in popcorn:
                locked_positions.insert(0, [(0,0,0) for _ in range(10)])

            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            
        draw_window(win, grid, score)
        pygame.display.update()

    return score


def main_menu(configuration_file_path):
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tetris')
    model = None
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, configuration_file_path)
    
    import pickle
    model_path = '/Users/noahfrahm/Library/Mobile Documents/com~apple~CloudDocs/VScode workspaces/Gehirn/models/two04in_4out.0'
    # '/Users/noahfrahm/Library/Mobile Documents/com~apple~CloudDocs/VScode workspaces/Gehirn/models/four_input_0_hidden'
    with open(model_path,'rb') as f:
        model = pickle.load(f)    
    genomes = [(1, model)]
    score = main(win, 0, genomes, config)
    

if __name__ == "__main__":
    config_path = '/Users/noahfrahm/Library/Mobile Documents/com~apple~CloudDocs/VScode workspaces/Gehirn/ml/config_files/config_solo.txt'
    local_directory = os.path.dirname(__file__)
    configuration_file_path = os.path.join(local_directory, config_path)
    main_menu(configuration_file_path)
