import pygame
import sys
import random
from itertools import cycle 
 
# Constants
SCREEN_WIDTH = 325
SCREEN_HEIGHT = 650

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_floor():
    screen.blit(floor_surf, (floor_x,floor_height))
    screen.blit(floor_surf, (floor_x + SCREEN_WIDTH ,floor_height))

def get_pipe():
    random_pipe_pos = random.choice(pipe_heights)
    top_pipe = pipe_surf.get_rect(midbottom=(SCREEN_WIDTH, random_pipe_pos-200))
    bot_pipe = pipe_surf.get_rect(midtop=(SCREEN_WIDTH, random_pipe_pos))
    return top_pipe, bot_pipe

def move_pipes(pipe_list):
    for pipe in pipe_list:
        pipe.centerx -= 2
        if pipe.centerx <= -SCREEN_WIDTH:
            pipe_list.remove(pipe)
    return pipe_list

def draw_pipes(pipe_list):
    for pipe in pipe_list:
        if pipe.bottom >= SCREEN_HEIGHT/2:
            screen.blit(pipe_surf, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surf, False, True)
            screen.blit(flip_pipe, pipe)

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement *3, 1)

def animate_bird():
    new_bird = next(bird_cycle)
    new_bird_rect = new_bird.get_rect(center = (bird_x,bird_rect.centery))
    return new_bird, new_bird_rect

def check_collision(pipe_list):
    global can_score
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            can_score = True
            return False
    
    if bird_rect.top <= 0 or bird_rect.bottom >= floor_height:
        can_score = True
        return False

    return True

def update_score():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if bird_x -5 < pipe.centerx < bird_x +5 and can_score:
                score += 1
                can_score = False 
            if pipe.centerx < 0:
                can_score = True

def get_highscore(score, high_score):
    if score > high_score:
        high_score = score

    return high_score

def display_score():
    if active:
        score_surf = game_font.render(str(score), True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH/2, 50))
        screen.blit(score_surf, score_rect)
    else:
        score_surf = game_font.render(f'Score: {score}', True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH/2, 50))
        screen.blit(score_surf, score_rect)

        new_hscore = get_highscore(score, high_score)
        hscore_surf = game_font.render(f'High Score: {new_hscore}', True, BLACK)
        hscore_rect = hscore_surf.get_rect(center=(SCREEN_WIDTH/2, 600))
        screen.blit(hscore_surf, hscore_rect)

def reset():
    active = True
    pipe_list.clear()
    bird_movement = 0
    bird_rect.center = (bird_x, SCREEN_HEIGHT/2)
    score = 0
    can_score =True
    
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 32)

# Game Variables
gravity = 0.2
bird_movement = 0
active = True
score = 0
high_score = 0
can_score = True

bg = pygame.image.load('assets/background-day.png').convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

floor_surf = pygame.image.load('assets/base.png').convert()
floor_x = 0
floor_height = 550

BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 300)
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_cycle = cycle([bird_up, bird_mid, bird_down])
bird_surf = next(bird_cycle)
bird_x = 50
bird_rect = bird_surf.get_rect(center=(bird_x, SCREEN_HEIGHT/2))


SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1800)
pipe_surf = pygame.image.load('assets/pipe-green.png').convert()
pipe_list =[]
pipe_heights = [300, 400, 500]


while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_PIPE:
            pipe_list.extend(get_pipe())
        if event.type == BIRD_FLAP:
            bird_surf, bird_rect = animate_bird()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if active:
                    bird_movement = 0
                    bird_movement -= 7 
                else:
                    active = True
                    pipe_list.clear()
                    bird_movement = 0
                    bird_rect.center = (bird_x, SCREEN_HEIGHT/2)
                    score = 0

    screen.blit(bg, (0,0))

    if active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surf)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        active = check_collision(pipe_list)
        update_score()

    floor_x -= 1
    draw_floor()
    if floor_x <= -SCREEN_WIDTH:
        floor_x = 0

    display_score()

    pygame.display.update()
    clock.tick(120)