from init import *


class Bird:
    
    IMGS = BIRD_IMGS
    MAX_UPWARD_ANGLE = bird_max_upward_angle
    MAX_DOWNWARD_ANGLE = bird_max_downward_angle
    ANIMATION_TIME = bird_animation_time
    
    
    def __init__(self, x_position, y_position):
        self.bird_img = self.IMGS[0]
        self.x = x_position #the starting x position
        self.animation_time_count = 0 # This will be used to change the bird images eventually 
        self.y = y_position #the initial y position 
        self.fly_angle = 0 #initial flying angle 
        self.velocity = 0 
        self.time = 0 
        
         
        
    def move(self):
        self.time += 1 
        
        # D = V*t + (1/2)A*t^2
        displacement = self.velocity * self.time + (1/2) * bird_acceleration * self.time ** 2 
        
        #limit the max displacement of the bird
        if displacement > bird_max_displacement:
            displacement = bird_max_displacement
        
        self.y = self.y + displacement 
        
        #When the bird will fly upward i.e displacement < 0 
        if displacement < 0: 
            if self.fly_angle < self.MAX_UPWARD_ANGLE: 
                self.fly_angle += max(bird_angular_acceleration*(self.MAX_UPWARD_ANGLE - self.fly_angle), bird_min_incremental_angle) #accelerate the angle up
            else:
                self.fly_angle = self.MAX_UPWARD_ANGLE
                
        else: 
            if self.fly_angle > self.MAX_DOWNWARD_ANGLE: #if the flying angle is less than the maximum downward angle
                self.fly_angle -= abs(min(bird_angular_acceleration*(self.MAX_DOWNWARD_ANGLE - self.fly_angle), -bird_min_incremental_angle)) #accelerate the angle down
            else:
                self.fly_angle = self.MAX_DOWNWARD_ANGLE

    
    def jump(self):
        self.time = 0 
        self.velocity = bird_jump_velocity 
        
    
    #Return the rotated image and rotated rectangle 

    def animation(self):
        self.animation_time_count += 1

        # If the bird dives then the flapping of the wings needs to be prevented, else it should flap its wings periodically, this is done by the below block of code
        if self.fly_angle < -45:
            self.bird_img = self.IMGS[0]
            self.animation_time_count = 0 #reset the animation_time_count

        elif self.animation_time_count < self.ANIMATION_TIME:
            self.bird_img = self.IMGS[0]
        elif self.animation_time_count < self.ANIMATION_TIME * 2:
            self.bird_img = self.IMGS[1]
        elif self.animation_time_count < self.ANIMATION_TIME * 3:
            self.bird_img = self.IMGS[2]
        elif self.animation_time_count < self.ANIMATION_TIME * 4:
            self.bird_img = self.IMGS[1]
        else:
            self.bird_img = self.IMGS[0]
            self.animation_time_count = 0 

        rotated_image = pygame.transform.rotate(self.bird_img, self.fly_angle)
    
        origin_img_center = self.bird_img.get_rect(topleft = (self.x, self.y)).center
        rotated_rect = rotated_image.get_rect(center = origin_img_center)

        return rotated_image, rotated_rect


class Pipe:

    VELOCITY = pipe_velocity
    IMG_WIDTH = TOP_PIPE_IMG.get_width() 
    IMG_LENGTH = TOP_PIPE_IMG.get_height() 


    def __init__(self, x_position):                
        self.top_pipe_img = TOP_PIPE_IMG 
        self.bottom_pipe_img = BOTTOM_PIPE_IMG 
        self.x = x_position 
        self.bottom_pipe_topleft = 0 
        self.top_pipe_topleft = 0 
        self.top_pipe_height = 0 
        self.vertical_gap = random.randrange(100,250)
        self.random_height() 
        
        

    def move(self):
        self.x -= self.VELOCITY
    

    def random_height(self):
        
        self.top_pipe_height = random.randrange(top_pipe_min_height, top_pipe_max_height) #between the permissible limits defined in the ini.py file
        self.top_pipe_topleft = self.top_pipe_height - self.IMG_LENGTH 
        self.bottom_pipe_topleft = self.top_pipe_height + self.vertical_gap 




class Floor:
 
    IMGS = [FLOOR_IMG, FLOOR_IMG, FLOOR_IMG] 
    VELOCITY = floor_velocity 
    IMG_WIDTH = FLOOR_IMG.get_width() 

    def __init__(self, y_position):
  
        self.x1 = 0 
        self.x2 = self.IMG_WIDTH 
        self.x3 = self.IMG_WIDTH * 2 
        self.y = y_position 
        
  
    def move(self):
        self.x1 -= self.VELOCITY 
        self.x2 -= self.VELOCITY 
        self.x3 -= self.VELOCITY 
        
        if self.x1 + self.IMG_WIDTH < 0: # This condition means that the first floor image is no longer on the screen  
            self.x1 = self.x3 + self.IMG_WIDTH # stich the first floor image at the back of third floor image
        if self.x2 + self.IMG_WIDTH < 0: 
            self.x2 = self.x1 + self.IMG_WIDTH 
        if self.x3 + self.IMG_WIDTH < 0: 
            self.x3 = self.x2 + self.IMG_WIDTH 




