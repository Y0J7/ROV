import pygame
import time
import os

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{pygame.display.Info().current_w-185},{pygame.display.Info().current_h-130}'
screen = pygame.display.set_mode((175, 100))
pygame.display.set_caption('ROV Control')

states = [0, 0, 0, 0]
prev_states = [0, 0, 0, 0]
speed = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    
    motion = "N"
    prev_keys = [0, 0, 0, 0]
    if keys != prev_keys:
        if keys[pygame.K_w]:
            motion = "F"
        if keys[pygame.K_s]:
            motion = "B"
        if keys[pygame.K_a]:
            motion = "L"
        if keys[pygame.K_d]:
            motion = "R"
#------------------------------------------------------
        if keys[pygame.K_1]:
            states[0] = 1
        if keys[pygame.K_2]:
            states[1] = 1 
        if keys[pygame.K_3]:
            states[2] = 1 
        if keys[pygame.K_4]:
            states[3] = 1 
        if keys[pygame.K_5]:
            states[0] = 0
        if keys[pygame.K_6]:
            states[1] = 0
        if keys[pygame.K_7]:
            states[2] = 0
        if keys[pygame.K_8]:
            states[3] = 0
#------------------------------------------------------
        if keys[pygame.K_UP]:
            if speed < 100:
                speed += 10
        if keys[pygame.K_DOWN]:
            if speed > 0:
                speed -= 10



    print(f"{motion},{states[0]},{states[1]},{states[2]},{states[3]}, {speed}%")
    time.sleep(0.1)