import pygame, sys
from pygame.locals import *
from puzzle import Puzzle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (192, 192, 192)


def draw_square(x, y, n, width, surface, font):
    square = pygame.draw.polygon(surface, RED, (
        (x-width/2, y-width/2),
        (x+width/2, y-width/2),
        (x+width/2, y+width/2),
        (x-width/2, y+width/2)
    ))
    number = font.render(str(n), True, WHITE, RED)
    if int(n) >= 10:
        surface.blit(number, (x - width/3, y - width/3))
    else:
        surface.blit(number, (x - width/6, y - width/3))


def draw_puzzle(puzzle, surface, font):
    oldstartx = startx = 25
    starty = 25
    size = puzzle.n
    if size is 9:
        oldstartx = startx = 80
        starty = 80
    elif size is 7:
        oldstartx = startx = 135
        starty = 135
    elif size is 5:
        oldstartx = startx = 190
        starty = 190

    for i in range(0, puzzle.n):
        for j in range(0, p.n):
            draw_square(startx, starty, puzzle.puzzle[i][j], 50, surface, font)
            startx += 55
        startx = oldstartx
        starty += 55



pygame.init()

# max size for 11 x 11 is 600
windowSurface = pygame.display.set_mode((600, 700), 0, 32)


#windowSurface.fill(BLACK)

pygame.display.update()

basicFont = pygame.font.SysFont(None, 48)


size = 5
p = Puzzle(size)
print(p)
draw_puzzle(p, windowSurface, basicFont)

pygame.display.update()

p.bfs()


pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

'''
class PuzzleGUI(object):
    def __init__(self, n):
        self.puzzle = Puzzle(n)
'''

