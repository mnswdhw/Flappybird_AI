import matplotlib.pyplot as plt
import numpy as np
from init import *
from game_obj import *
from static_func import *
from visualize import *

from deep_hyperneat.genome import Genome
from deep_hyperneat.population import Population
from deep_hyperneat.phenomes import FeedForwardCPPN as CPPN
from deep_hyperneat.decode import decode
from deep_hyperneat.visualize import draw_net



sub_in_dims = [1,2]
sub_sh_dims = [1,3]
sub_o_dims = 1

goal_fitness= 200
pop_key = 0
pop_size = 5
pop_elitism = 1
num_generations = 50



generation = 0 
prob_threshold_to_jump = 0.8 
failed_punishment = 10 


def get_index(pipes, birds):
    bird_x = birds[0].x
    list_distance = [pipe.x + pipe.IMG_WIDTH - bird_x for pipe in pipes]
    index = list_distance.index(min(i for i in list_distance if i >= 0)) 
    return index



def main(genomes):
    
    global generation, SCREEN 
    screen = SCREEN
    generation += 1 
    
    score = 0 
    clock = pygame.time.Clock() 
    start_time = pygame.time.get_ticks() 
    
    floor = Floor(floor_starting_y_position) 
    pipes_list = [Pipe(pipe_starting_x_position + i * pipe_horizontal_gap) for i in range(pipe_max_num)] 
    
    models_list = [] 
    genomes_list = [] 
    birds_list = [] 
    
    for genome_id, genome in genomes: 

        cppn = CPPN.create(genome)
        substrate = decode(cppn,sub_in_dims,sub_o_dims,sub_sh_dims)
        birds_list.append(Bird(bird_starting_x_position, bird_starting_y_position)) 
        genome.fitness = 0 
        genomes_list.append(genome) 
        models_list.append(substrate) 
        
    run = True
    
    while run is True: 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        
        if score >= max_score or len(birds_list) == 0:
            run = False
            break
        
        game_time = round((pygame.time.get_ticks() - start_time)/1000, 2) 
        clock.tick(FPS) 
        
        floor.move() 
        
        pipe_input_index = get_index(pipes_list, birds_list) #het the index of the pipe closest to the bird 
        
        passed_pipes = [] 
        for pipe in pipes_list:
            pipe.move() 
            if pipe.x + pipe.IMG_WIDTH < birds_list[0].x:
                passed_pipes.append(pipe) 
                       
        score = len(passed_pipes) #the score of the game is the number of pipes passed successfully by the bird 
        
        for index, bird in enumerate(birds_list):
            bird.move() 
            delta_x = bird.x - pipes_list[pipe_input_index].x 
            delta_y_top = bird.y - pipes_list[pipe_input_index].top_pipe_height 
            delta_y_bottom = bird.y - pipes_list[pipe_input_index].bottom_pipe_topleft 
            net_input = (delta_x, delta_y_top, delta_y_bottom)
            output = models_list[index].activate(net_input)
            
            if output[0] > prob_threshold_to_jump: 
                bird.jump() 
            
            bird_failed_bool,flag_offset = collide(bird, pipes_list[pipe_input_index], floor, screen) 

            start_temp = 0

            # if score == 0 and bird_failed_bool and flag_offset == 1:

            #     start_temp = 0
            # elif score == 0 and bird_failed_bool and flag_offset == 0:
            #     start_temp = 0.5
            
            genomes_list[index].fitness = game_time + score - bird_failed_bool * failed_punishment 
            
            if bird_failed_bool:
                models_list.pop(index) 
                genomes_list.pop(index) 
                birds_list.pop(index) 

        draw_game(screen, birds_list, pipes_list, floor, score, generation, game_time) 
        





def run_hyperNEAT():
    
    pop = Population(pop_key,pop_size,pop_elitism)
    

    winner_genome = pop.run(main,goal_fitness,num_generations)
    cppn = CPPN.create(winner_genome)
    
    substrate = decode(cppn,sub_in_dims,sub_o_dims,sub_sh_dims)

    draw_net(cppn, filename="reports/flappy_cpnn")
    draw_net(substrate, filename="reports/flappy_substrate")

    print("\nChampion Genome: {} with Fitness {}\n".format(winner_genome.key,winner_genome.fitness))


run_hyperNEAT()