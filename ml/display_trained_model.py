
import pygame
from tetris_noah import GamePiece, create_grid, get_shape, draw_grid, draw_window, screen_width, screen_height


def main(win, score):
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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    _ = current_piece.move("LEFT", grid)
                elif event.key == pygame.K_RIGHT:
                    _ = current_piece.move("RIGHT", grid)
                elif event.key == pygame.K_DOWN:
                    _ = current_piece.move("DOWN", grid)
                elif event.key == pygame.K_UP:
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


def main_menu():
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tetris')
    model = ""
    score = main(win, 0)
    

if __name__ == "__main__":
    main_menu()
