import pygame, random
from pygame.locals import *

pygame.init()

CLOCK = pygame.time.Clock()

WINDOW = pygame.display.set_mode((800,600))
pygame.display.set_caption('Pong')

DISPLAY = pygame.Surface((200, 150))

MENU = 'home' # home, play, pause
MATCH_TIME = 0

class Ball:
    def __init__(self, entity_name: str, position: list = [0,0], size: list = [0,0], default_action: str = 'idle'):
        self.__actions = self.__load_actions(entity_name)
        self.__action_frame = 0
        self.__action_default = default_action
        self.__action_current = default_action
        self.__position = position
        self.__size = size
        self.__rect = pygame.Rect(int(self.__position[0]), int(self.__position[1]), self.__size[0], self.__size[1])
        self.movement = [random.choice([-1.5, 1.5]), 0]
        self.hit_count = 0

    # Loads all the entity actions
    def __load_actions(self, entity_name) -> dict :
        actions = {} # Create the entity actions dict
        actions_file = open(f'assets/entities/{entity_name}/actions.txt', 'r') # Opens the file with the actions declarations
        actions_decls = actions_file.read().splitlines() # Gets each declaration
        actions_file.close() # Closes the file

        for action_decl in actions_decls: # Iterates for each declaration
            action_decl = action_decl.split(' ') # Splits the string into each element
            action_name = action_decl[0] # Gets the action name, it's the first element
            action_mode = action_decl[1] # Gets the action mode loop or once
            action_decl.remove(action_decl[0]) # Removes the action name to keep just the action frames times and the action mode
            action_decl.remove(action_decl[0]) # Removes the action mode to keep just the action frames times
            action_images = [] # A List to contain all images

            for i in range(len(action_decl)):
                for j in range(int(action_decl[i])):
                    # Adding the image to the list of images
                    action_images.append(pygame.image.load(f'assets/entities/{entity_name}/{action_name}/{action_name}_{i}.png'))

            actions[action_name] = [action_images, action_mode]
        
        return actions

    # Sets the action
    # If it's playing a loop action, this action can be interrupted to play another action and the frame count is restarted
    # If it's playing a once play action, the action can be interrupted, but if you set force to True, so the action will be interrupted
    def set_action(self, action_name, force: bool = False):
        if self.__actions[self.__action_current][1] == 'loop':
            if self.__action_current != action_name:
                self.__action_frame = 0
                self.__action_current = action_name
            elif force:
                self.__action_frame = 0
        elif force:
            self.__action_current = action_name
            self.__action_frame = 0

    def get_rect(self) -> pygame.Rect:
        return self.__rect

    def set_position(self, position):
        self.__position[0] = position[0]
        self.__position[1] = position[1]
        self.__update_rect()
    
    def __update_rect(self): # Updates the object rect x, y, width and height
        self.__rect = pygame.Rect(int(self.__position[0]), int(self.__position[1]), self.__size[0], self.__size[1])

    def apply_movement(self, movement): # Apply movement to the player
        self.__position[0] += movement[0]
        self.__position[1] += movement[1]
        self.__update_rect()
    
    def next_frame(self): # Updates the current action
        self.__action_frame += 1
        if self.__action_frame > len(self.__actions[self.__action_current][0]) - 1:
            if self.__actions[self.__action_current][1] == 'once': # If the action is a once play action, when it ends will auto set to the default action
                self.set_action(self.__action_default, True)
            self.__action_frame = 0 
    
    def render(self, camera: pygame.Surface):
        camera.blit(self.__actions[self.__action_current][0][self.__action_frame], self.__position)

    def reset(self):
        self.score = 0
        self.__position[0] = 98
        self.__position[1] = 73
        self.__update_rect()
        self.movement = [random.choice([-1.5, 1.5]), 0]

    def update(self):
        self.next_frame()
        self.apply_movement(self.movement)
        if self.__rect.top < 1 or self.__rect.bottom > 149:
            self.movement[1] *= -1
            self.set_action('hit', True)

class Bar:
    def __init__(self, entity_name: str, position: list = [0,0], size: list = [0,0], player_control: dict = None, move_condition = None,  default_action: str = 'idle'):
        self.__actions = self.__load_actions(entity_name)
        self.__action_frame = 0
        self.__action_default = default_action
        self.__action_current = default_action
        self.__position = position
        self.__size = size
        self.__rect = pygame.Rect(int(self.__position[0]), int(self.__position[1]), self.__size[0], self.__size[1])
        self.__player_control = player_control
        self.__move_condition = move_condition
        self.__accuracy_error = random.randint(-8, 9)
        self.target_point = 74
        self.score = 0

    # Loads all the entity actions
    def __load_actions(self, entity_name) -> dict :
        actions = {} # Create the entity actions dict
        actions_file = open(f'assets/entities/{entity_name}/actions.txt', 'r') # Opens the file with the actions declarations
        actions_decls = actions_file.read().splitlines() # Gets each declaration
        actions_file.close() # Closes the file

        for action_decl in actions_decls: # Iterates for each declaration
            action_decl = action_decl.split(' ') # Splits the string into each element
            action_name = action_decl[0] # Gets the action name, it's the first element
            action_mode = action_decl[1] # Gets the action mode loop or once
            action_decl.remove(action_decl[0]) # Removes the action name to keep just the action frames times and the action mode
            action_decl.remove(action_decl[0]) # Removes the action mode to keep just the action frames times
            action_images = [] # A List to contain all images

            for i in range(len(action_decl)):
                for j in range(int(action_decl[i])):
                    # Adding the image to the list of images
                    action_images.append(pygame.image.load(f'assets/entities/{entity_name}/{action_name}/{action_name}_{i}.png'))

            actions[action_name] = [action_images, action_mode]
        
        return actions

    # Sets the action
    # If it's playing a loop action, this action can be interrupted to play another action and the frame count is restarted
    # If it's playing a once play action, the action can be interrupted, but if you set force to True, so the action will be interrupted
    def set_action(self, action_name, force: bool = False):
        if self.__actions[self.__action_current][1] == 'loop':
            if self.__action_current != action_name:
                self.__action_frame = 0
                self.__action_current = action_name
            elif force:
                self.__action_frame = 0
        elif force:
            self.__action_current = action_name
            self.__action_frame = 0
    
    def __update_rect(self): # Updates the object rect x, y, width and height
        self.__rect = pygame.Rect(int(self.__position[0]), int(self.__position[1]), self.__size[0], self.__size[1])

    def apply_movement(self, movement): # Apply movement to the player
        self.__position[0] += movement[0]
        self.__position[1] += movement[1]
        self.__update_rect()
    
    def next_frame(self): # Updates the current action
        self.__action_frame += 1
        if self.__action_frame > len(self.__actions[self.__action_current][0]) - 1:
            if self.__actions[self.__action_current][1] == 'once': # If the action is a once play action, when it ends will auto set to the default action
                self.set_action(self.__action_default, True)
            self.__action_frame = 0
    
    def render(self, camera: pygame.Surface):
        camera.blit(self.__actions[self.__action_current][0][self.__action_frame], self.__position)

    def get_rect(self):
        return self.__rect

    def set_control_mode(self, mode: dict, move_condition = None):
        # mode = None: IA, dict: Player
        # side = None: Player, 0: Right Side, 1: Left Side
        self.__player_control = mode
        self.__move_condition = move_condition
    
    def update_target_point(self, ball: Ball):
        dx = self.__rect.centerx - ball.get_rect().centerx
        dt = int(dx / ball.movement[0])

        yi = ball.get_rect().centery

        dy = ball.movement[1] * dt

        yf = yi + dy

        while yf < 0 or yf > 150:
            if yf < 0:
                yf *= -1
            elif yf > 150:
                yf = 300 - yf
        
        self.target_point = yf

        return self.target_point

    def reset(self):
        self.score = 0
        self.__rect.y = 63

    def update(self, ball: Ball):
        self.next_frame()

        if self.__player_control: # Player control system
            pressed_keys = pygame.key.get_pressed()
            y_movement = (pressed_keys[self.__player_control['down']] - pressed_keys[self.__player_control['up']])
            self.apply_movement([0, y_movement])
        else: # IA control system
            if self.__move_condition(ball.movement[0]):
                delta_y = ball.get_rect().centery - self.__rect.centery + self.__accuracy_error # Gets to where the ball is going
                delta_x = ball.get_rect().centerx - self.__rect.centerx
            
                if delta_x > -70 and delta_x < 70:
                    if self.target_point > self.__rect.centery + self.__accuracy_error: 
                        self.apply_movement([0, 1])
                    elif self.target_point < self.__rect.centery + self.__accuracy_error:
                        self.apply_movement([0, -1])
                else:
                    if delta_y > 0:
                        self.apply_movement([0, 1])
                    elif delta_y < 0: 
                        self.apply_movement([0, -1])
            else:
                if self.__rect.centery > 75 + self.__accuracy_error:
                    self.apply_movement([0, -1])
                elif self.__rect.centery < 75 + self.__accuracy_error:
                    self.apply_movement([0, 1])
        
        if self.__rect.colliderect(ball.get_rect()): # Gets wherever the ball collides with the bars
            ball.movement[0] *= -1
            ball_y = ball.get_rect().y - ( ball.get_rect().height / 2 ) - 32.5
            self_y = self.__rect.y - ( self.__rect.height / 2 ) - 12.5
            delta_y = ball_y - self_y
            ball.movement[1] += delta_y / 12 # Sets the ball movement

            if ball.movement[0] > 0:
                ball.movement[0] += int( ball.hit_count / 15 ) / 2
            elif ball.movement[0] < 0:
                ball.movement[0] -= int( ball.hit_count / 15 ) / 2

            self.__accuracy_error = random.randint(-8, 9)

            self.set_action('hit', True) # Change the current bar action
            ball.set_action('hit', True) # Change the ball action
            ball.hit_count += 1 # Counter to increase the ball speed

class ScoreParticle:
    def __init__(self, entity_name: str, position: list = [0,0], size: list = [0,0], default_action: str = 'idle'):
        self.__actions = self.__load_actions(entity_name)
        self.__action_frame = 0
        self.__action_default = default_action
        self.__action_current = default_action
        self.__position = position
        self.__size = size
        self.__rect = pygame.Rect(int(self.__position[0]), int(self.__position[1]), self.__size[0], self.__size[1])
        self.is_living = 2

    # Loads all the entity actions
    def __load_actions(self, entity_name) -> dict :
        actions = {} # Create the entity actions dict
        actions_file = open(f'assets/entities/{entity_name}/actions.txt', 'r') # Opens the file with the actions declarations
        actions_decls = actions_file.read().splitlines() # Gets each declaration
        actions_file.close() # Closes the file

        for action_decl in actions_decls: # Iterates for each declaration
            action_decl = action_decl.split(' ') # Splits the string into each element
            action_name = action_decl[0] # Gets the action name, it's the first element
            action_mode = action_decl[1] # Gets the action mode loop or once
            action_decl.remove(action_decl[0]) # Removes the action name to keep just the action frames times and the action mode
            action_decl.remove(action_decl[0]) # Removes the action mode to keep just the action frames times
            action_images = [] # A List to contain all images

            for i in range(len(action_decl)):
                for j in range(int(action_decl[i])):
                    # Adding the image to the list of images
                    action_images.append(pygame.image.load(f'assets/entities/{entity_name}/{action_name}/{action_name}_{i}.png'))

            actions[action_name] = [action_images, action_mode]
        
        return actions
    
    def next_frame(self): # Updates the current action
        self.__action_frame += 1
        if self.__action_frame > len(self.__actions[self.__action_current][0]) - 1:
            if self.__actions[self.__action_current][1] == 'once': # If the action is a once play action, when it ends will auto set to the default action
                self.set_action(self.__action_default, True)
            self.__action_frame = 0
            self.is_living -= 1
    
    def render(self, camera: pygame.Surface):
        camera.blit(self.__actions[self.__action_current][0][self.__action_frame], self.__position)

    def update(self):
        self.next_frame()

class ResumeButton:
    def __init__(self, position: list, size: list, button_name, default_action = 'normal'):
        self.__position = position
        self.__size = size
        self.__rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.__actions = self.__load_actions(button_name)
        self.__action_frame = 0
        self.__action_default = default_action
        self.__action_current = default_action

    # Loads all the entity actions
    def __load_actions(self, button_name: str):
        actions = {} # Create the entity actions dict
        actions_file = open(f'assets/ui/{button_name}/actions.txt', 'r') # Opens the file with the actions declarations
        actions_decls = actions_file.read().splitlines() # Gets each declaration
        actions_file.close() # Closes the file

        for action_decl in actions_decls: # Iterates for each declaration
            action_decl = action_decl.split(' ') # Splits the string into each element
            action_name = action_decl[0] # Gets the action name, it's the first element
            action_mode = action_decl[1] # Gets the action mode loop or once
            action_decl.remove(action_decl[0]) # Removes the action name to keep just the action frames times and the action mode
            action_decl.remove(action_decl[0]) # Removes the action mode to keep just the action frames times
            action_images = [] # A List to contain all images

            for i in range(len(action_decl)):
                for j in range(int(action_decl[i])):
                    # Adding the image to the list of images
                    action_images.append(pygame.image.load(f'assets/ui/{button_name}/{action_name}/{action_name}_{i}.png'))

            actions[action_name] = [action_images, action_mode]
        
        return actions

    # Sets the action
    # If it's playing a loop action, this action can be interrupted to play another action and the frame count is restarted
    # If it's playing a once play action, the action can be interrupted, but if you set force to True, so the action will be interrupted
    def set_action(self, action_name, force: bool = False):
        if self.__actions[self.__action_current][1] == 'loop':
            if self.__action_current != action_name:
                self.__action_frame = 0
                self.__action_current = action_name
            elif force:
                self.__action_frame = 0
        elif force:
            self.__action_current = action_name
            self.__action_frame = 0
    
    def next_frame(self): # Updates the current action
        self.__action_frame += 1
        if self.__action_frame > len(self.__actions[self.__action_current][0]) - 1:
            if self.__actions[self.__action_current][1] == 'once': # If the action is a once play action, when it ends will auto set to the default action
                self.set_action(self.__action_default, True)
            self.__action_frame = 0
    
    def render(self, camera: pygame.Surface):
        camera.blit(self.__actions[self.__action_current][0][self.__action_frame], self.__position)

    def get_rect(self):
        return self.__rect

    def __on_click(self):
        global MENU
        MENU = 'play'

    def update(self):
        self.next_frame()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]/4, mouse_pos[1]/4)
        hover = self.__rect.right >= mouse_pos[0] and mouse_pos[0] >= self.__rect.left and self.__rect.bottom >= mouse_pos[1] and mouse_pos[1] >= self.__rect.top
        if hover:
            self.set_action('hover')
            if pygame.mouse.get_pressed(3)[0]:
                self.__on_click()
                self.set_action('click', True)

class PlayButton:
    def __init__(self, position: list, size: list, button_name, default_action = 'normal'):
        self.__position = position
        self.__size = size
        self.__rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.__actions = self.__load_actions(button_name)
        self.__action_frame = 0
        self.__action_default = default_action
        self.__action_current = default_action

    # Loads all the entity actions
    def __load_actions(self, button_name: str):
        actions = {} # Create the entity actions dict
        actions_file = open(f'assets/ui/{button_name}/actions.txt', 'r') # Opens the file with the actions declarations
        actions_decls = actions_file.read().splitlines() # Gets each declaration
        actions_file.close() # Closes the file

        for action_decl in actions_decls: # Iterates for each declaration
            action_decl = action_decl.split(' ') # Splits the string into each element
            action_name = action_decl[0] # Gets the action name, it's the first element
            action_mode = action_decl[1] # Gets the action mode loop or once
            action_decl.remove(action_decl[0]) # Removes the action name to keep just the action frames times and the action mode
            action_decl.remove(action_decl[0]) # Removes the action mode to keep just the action frames times
            action_images = [] # A List to contain all images

            for i in range(len(action_decl)):
                for j in range(int(action_decl[i])):
                    # Adding the image to the list of images
                    action_images.append(pygame.image.load(f'assets/ui/{button_name}/{action_name}/{action_name}_{i}.png'))

            actions[action_name] = [action_images, action_mode]
        
        return actions

    # Sets the action
    # If it's playing a loop action, this action can be interrupted to play another action and the frame count is restarted
    # If it's playing a once play action, the action can be interrupted, but if you set force to True, so the action will be interrupted
    def set_action(self, action_name, force: bool = False):
        if self.__actions[self.__action_current][1] == 'loop':
            if self.__action_current != action_name:
                self.__action_frame = 0
                self.__action_current = action_name
            elif force:
                self.__action_frame = 0
        elif force:
            self.__action_current = action_name
            self.__action_frame = 0
    
    def next_frame(self): # Updates the current action
        self.__action_frame += 1
        if self.__action_frame > len(self.__actions[self.__action_current][0]) - 1:
            if self.__actions[self.__action_current][1] == 'once': # If the action is a once play action, when it ends will auto set to the default action
                self.set_action(self.__action_default, True)
            self.__action_frame = 0
    
    def render(self, camera: pygame.Surface):
        camera.blit(self.__actions[self.__action_current][0][self.__action_frame], self.__position)

    def get_rect(self):
        return self.__rect

    def __on_click(self):
        global MENU, red_bar, blue_bar, ball, MATCH_TIME
        MENU = 'play'
        red_bar.reset()
        blue_bar.reset()
        ball.reset()
        MATCH_TIME = 0

    def update(self):
        self.next_frame()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]/4, mouse_pos[1]/4)
        hover = self.__rect.right >= mouse_pos[0] and mouse_pos[0] >= self.__rect.left and self.__rect.bottom >= mouse_pos[1] and mouse_pos[1] >= self.__rect.top
        if hover:
            self.set_action('hover')
            if pygame.mouse.get_pressed(3)[0]:
                self.__on_click()
                self.set_action('click', True)

class ExitButton:
    def __init__(self, position: list, size: list, button_name, default_action = 'normal'):
        self.__position = position
        self.__size = size
        self.__rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.__actions = self.__load_actions(button_name)
        self.__action_frame = 0
        self.__action_default = default_action
        self.__action_current = default_action

    # Loads all the entity actions
    def __load_actions(self, button_name: str):
        actions = {} # Create the entity actions dict
        actions_file = open(f'assets/ui/{button_name}/actions.txt', 'r') # Opens the file with the actions declarations
        actions_decls = actions_file.read().splitlines() # Gets each declaration
        actions_file.close() # Closes the file

        for action_decl in actions_decls: # Iterates for each declaration
            action_decl = action_decl.split(' ') # Splits the string into each element
            action_name = action_decl[0] # Gets the action name, it's the first element
            action_mode = action_decl[1] # Gets the action mode loop or once
            action_decl.remove(action_decl[0]) # Removes the action name to keep just the action frames times and the action mode
            action_decl.remove(action_decl[0]) # Removes the action mode to keep just the action frames times
            action_images = [] # A List to contain all images

            for i in range(len(action_decl)):
                for j in range(int(action_decl[i])):
                    # Adding the image to the list of images
                    action_images.append(pygame.image.load(f'assets/ui/{button_name}/{action_name}/{action_name}_{i}.png'))

            actions[action_name] = [action_images, action_mode]
        
        return actions

    # Sets the action
    # If it's playing a loop action, this action can be interrupted to play another action and the frame count is restarted
    # If it's playing a once play action, the action can be interrupted, but if you set force to True, so the action will be interrupted
    def set_action(self, action_name, force: bool = False):
        if self.__actions[self.__action_current][1] == 'loop':
            if self.__action_current != action_name:
                self.__action_frame = 0
                self.__action_current = action_name
            elif force:
                self.__action_frame = 0
        elif force:
            self.__action_current = action_name
            self.__action_frame = 0
    
    def next_frame(self): # Updates the current action
        self.__action_frame += 1
        if self.__action_frame > len(self.__actions[self.__action_current][0]) - 1:
            if self.__actions[self.__action_current][1] == 'once': # If the action is a once play action, when it ends will auto set to the default action
                self.set_action(self.__action_default, True)
            self.__action_frame = 0
    
    def render(self, camera: pygame.Surface):
        camera.blit(self.__actions[self.__action_current][0][self.__action_frame], self.__position)

    def get_rect(self):
        return self.__rect

    def __on_click(self):
        pygame.quit()
        quit()

    def update(self):
        self.next_frame()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]/4, mouse_pos[1]/4)
        hover = self.__rect.right >= mouse_pos[0] and mouse_pos[0] >= self.__rect.left and self.__rect.bottom >= mouse_pos[1] and mouse_pos[1] >= self.__rect.top
        if hover:
            self.set_action('hover')
            if pygame.mouse.get_pressed(3)[0]:
                self.__on_click()
                self.set_action('click', True)

class HomeButton:
    def __init__(self, position: list, size: list, button_name, default_action = 'normal'):
        self.__position = position
        self.__size = size
        self.__rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.__actions = self.__load_actions(button_name)
        self.__action_frame = 0
        self.__action_default = default_action
        self.__action_current = default_action

    # Loads all the entity actions
    def __load_actions(self, button_name: str):
        actions = {} # Create the entity actions dict
        actions_file = open(f'assets/ui/{button_name}/actions.txt', 'r') # Opens the file with the actions declarations
        actions_decls = actions_file.read().splitlines() # Gets each declaration
        actions_file.close() # Closes the file

        for action_decl in actions_decls: # Iterates for each declaration
            action_decl = action_decl.split(' ') # Splits the string into each element
            action_name = action_decl[0] # Gets the action name, it's the first element
            action_mode = action_decl[1] # Gets the action mode loop or once
            action_decl.remove(action_decl[0]) # Removes the action name to keep just the action frames times and the action mode
            action_decl.remove(action_decl[0]) # Removes the action mode to keep just the action frames times
            action_images = [] # A List to contain all images

            for i in range(len(action_decl)):
                for j in range(int(action_decl[i])):
                    # Adding the image to the list of images
                    action_images.append(pygame.image.load(f'assets/ui/{button_name}/{action_name}/{action_name}_{i}.png'))

            actions[action_name] = [action_images, action_mode]
        
        return actions

    # Sets the action
    # If it's playing a loop action, this action can be interrupted to play another action and the frame count is restarted
    # If it's playing a once play action, the action can be interrupted, but if you set force to True, so the action will be interrupted
    def set_action(self, action_name, force: bool = False):
        if self.__actions[self.__action_current][1] == 'loop':
            if self.__action_current != action_name:
                self.__action_frame = 0
                self.__action_current = action_name
            elif force:
                self.__action_frame = 0
        elif force:
            self.__action_current = action_name
            self.__action_frame = 0
    
    def next_frame(self): # Updates the current action
        self.__action_frame += 1
        if self.__action_frame > len(self.__actions[self.__action_current][0]) - 1:
            if self.__actions[self.__action_current][1] == 'once': # If the action is a once play action, when it ends will auto set to the default action
                self.set_action(self.__action_default, True)
            self.__action_frame = 0
    
    def render(self, camera: pygame.Surface):
        camera.blit(self.__actions[self.__action_current][0][self.__action_frame], self.__position)

    def get_rect(self):
        return self.__rect

    def __on_click(self):
        global MENU
        MENU = 'home'
        pygame.time.delay(250)

    def update(self):
        self.next_frame()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]/4, mouse_pos[1]/4)
        hover = self.__rect.right >= mouse_pos[0] and mouse_pos[0] >= self.__rect.left and self.__rect.bottom >= mouse_pos[1] and mouse_pos[1] >= self.__rect.top
        if hover:
            self.set_action('hover')
            if pygame.mouse.get_pressed(3)[0]:
                self.__on_click()
                self.set_action('click', True)

ball = Ball('ball', [98, 72], [5, 5])
blue_bar = Bar('blue_bar', [5, 63], [5, 25], move_condition=lambda x: x < 0) #  player_control={'up': K_UP, 'down': K_DOWN}
red_bar = Bar('red_bar', [190, 63], [5, 25], move_condition=lambda x: x > 0)

score_particles = []

resume_btn = ResumeButton([68, 35], [64, 32], 'resume')
home_btn = HomeButton([68, 83], [64, 32], 'home')
play_btn = PlayButton([68, 66], [64, 32], 'singleplayer')
exit_btn = ExitButton([68, 114], [64, 32], 'exit')

font = pygame.font.Font('assets/ui/font/FreePixel.ttf', 15)

blue_score = font.render(str(blue_bar.score), True, pygame.Color(0,0,150))
red_score = font.render(str(red_bar.score), True, pygame.Color(150,0,0))
time_text = font.render(str(MATCH_TIME), True, pygame.Color(0,0,0))

while True:
    DISPLAY.fill((100,100,100))
    DISPLAY.blit(pygame.image.load('assets/background/pitch.png'), (0,0))

    # EVENT HANDLER

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_r and MENU == 'play':
                ball.set_position([98, 72])
                ball.movement = [random.choice([-1.5, 1.5]), 0]
            elif event.key == K_ESCAPE:
                if MENU == 'play':
                    MENU = 'pause'
                elif MENU == 'pause':
                    MENU = 'play'
    
    if MENU == 'play':
        # LOGIC
        ball.update()
        blue_bar.update(ball)
        red_bar.update(ball)

        for p in score_particles:
            p.update()

        # Checking for score

        if ball.get_rect().left < 1:
            score_particles.append(ScoreParticle('score', [ball.get_rect().x-11, ball.get_rect().y-11], [22, 22]))
            red_bar.score += 1
            blue_bar.target_point = 74
            red_bar.target_point = 74
            ball.set_position([98, 72])
            ball.movement = [random.choice([-1.5, 1.5]), 0]
            ball.hit_count = 0

        elif ball.get_rect().right > 199:
            score_particles.append(ScoreParticle('score', [ball.get_rect().x-11, ball.get_rect().y-11], [22, 22]))
            blue_bar.score += 1
            blue_bar.target_point = 74
            red_bar.target_point = 74
            ball.set_position([98, 72])
            ball.movement = [random.choice([-1.5, 1.5]), 0]
            ball.hit_count = 0
        
        # Updating the bar's AI target point

        if blue_bar.get_rect().colliderect(ball.get_rect()):
            red_bar.update_target_point(ball)
        if red_bar.get_rect().colliderect(ball.get_rect()):
            blue_bar.update_target_point(ball)
        
        # Removing the particles

        for p in score_particles:
            if not p.is_living:
                score_particles.remove(p)

        # DRAWING

        blue_bar.render(DISPLAY)
        red_bar.render(DISPLAY)
        ball.render(DISPLAY)

        for p in score_particles:
            p.render(DISPLAY)

        blue_score = font.render(str(blue_bar.score), True, pygame.Color(0,0,150))
        red_score = font.render(str(red_bar.score), True, pygame.Color(150,0,0))


        match_seconds = int(MATCH_TIME // 60)
        time_text = font.render(f'{match_seconds}s', True, pygame.Color(0,0,0))

        DISPLAY.blit(blue_score, [98-blue_score.get_rect().width, 0])
        DISPLAY.blit(red_score, [102, 0])
        DISPLAY.blit(time_text, [100-time_text.get_rect().width/2, 150-time_text.get_rect().height])

        MATCH_TIME += 1

    elif MENU == 'pause':
        resume_btn.update()
        home_btn.update()

        blue_bar.render(DISPLAY)
        ball.render(DISPLAY)
        red_bar.render(DISPLAY)

        DISPLAY.blit(time_text, [100-time_text.get_rect().width/2, 150-time_text.get_rect().height])
        DISPLAY.blit(blue_score, [98-blue_score.get_rect().width, 0])
        DISPLAY.blit(red_score, [102, 0])

        resume_btn.render(DISPLAY)
        home_btn.render(DISPLAY)

    elif MENU == 'home':
        play_btn.update()
        exit_btn.update()
        
        play_btn.render(DISPLAY)
        exit_btn.render(DISPLAY)

    WINDOW.blit(pygame.transform.scale(DISPLAY, (800,600)), (0,0))
    pygame.display.update()
    CLOCK.tick(60)
