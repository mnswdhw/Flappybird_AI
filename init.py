from __future__ import print_function
import pygame
import time
import random
import os

pygame.init()

SCREEN_WIDTH = 800    
SCREEN_HEIGHT = 550    
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


FONT = pygame.font.SysFont('comicsansms', 20)
FONT_COLOR = (255, 255, 255) 


BIRD_IMGS = [pygame.image.load('images/Flappy Bird.png'),
             pygame.image.load('images/Flappy Bird Wings Up.png'),
             pygame.image.load('images/Flappy Bird Wings Down.png')]
BOTTOM_PIPE_IMG = pygame.image.load('images/Super Mario pipe.png')
TOP_PIPE_IMG = pygame.transform.flip(BOTTOM_PIPE_IMG, False, True) 
FLOOR_IMG = pygame.image.load('images/Stone Floor.png')
BG_IMG = pygame.transform.scale(pygame.image.load('images/1.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))

#defining constants
FPS = 30 
max_score = 100


floor_velocity = 5 #this velocity should be equal to the pipe velocity
floor_starting_y_position = 500 

pipe_max_num = 100 #maximum number of pipes equal to the max score 
pipe_vertical_gap = 150 
pipe_horizontal_gap = 200 #gap between pair of pipes
pipe_velocity = 5 
top_pipe_min_height = 100 
top_pipe_max_height = 200 
pipe_starting_x_position = 500 


bird_max_upward_angle = 35
bird_jump_velocity = -8 
bird_max_downward_angle = -90 
bird_angular_acceleration = 0.3
bird_starting_x_position = 150 
bird_min_incremental_angle = 5 
bird_animation_time = 1 
bird_acceleration = 3 
bird_max_displacement = 12 
bird_starting_y_position = 250 



