import pygame
from py import settings

bg = pygame.image.load('assets/background-day.png')
bg = pygame.transform.scale(bg, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

floor_surf = pygame.image.load('assets/base.png')
floor_x = 0
floor_height = 500

game_over_surf = pygame.image.load('assets/message.png')
game_over_rect = game_over_surf.get_rect(
    center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))


def draw_floor(screen):
    screen.blit(floor_surf, (floor_x, floor_height))
    screen.blit(floor_surf, (floor_x + settings.SCREEN_WIDTH, floor_height))


if __name__ == '__main__':
    pass
