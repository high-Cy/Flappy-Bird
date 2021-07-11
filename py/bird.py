import pygame
from itertools import cycle
from py import settings

movement = 0

up = pygame.image.load('assets/yellowbird-upflap.png')
mid = pygame.image.load('assets/yellowbird-midflap.png')
down = pygame.image.load('assets/yellowbird-downflap.png')
cycle_img = cycle([up, mid, down])
surf = next(cycle_img)
x = 50
rect = surf.get_rect(center=(x, settings.SCREEN_HEIGHT / 3))


def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -movement * 3, 1)


def animate_bird():
    new = next(cycle_img)
    new_rect = new.get_rect(center=(x, rect.centery))
    return new, new_rect


if __name__ == '__main__':
    pass

