import pygame
import sys
from py import bird, pipe, landscape, settings


def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird.rect.colliderect(pipe):
            can_score = True
            death_sound.play()
            return False

    if bird.rect.top <= 0 or bird.rect.bottom >= landscape.floor_height:
        can_score = True
        death_sound.play()
        return False

    return True


def update_score():
    global score, can_score
    if pipe.all_pipes:
        for a_pipe in pipe.all_pipes:
            if bird.x - 5 < a_pipe.centerx < bird.x + 5 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if a_pipe.centerx < 0:
                can_score = True


def get_highscore(score, high_score):
    if score > high_score:
        high_score = score

    return high_score


def display_score():
    if active:
        score_surf = game_font.render(str(score), True, settings.WHITE)
        score_rect = score_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, 50))
        screen.blit(score_surf, score_rect)
    else:
        score_surf = game_font.render(f'Score: {score}', True, settings.WHITE)
        score_rect = score_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, 50))
        screen.blit(score_surf, score_rect)

        hscore_surf = game_font.render(f'High Score: {high_score}', True, settings.BLACK)
        hscore_rect = hscore_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, landscape.floor_height-25))
        screen.blit(hscore_surf, hscore_rect)


pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 32)

pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
pygame.display.set_icon(icon)

# Game Variables
active = True
score = 0
high_score = 0
can_score = True


BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 300)


SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1800)

flap_sound = pygame.mixer.Sound('sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sounds/sfx_point.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_PIPE:
            pipe.all_pipes.extend(pipe.get_pipe())
        if event.type == BIRD_FLAP:
            bird.surf, bird.rect = bird.animate_bird()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if active:
                    bird.movement = 0
                    bird.movement -= 7
                    flap_sound.play()

                else:
                    active = True
                    pipe.all_pipes.clear()
                    bird.movement = 0
                    bird.rect.center = (bird.x, settings.SCREEN_HEIGHT / 3 )
                    score = 0
                    can_score = True

    screen.blit(landscape.bg, (0, 0))

    if active:
        bird.movement += settings.gravity
        rotated_bird = bird.rotate_bird(bird.surf)
        bird.rect.centery += bird.movement
        screen.blit(rotated_bird, bird.rect)

        pipe.all_pipes = pipe.move_pipes(pipe.all_pipes)
        pipe.draw_pipes(screen, pipe.all_pipes)

        active = check_collision(pipe.all_pipes)
        update_score()

    else:
        screen.blit(landscape.game_over_surf, landscape.game_over_rect)
        high_score = get_highscore(score, high_score)

    landscape.floor_x -= 1
    landscape.draw_floor(screen)
    if landscape.floor_x <= -settings.SCREEN_WIDTH:
        landscape.floor_x = 0

    display_score()

    pygame.display.update()
    clock.tick(120)
