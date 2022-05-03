import pygame
import sys
import random

from pygame.locals import *

WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH / GRID_SIZE
GRID_HEIGHT = HEIGHT / GRID_SIZE

BLACK = (0, 0, 0)
GREEN = (0, 50, 0)
ORANGE = (250, 150, 0)
RED    = (255, 0, 0)
GRAY   = (100, 100, 100)

# set the movement with the coordinates
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FPS = 10

class Snake(object):
    def __init__(self):
        self.create()
        self.color = GREEN

    def create(self):
        self.length = 2
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction =random.choice([UP, DOWN, LEFT, RIGHT])

    def control(self, xy):
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if new in self.positions[2:]:
            self.create()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def eat(self):
        self.length += 1

    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)

class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.create()

    def create(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        draw_object(surface, self.color, self.position)

# to draw object on the screen make a grid so that it can get POS
def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, color, r)

def check_eat(Snake, feed):
    if Snake.positions[0] == feed.position:
        Snake.eat()
        feed.create()

def show_info(length, speed, surface):
    font = pygame.font.Font(None, 34)
    text = font.render("Length: " + str(length) + "   Speed: " + str(round(speed,2)),1,GRAY)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text, pos) 

if  __name__ == '__main__':
    snake = Snake()
    feed = Feed()
    
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('SNAKE GAME')

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    clock = pygame.time.Clock()

    surface.fill(BLACK)
    screen.blit(surface, (0, 0))
    
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    snake.control(UP)
                elif event.key == K_DOWN:
                    snake.control(DOWN)
                elif event.key == K_LEFT:
                    snake.control(LEFT)
                elif event.key == K_RIGHT:
                    snake.control(RIGHT)

        surface.fill(BLACK)

        snake.move()

        check_eat(snake, feed)

        speed = (FPS + snake.length) / 2

        show_info(snake.length,speed,surface)

        snake.draw(surface)

        feed.draw(surface)

        screen.blit(surface, (0, 0))

        pygame.display.flip()
        pygame.display.update()

        clock.tick(speed)
