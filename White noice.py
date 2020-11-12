import pygame
from pygame.draw import *
from random import randint as ran

FPS = 60

screen_x, screen_y = 300, 300
screen = pygame.display.set_mode((screen_x, screen_y))

rect_size = 3


def noise():
    for x in range(0, screen_x, rect_size):
        for y in range(0, screen_y, rect_size):
            rgb = ran(0, 255)
            rect(screen, (rgb, rgb, rgb), (x, y, rect_size, rect_size))


finished = False
clock = pygame.time.Clock()

while not finished:
    clock.tick(FPS)
    noise()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    pygame.display.update()

pygame.quit()
