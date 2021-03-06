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
    [(0,0),(1,0),(-1,0),(0,-1)],
    [(0,0),(1,0),(0,1),(0,-1)],
    [(0,0),(1,0),(0,1),(-1,0)],
    [(0,0),(0,-1),(0,1),(-1,0)],
    ]

square = [
    [(0,0),(0,-1),(-1,-1),(-1,0)],
    [(0,0),(0,-1),(-1,-1),(-1,0)],
    [(0,0),(0,-1),(-1,-1),(-1,0)],
    [(0,0),(0,-1),(-1,-1),(-1,0)],
    ]

s5 = [
    [(0,0),(1,0),(-1,-1),(0,-1)],
    [(0,0),(-1,0),(-1,1),(0,-1)],
    [(0,0),(1,0),(-1,-1),(0,-1)],
    [(0,0),(-1,0),(-1,1),(0,-1)],
    ]

s = [
    [(0,0),(-1,0),(1,-1),(0,-1)],
    [(0,0),(0,1),(-1,0),(-1,-1)],
    [(0,0),(-1,0),(1,-1),(0,-1)],
    [(0,0),(0,1),(-1,0),(-1,-1)],
    ]

l = [
    [(0,0), (-1,0),(1,0),(1,-1)],
    [(0,0), (0,1),(0,-1),(1,1)],
    [(0,0),(-1,0),(1,0),(-1,1)],
    [(0,0),(0,-1),(0,1),(-1,-1)]
    ]

p = [
    [(0,0), (-1,0),(1,0),(-1,-1)],
    [(0,0), (0,1),(0,-1),(1,-1)],
    [(0,0),(-1,0),(1,0),(1,1)],
    [(0,0),(0,-1),(0,1),(-1,1)]
    ]

i = [
    [(0,0),(-1,0),(1,0),(2,0)],
    [(0,0),(0,-1),(0,1),(0,2)],
    [(0,0),(-1,0),(1,0),(2,0)],
    [(0,0),(0,-1),(0,1),(0,2)],
    ]

shapes = [t,l,p,i,s,s5,square]


class GamePiece:

    def __init__(self, x, y, shape_index, orientations) -> None:
        self.x = x
        self.y = y
        self.shape_orientations = orientations
        self.orientation = 0
        self.current_shape = self.pointify(self.x, self.y, self.shape_orientations[0])
        self.color = (0, 255, 0)
        self.shape_id = shape_index

    

    def pointify(self, x,y,orientation):
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
            self.orientation = new_orientation
            self.current_shape = new_shape
        
    
    def move(self, direction, grid) -> bool:
        """changes the x,y of our piece"""
        # returns true if we move DOWN and collide with something else false
        if direction == "LEFT":
            shifted_shape = self.pointify(self.x - 1, self.y, self.shape_orientations[self.orientation])
            # print(self.inBounds(grid, shifted_shape))
            if self.inBounds(grid, shifted_shape):
                self.current_shape = shifted_shape
                self.x -= 1
        if direction == "RIGHT":
            shifted_shape = self.pointify(self.x + 1, self.y, self.shape_orientations[self.orientation])
            # print(self.inBounds(grid, shifted_shape))
            if self.inBounds(grid, shifted_shape):
                self.current_shape = shifted_shape
                self.x += 1
        if direction == "DOWN":
            shifted_shape = self.pointify(self.x, self.y + 1, self.shape_orientations[self.orientation])
            # print(self.inBounds(grid, shifted_shape))
            if self.inBounds(grid, shifted_shape):
                self.current_shape = shifted_shape
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
       
        for point in shape:
            if point not in accepted_pos:
                # print(point)
                # for when we start off screen shape we are good so only > -1
                if point[1] > -1 or point[0] < 0 or point[0] > 9:
                    return False
        return True    


def create_grid(locked_positions = {}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if locked_positions[i][j] != (0,0,0):
                c = locked_positions[i][j]
                grid[i][j] = c
    return grid


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy + i*block_size), (sx + j*block_size, sy + play_height))


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

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    
    pygame.draw.rect(surface, (255, 0, 0),(top_left_x, top_left_y, play_width, play_height), 4)
    draw_grid(surface, grid)
    pygame.display.update()


def get_shape():
    ind = random.randint(0,len(shapes)-1)
    return GamePiece(5, 0, ind, shapes[ind])


def main(win, score):
    locked_positions = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    grid = create_grid(locked_positions)
    # score = 0
    point_key = {
        0:0,
        1:40,
        2:100,
        3:300,
        4:1200,
    }

    level_multiplier = {

    }

    # when true we burn the current piece permanently into our grid where it stands
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
        # print(score)
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
        # draw_next_shape(next_piece, win)

    return score


def main_menu():
    # win = pygame.display.set_mode((screen_width, screen_height))
    # pygame.display.set_caption('Tetris')
    # score = main(win, 0)
    # print(score)
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    shape = [(9, 0), (8, 0), (10, -1), (9, -1)]
    # accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    # accepted_pos = [j for sub in accepted_pos for j in sub]

    print(GamePiece.inBounds(grid, shape))


if __name__ == "__main__":
    # win = pygame.display.set_mode((screen_width, screen_height))
    # pygame.display.set_caption('Tetris')
    main_menu()
