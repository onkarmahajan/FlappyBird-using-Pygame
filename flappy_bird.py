import pygame
import sys
import random

def draw_floor():
    screen.blit(floor, (floor_x_pos, 450))
    screen.blit(floor, (floor_x_pos + 288, 450))

def create_pipe():
    pipe_height = random.choice(pipe_pos)
    bottom_pipe = pipe_surface.get_rect(midtop = (300, pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom = (300, pipe_height - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipe_list):
    for pipe in pipe_list:
        pipe.centerx -= 3
    visible_pipes = [pipe for pipe in pipe_list if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipe_list):
    for pipe in pipe_list:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collisions(pipe_list):
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            hit.play()
            allow = True
            return False
    
    if bird_rect.top <= -10 or bird_rect.bottom >= 450:
        hit.play()
        allow = True
        return False
    
    return True

def rotate_bird(bird_surface):
    rotate_surface = pygame.transform.rotozoom(bird_surface, -bird_movement*3, 1)
    return rotate_surface

def bird_animation(end):
    new_surface = bird_list[bird_index]

    if end == "off":
        new_surface_rect = new_surface.get_rect(center = (144, 280))
    elif end == "on":
        new_surface_rect = new_surface.get_rect(center = (50, bird_rect.centery))

    return new_surface, new_surface_rect

allow = True
high_score = 0

def pipe_score():
    global allow, score

    if pipe_list:
        for pipe in pipe_list:
            if 97 < pipe.centerx < 103 and allow:
                point.play()
                score += 1
                allow = False
            if pipe.centerx < 0:
                allow = True
    

def display_score(game_state):

    global high_score

    score_surface = game_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (144, 50))
    screen.blit(score_surface, score_rect)

    if game_state == "off":
        if score > high_score:
            high_score = score
        highscore_surface = game_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        highscore_rect = highscore_surface.get_rect(center = (144, 400))
        screen.blit(highscore_surface, highscore_rect)
        

pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19__.TTF', 20)

#background
bg_surface = pygame.image.load("background-day.png").convert()

#floor
floor = pygame.image.load("floor.png").convert()
floor_x_pos = 0

#bird
bird_surface_downflap = pygame.image.load("bluebird-downflap.png").convert_alpha()
bird_surface_midflap = pygame.image.load("bluebird-midflap.png").convert_alpha()
bird_surface_upflap = pygame.image.load("bluebird-upflap.png").convert_alpha()
bird_list = [bird_surface_downflap, bird_surface_midflap, bird_surface_upflap]
bird_index = 0
bird_surface = bird_list[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 300)

#pipes
pipe_surface = pygame.image.load("pipe-green.png").convert()
SPWANPIPE = pygame.USEREVENT
pygame.time.set_timer(SPWANPIPE, 1800)
pipe_list = []
pipe_pos = [200, 300, 400]

#game variables
gravity = 0.25
bird_movement = 0
game_on = False
score = 0

#gameover
gameover_surface = pygame.image.load("gameover.png").convert_alpha()
gameover_rect = gameover_surface.get_rect(center = (144, 230))

#audio
hit = pygame.mixer.Sound("audio_hit.wav")
wing = pygame.mixer.Sound("audio_wing.wav")
point = pygame.mixer.Sound("audio_point.wav")

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_on == True:
                wing.play()
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_on == False:
                game_on = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0

        if event.type == SPWANPIPE:
            new_pipe = create_pipe()
            pipe_list.extend(new_pipe)
        
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            if game_on == True:
                bird_surface, bird_rect = bird_animation("on")
            elif game_on == False:
                bird_surface, bird_rect = bird_animation("off")



    screen.blit(bg_surface, (0, 0))

    if game_on:

        #bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #score
        pipe_score()
        display_score("on")

        game_on = check_collisions(pipe_list)
    
    else:
        display_score("off")
        screen.blit(bird_surface, bird_rect)
        screen.blit(gameover_surface, gameover_rect)


    if floor_x_pos <= -288:
        floor_x_pos = 0

    floor_x_pos -= 1
    draw_floor()

    pygame.display.update()
    clock.tick(60)