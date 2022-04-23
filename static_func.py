from init import *


def collide(bird, pipe, floor, screen):
    
    #below will create a mask object, all the opaque pixels are set and transparent pixels are ignored 

    bird_mask = pygame.mask.from_surface(bird.bird_img) 
    top_pipe_mask = pygame.mask.from_surface(pipe.top_pipe_img) 
    bottom_pipe_mask = pygame.mask.from_surface(pipe.bottom_pipe_img) 
    
    sky_height = 0 #upper collision limit
    floor_height = floor.y #lower collision limit
    bird_lower_end = bird.y + bird.bird_img.get_height() 
    

    top_pipe_offset = (round(pipe.x - bird.x), round(pipe.top_pipe_topleft - bird.y))
    bottom_pipe_offset = (round(pipe.x - bird.x), round(pipe.bottom_pipe_topleft - bird.y))
    
    top_pipe_intersection_point = bird_mask.overlap(top_pipe_mask, top_pipe_offset)
    bottom_pipe_intersection_point = bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset)

    flag = 0

    if top_pipe_intersection_point is not None or bottom_pipe_intersection_point is not None :
        return (True,flag)
    elif bird_lower_end > floor_height or bird.y < sky_height:
        flag = 1
        return (True,flag)
    else:
        return (False,flag)


def draw_game(screen, birds, pipes, floor, score, generation, game_time):
    
    #screen.blit is used to draw on the pygame window
    screen.blit(BG_IMG, (0, 0))
    

    screen.blit(floor.IMGS[0], (floor.x1, floor.y)) 
    screen.blit(floor.IMGS[1], (floor.x2, floor.y)) 
    screen.blit(floor.IMGS[2], (floor.x3, floor.y)) 
    

    for pipe in pipes:
        screen.blit(pipe.top_pipe_img, (pipe.x, pipe.top_pipe_topleft)) 
        screen.blit(pipe.bottom_pipe_img, (pipe.x, pipe.bottom_pipe_topleft)) 
    
    for bird in birds:
        rotated_image, rotated_rect = bird.animation()
        screen.blit(rotated_image, rotated_rect)
    
    #Styling options 
    score_text = FONT.render('Score: ' + str(score), 1, FONT_COLOR) 
    screen.blit(score_text, (SCREEN_WIDTH - 15 - score_text.get_width(), 15)) 
    
    game_time_text = FONT.render('Timer: ' + str(game_time) + ' s', 1, FONT_COLOR) 
    screen.blit(game_time_text, (SCREEN_WIDTH - 15 - game_time_text.get_width(), 15 + score_text.get_height())) 
    
    generation_text = FONT.render('Generation: ' + str(generation - 1), 1, FONT_COLOR)
    screen.blit(generation_text, (15, 15)) 
    
    bird_text = FONT.render('Birds Alive: ' + str(len(birds)), 1, FONT_COLOR) 
    screen.blit(bird_text, (15, 15 + generation_text.get_height())) 
    
    progress_text = FONT.render('Pipes Remained: ' + str(len(pipes) - score), 1, FONT_COLOR) 
    screen.blit(progress_text, (15, 15 + generation_text.get_height() + bird_text.get_height())) 
    
    pygame.display.update() 