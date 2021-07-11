import pygame
from random import choice
from py import settings

surf = pygame.image.load('assets/pipe-green.png')
all_pipes = []
heights = [250, 350, 450]


def get_pipe():
    random_pipe_pos = choice(heights)
    top_pipe = surf.get_rect(
        midbottom=(settings.SCREEN_WIDTH, random_pipe_pos - 200))
    bot_pipe = surf.get_rect(midtop=(settings.SCREEN_WIDTH, random_pipe_pos))
    return top_pipe, bot_pipe


def move_pipes(pipe_list):
    for pipe in pipe_list:
        pipe.centerx -= 2
        if pipe.centerx <= -settings.SCREEN_WIDTH:
            pipe_list.remove(pipe)
    return pipe_list


def draw_pipes(screen, pipe_list):
    for pipe in pipe_list:
        if pipe.bottom > settings.SCREEN_HEIGHT / 2:
            screen.blit(surf, pipe)
        else:
            flip_pipe = pygame.transform.flip(surf, False, True)
            screen.blit(flip_pipe, pipe)

if __name__ == '__main__':
    pass
