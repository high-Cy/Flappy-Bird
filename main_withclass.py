import pygame
import sys
import random
from itertools import cycle 

# Constants
SCREEN_WIDTH = 325
SCREEN_HEIGHT = 650

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Bird:
    bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
    bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
    bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
    bird_x = 50 
    bird_cycle = cycle([bird_up, bird_mid, bird_down])
    bird_surf = next(bird_cycle)
    bird_rect = bird_surf.get_rect(center=(bird_x, SCREEN_HEIGHT/2))

    def __init__(self):
        self.bird_movement = 0

    def rotate_bird(self):
        return pygame.transform.rotozoom(self.bird_surf, -self.bird_movement *3, 1)

    def animate_bird(self):
        new_bird = next(self.bird_cycle)
        new_bird_rect = new_bird.get_rect(center = (self.bird_x,self.bird_rect.centery))
        return new_bird, new_bird_rect

class Pipe:
    pipe_surf = pygame.image.load('assets/pipe-green.png').convert()
    pipe_list =[]
    pipe_heights = [300, 400, 500]

    def get_pipe(self):
        rand_pos = random.choice(self.pipe_heights)
        top_pipe = self.pipe_surf.get_rect(midbottom=(SCREEN_WIDTH, rand_pos-200))
        bot_pipe = self.pipe_surf.get_rect(midtop=(SCREEN_WIDTH, rand_pos))
        return top_pipe, bot_pipe

    def move_pipes(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 2
        return self.pipe_list

    def draw_pipes(self):
        for pipe in self.pipe_list:
            if pipe.bottom >= SCREEN_HEIGHT/2:
                screen.blit(self.pipe_surf, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surf, False, True)
                screen.blit(flip_pipe, pipe)

class Landscape:
    bg = pygame.image.load('assets/background-day.png').convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    floor_surf = pygame.image.load('assets/base.png').convert()
    floor_x = 0
    floor_height = 550

    def draw_floor(self):
        screen.blit(self.floor_surf, (self.floor_x,self.floor_height))
        screen.blit(self.floor_surf, (self.floor_x + SCREEN_WIDTH ,self.floor_height))

class Main:
    def __init__(self):
        self.bird = Bird()
        self.pipe = Pipe()
        self.landscape = Landscape()
        self.gravity = 0.25
        self.active = True
        self.score = 0
        self.high_score = 0

    def check_collision(self):
        for pipe in self.pipe.pipe_list:
            if self.bird.bird_rect.colliderect(pipe):
                return False
        
        if self.bird.bird_rect.top <= 0 or self.bird.bird_rect.bottom >= self.landscape.floor_height:
            return False

        return True

    def reset(self):
        active = True
        pipe_list.clear()
        bird_movement = 0
        bird_rect.center = (self.bird.bird_x, SCREEN_HEIGHT/2)
        score = 0

BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 300)

SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)

game = Main()
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_PIPE:
            pipe_list.extend(game.pipe.get_pipe())
        if event.type == BIRD_FLAP:
            bird_surf, bird_rect = game.bird.animate_bird()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if active:
                    game.bird.bird_movement = 0
                    game.bird.bird_movement -= 5 
                else:
                    game.active = True
                    pipe_list.clear()
                    game.bird.bird_movement = 0
                    game.bird.bird_rect.center = (game.bird.bird_x, SCREEN_HEIGHT/2)


    screen.blit(game.landscape.bg, (0,0))

    if game.active:
        game.bird.bird_movement += game.gravity
        rotated_bird = game.bird.rotate_bird()
        game.bird.bird_rect.centery += game.bird.bird_movement
        screen.blit(rotated_bird, game.bird.bird_rect)

        pipe_list = game.pipe.move_pipes()
        game.pipe.draw_pipes()

        active = game.check_collision()
         
    game.landscape.floor_x -= 1
    game.landscape.draw_floor()
    if game.landscape.floor_x <= -SCREEN_WIDTH:
        game.landscape.floor_x = 0

    pygame.display.update()
    clock.tick(60)