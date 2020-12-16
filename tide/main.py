from math import sin, cos, pi

import pygame
from pygame.draw import *

from my_colors import *

pygame.init()

FPS = 60
SCREEN_X, SCREEN_Y = 1300, 600
GROUND_Y = 19 * SCREEN_Y // 20

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))


class Simulator:
    def __init__(self, n=30, d_moon=SCREEN_Y/3, angle_moon=0, v=0.3, m_earth=100, m_moon=10, r_earth=50, k=0.00005, b=0.01):
        self.n = n
        self.d_moon = d_moon
        self.angle_moon = angle_moon
        self.x = self.d_moon * cos(self.angle_moon)
        self.y = self.d_moon * sin(self.angle_moon)
        self.v = v
        self.a = [i * 2 * pi / n for i in range(self.n)]
        self.da = [0 for i in range(self.n)]
        self.d2a = [0 for i in range(self.n)]
        self.m_earth = m_earth
        self.m_moon = m_moon
        self.r_earth = r_earth
        self.k = k
        self.b = b

    def move(self):

        self.angle_moon += self.v / self.d_moon

        self.x = self.d_moon * cos(self.angle_moon)
        self.y = self.d_moon * sin(self.angle_moon)

        for i in range(self.n):
            self.a[i] += self.da[i]

            self.da[i] += self.d2a[i]

            self.d2a[i] = self.m_moon / self.r_earth * (self.x * sin(self.a[i]) - self.y * cos(self.a[i])) * (
                    ((self.x - self.r_earth * cos(self.a[i])) ** 2
                     + (self.y - self.r_earth * sin(self.a[i])) ** 2) ** - 1.5
                    - (self.x ** 2 + self.y ** 2) ** - 1.5
            ) - self.b * self.da[i]

        for i in range(1, self.n - 1):
            self.d2a[i] += self.k * (self.a[i - 1] + self.a[i + 1] - 2 * self.a[i])
        self.d2a[0] += self.k * (self.a[self.n - 1] + self.a[1] - 2 * self.a[0] - 2 * pi)
        self.d2a[self.n - 1] += self.k * (self.a[self.n - 2] + self.a[0] - 2 * self.a[self.n - 1] + 2 * pi)

    def draw(self):
        const = 5
        angle = [(self.a[i] - 2 * pi / self.n * i) * const + 2 * pi / self.n * i for i in range(self.n)]

        circle(screen, BROWN, [SCREEN_X / 2, SCREEN_Y / 2], self.r_earth)
        circle(screen, WHITE, [SCREEN_X / 2 + self.x, SCREEN_Y / 2 + self.y], 20)
        for a in angle:
            circle(screen, BLUE, [SCREEN_X / 2 + (self.r_earth + 3) * cos(a), SCREEN_Y / 2 + (self.r_earth + 3) * sin(a)], 3)

    def mainloop(self):
        finished = False
        while not finished:
            self.move()
            self.draw()
            pygame.display.update()
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True


if __name__ == "__main__":
    try:
        simulator = Simulator()
        simulator.mainloop()
    finally:
        pygame.quit()
