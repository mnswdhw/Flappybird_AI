import copy
import warnings
import graphviz
import matplotlib.pyplot as plt
import numpy as np
import neat
from init import *
from game_obj import *
from static_func import *
from visualize import *


generation = 0 
max_gen = 50 # exit if the game is not solved till 50 generations.
prob_threshold_to_jump = 0.8 
failed_punishment = 10 #how much to penalize for punishment? 


#get the index of the closest pipe to the bird
def get_index(pipes, birds):
    bird_x = birds[0].x
    list_distance = [pipe.x + pipe.IMG_WIDTH - bird_x for pipe in pipes]
    index = list_distance.index(min(i for i in list_distance if i >= 0)) 
    return index


def main(genomes, config):
    
    global generation, SCREEN
    screen = SCREEN
    generation += 1 
    
    score = 0 
    clock = pygame.time.Clock() 
    start_time = pygame.time.get_ticks() 
    
    floor = Floor(floor_starting_y_position) 
    pipes_list = [Pipe(pipe_starting_x_position + i * pipe_horizontal_gap) for i in range(pipe_max_num)] 
    
    genomes_list = [] 
    models_list = [] 
    birds_list = [] 
    
    for genome_id, genome in genomes: 
        birds_list.append(Bird(bird_starting_x_position, bird_starting_y_position)) 
        genome.fitness = 0 
        genomes_list.append(genome) 
        model = neat.nn.FeedForwardNetwork.create(genome, config) 
        models_list.append(model) 
        
    run = True
    
    while run is True: 
        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        
        #quit the game when score exceeds the max_score
        if score >= max_score or len(birds_list) == 0:
            run = False
            break
        
        game_time = round((pygame.time.get_ticks() - start_time)/1000, 2) 
        
        clock.tick(FPS) #By running the clock at FPS, we can limit the runtime speed of a game.
        
        floor.move() 
        
        pipe_input_index = get_index(pipes_list, birds_list) 
        
        passed_pipes = [] 
        for pipe in pipes_list:
            pipe.move() 
            if pipe.x + pipe.IMG_WIDTH < birds_list[0].x: 
                passed_pipes.append(pipe) 
                       
        score = len(passed_pipes) #score will be the number of passed pipes
        
        for index, bird in enumerate(birds_list):
            bird.move() 
            delta_x = bird.x - pipes_list[pipe_input_index].x #This is the horizontal distance between pipe and bird
            delta_y_top = bird.y - pipes_list[pipe_input_index].top_pipe_height #This is the vertical distance between top pipe and bird
            delta_y_bottom = bird.y - pipes_list[pipe_input_index].bottom_pipe_topleft #This is the vertical distance between bottom pipe and bird
            net_input = (delta_x, delta_y_top, delta_y_bottom)

            output = models_list[index].activate(net_input)
            
            if output[0] > prob_threshold_to_jump: 
                bird.jump() 
            
            bird_failed_bool, flag_offset = collide(bird, pipes_list[pipe_input_index], floor, screen) 

            start_temp = 0
            if score == 0 and bird_failed_bool and flag_offset == 1:

                start_temp = 0
            elif score == 0 and bird_failed_bool and flag_offset == 0:
                start_temp = 0.5

            genomes_list[index].fitness = game_time + score - bird_failed_bool * failed_punishment + start_temp
            
            if bird_failed_bool:
                models_list.pop(index) 
                genomes_list.pop(index) 
                birds_list.pop(index) 
        #draw each frame in the loop 
        draw_game(screen, birds_list, pipes_list, floor, score, generation, game_time) 
        





def run_NEAT(config_file):

    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation,
                                config_file)
    
   
    neat_pop = neat.population.Population(config)
    

    neat_pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    neat_pop.add_reporter(stats)
    
    #pass the main function to neat, to manipulate internally.
    neat_pop.run(main, max_gen)

    winner = stats.best_genome()
 
    node_names = {-1:'delta_x', -2: 'delta_y_top', -3:'delta_y_bottom', 0:'Jump or Not'}
    draw_net(config, winner, True, node_names = node_names)
    plot_stats(stats, ylog = False, view = True)
    plot_species(stats, view = True)
    
    print('\nBest genome:\n{!s}'.format(winner))


config_file = 'config-feedforward.txt'
run_NEAT(config_file)