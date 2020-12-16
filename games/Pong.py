import pygame
from pygame.draw import *
from random import randint, choice
from math import pi, sin, cos

pygame.init()
FPS = 120

screen_x, screen_y = 1200, 600
screen = pygame.display.set_mode((screen_x, screen_y))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
rect_y = 3 * screen_y / 20
rect_x = 3 * rect_y / 20
radius = screen_x / 120
score_1 = 0
score_2 = 0
score_3 = 0


def show_score():
    """Draws player's score in top left corner of the screen"""
    font = pygame.font.SysFont('arial', 50, True)
    text_1 = font.render("{}".format(score_1), True, WHITE)
    text_2 = font.render("{}".format(score_2), True, WHITE)
    screen.blit(text_1, (screen_x / 4, 0))
    screen.blit(text_2, (3 * screen_x / 4, 0))


def ball_parameters(v, ar):
    param = []
    rand = {
        '1': randint(int(100 * pi / 8), int(200 * pi / 8)),
        '2': randint(int(600 * pi / 8), int(700 * pi / 8)),
        '3': randint(int(900 * pi / 8), int(1000 * pi / 8)),
        '4': randint(int(1400 * pi / 8), int(1500 * pi / 8))
    }
    angle = choice(list(rand.values()))
    param.append({
        'x': screen_x / 2,
        'y': screen_y / 2,
        'vx': v * cos(angle / 100),
        'vy': v * sin(angle / 100),
        'ax': ar * cos(angle / 100),
        'ay': ar * sin(angle / 100),
        'r': randint(40, 255),
        'g': randint(40, 255),
        'b': randint(40, 255),
        'w': 0,
        'e': 0.002
    })
    return param


def rockets_lists():
    list_1 = [{'x': screen_x / 10, 'y': screen_y / 2}]
    list_2 = [{'x': 9 * screen_x / 10, 'y': screen_y / 2}]
    return list_1, list_2


def draw_rocket(rocket_1, rocket_2):
    for item in rocket_1:
        rect(screen, WHITE, (item['x'], item['y'], rect_x, rect_y))
    for item in rocket_2:
        rect(screen, WHITE, (item['x'], item['y'], rect_x, rect_y))


def balls_movement():
    for item in balls:
        ellipse(screen, (item['r'], item['g'], item['b']),
                (item['x'] - radius, item['y'] - radius, 2 * radius, 2 * radius))
        item['x'] += item['vx']
        item['y'] += item['vy']
        if item['vx'] <= 2 * rect_x:
            item['vx'] += item['ax']
            item['vy'] += item['ay']


def ricochet_wall(param):
    global score_1, score_2, score_3
    for item in param:
        if item['y'] - radius <= 0:
            item['vy'] = abs(item['vy'])
            item['ay'] = abs(item['ay'])
        if item['y'] + radius >= screen_y:
            item['vy'] = -abs(item['vy'])
            item['ay'] = -abs(item['ay'])
        if item['x'] - radius <= 0:
            score_2 += 1
            score_3 += 1
        if item['x'] + radius >= screen_x:
            score_1 += 1
            score_3 += 1


def rocket_ricochet(list_1, list_2, list_3):
    for ball in list_1:
        for rect_1, rect_2 in zip(list_2, list_3):
            if rect_1['x'] - rect_x * 3 <= ball['x'] - radius <= rect_1['x'] and \
                    rect_1['y'] - radius <= ball['y'] <= rect_1['y'] + rect_y + radius:
                ball['vx'] = abs(ball['vx'])
                ball['ax'] = abs(ball['ax'])
            if rect_2['x'] + rect_x * 3 >= ball['x'] + radius >= rect_2['x'] and \
                    rect_2['y'] - radius <= ball['y'] <= rect_2['y'] + rect_y + radius:
                ball['vx'] = -abs(ball['vx'])
                ball['ax'] = -abs(ball['ax'])


def rocket_movement(speed):
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        for ball in rock_2:
            ball['y'] -= speed
    if key[pygame.K_DOWN]:
        for ball in rock_2:
            ball['y'] += speed
    if key[pygame.K_w]:
        for ball in rock_1:
            ball['y'] -= speed
    if key[pygame.K_s]:
        for ball in rock_1:
            ball['y'] += speed


def rocket_teleport(list_1, list_2):
    for rect_1, rect_2 in zip(list_1, list_2):
        if rect_1['y'] < 0:
            rect_1['y'] = 0
        if rect_2['y'] < 0:
            rect_2['y'] = 0
        if rect_1['y'] + rect_y > screen_y:
            rect_1['y'] = screen_y - rect_y
        if rect_2['y'] + rect_y > screen_y:
            rect_2['y'] = screen_y - rect_y


clock = pygame.time.Clock()
finished = False

while not finished:
    rock_1, rock_2 = rockets_lists()
    balls = ball_parameters(v=3, ar=0.004)
    score_3 = 0
    while score_3 < 1:
        clock.tick(FPS)
        balls_movement()
        ricochet_wall(balls)
        draw_rocket(rock_1, rock_2)
        rocket_teleport(rock_1, rock_2)
        rockets_lists()
        rocket_ricochet(balls, rock_1, rock_2)
        show_score()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        rocket_movement(speed=7)
        pygame.display.update()
        screen.fill(BLACK)

pygame.quit()
