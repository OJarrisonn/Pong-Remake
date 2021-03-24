import pygame, random
from pygame.locals import *

pygame.init()

CLOCK = pygame.time.Clock()

WINDOW = pygame.display.set_mode((800,600))
pygame.display.set_caption('Pong')

DISPLAY = pygame.Surface((200, 150))

class Ball:
    def __init__(self, entity_name: str, position: list = [0,0], size: list = [0,0], standard_action: str = 'idle'):
        self.__actions = self.__load_actions(entity_name)
        self.__action_frame = 0
        self.__action_current = standard_action
        self.__position = position
        self.__size = size
        self.__rect = pygame.Rect(int(self.__position[0]), int(self.__position[1]), self.__size[0], self.__size[1])
        self.movement = [random.choice([-1.5, 1.5]), 0]

    # Loads all the entity actions
    def __load_actions(self, entity_name) -> dict :
        actions = {} # Create the entity actions dict
        actions_file = open(f'assets/entities/{entity_name}/actions.txt', 'r') # Opens the file with the actions declarations
        actions_decls = actions_file.read().splitlines() # Gets each declaration
        actions_file.close() # Closes the file

        for action_decl in actions_decls: # Iterates for each declaration
            action_decl = action_decl.split(' ') # Splits the string into each element
            action_name = action_decl[0] # Gets the action name, it's the first element
            action_decl.remove(action_decl[0]) # Removes the action name to keep just the action frame times
            action_images = [] # A List to contain all images

            for i in range(len(action_decl)):
                for j in range(int(action_decl[i])):
                    # Adding the image to the list of images
                    action_images.append(pygame.image.load(f'assets/entities/{entity_name}/{action_name}/{action_name}_{i}.png'))

            actions[action_name] = action_images
        
        return actions

    def set_action(self, action_name, force: bool = False):
        if self.__action_current != action_name:
            self.__action_frame = 0
            self.__action_current = action_name
        elif force:
            self.__action_frame = 0
    
    def __update_rect(self):
        self.__rect = pygame.Rect(int(self.__position[0]), int(self.__position[1]), self.__size[0], self.__size[1])

    def get_rect(self) -> pygame.Rect:
        return self.__rect

    def apply_movement(self, movement):
        self.__position[0] += movement[0]
        self.__position[1] += movement[1]
        self.__update_rect()
    
    def next_frame(self):
        self.__action_frame += 1
        if self.__action_frame > len(self.__actions[self.__action_current]) - 1:
            self.__action_frame = 0
    
    def render(self, camera: pygame.Surface):
        camera.blit(self.__actions[self.__action_current][self.__action_frame], self.__position)

    def update(self):
        self.next_frame()
        self.apply_movement(self.movement)
        if self.__rect.top < 1 or self.__rect.bottom > 149:
            self.movement[1] *= -1

class Bar:
    def __init__(self, entity_name: str, position: list = [0,0], size: list = [0,0], player_controled: bool = False, standard_action: str = 'idle'):
        self.__actions = self.__load_actions(entity_name)
        self.__action_frame = 0
        self.__action_current = standard_action
        self.__position = position
        self.__size = size
        self.__rect = pygame.Rect(int(self.__position[0]), int(self.__position[1]), self.__size[0], self.__size[1])
        self.__is_player_controlled = player_controled

    # Loads all the entity actions
    def __load_actions(self, entity_name) -> dict :
        actions = {} # Create the entity actions dict
        actions_file = open(f'assets/entities/{entity_name}/actions.txt', 'r') # Opens the file with the actions declarations
        actions_decls = actions_file.read().splitlines() # Gets each declaration
        actions_file.close() # Closes the file

        for action_decl in actions_decls: # Iterates for each declaration
            action_decl = action_decl.split(' ') # Splits the string into each element
            action_name = action_decl[0] # Gets the action name, it's the first element
            action_decl.remove(action_decl[0]) # Removes the action name to keep just the action frame times
            action_images = [] # A List to contain all images

            for i in range(len(action_decl)):
                for j in range(int(action_decl[i])):
                    # Adding the image to the list of images
                    action_images.append(pygame.image.load(f'assets/entities/{entity_name}/{action_name}/{action_name}_{i}.png'))

            actions[action_name] = action_images
        
        return actions

    def set_action(self, action_name, force: bool = False):
        if self.__action_current != action_name:
            self.__action_frame = 0
            self.__action_current = action_name
        elif force:
            self.__action_frame = 0
    
    def __update_rect(self):
        self.__rect = pygame.Rect(int(self.__position[0]), int(self.__position[1]), self.__size[0], self.__size[1])

    def apply_movement(self, movement):
        self.__position[0] += movement[0]
        self.__position[1] += movement[1]
        self.__update_rect()
    
    def next_frame(self):
        self.__action_frame += 1
        if self.__action_frame > len(self.__actions[self.__action_current]) - 1:
            self.__action_frame = 0
    
    def render(self, camera: pygame.Surface):
        camera.blit(self.__actions[self.__action_current][self.__action_frame], self.__position)

    def update(self, ball: Ball = None):
        self.next_frame()
        if self.__is_player_controlled:
            pressed_keys = pygame.key.get_pressed()
            y_movement = (pressed_keys[K_DOWN] - pressed_keys[K_UP]) * 2
            self.apply_movement([0, y_movement])
        
        if self.__rect.colliderect(ball.get_rect()):
            ball.movement[0] *= -1
            ball_y = ball.get_rect().y - ( ball.get_rect().height / 2 ) - 32.5
            self_y = self.__rect.y - ( self.__rect.height / 2 ) - 12.5
            delta_y = ball_y - self_y
            ball.movement[1] += delta_y / 12


ball = Ball('ball', [98, 72], [5, 5])
blue_bar = Bar('blue_bar', [5, 63], [5, 25], player_controled=True)
red_bar = Bar('red_bar', [190, 63], [5, 25])

while True:
    DISPLAY.fill((100,100,100))

    # EVENT HANDLER

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            blue_bar.set_action('hit')
            red_bar.set_action('hit')
        elif event.type == KEYUP:
            blue_bar.set_action('idle')
            red_bar.set_action('idle')
    
    # LOGIC
    blue_bar.update(ball)
    red_bar.update(ball)
    ball.update()

    # DRAWING

    blue_bar.render(DISPLAY)
    red_bar.render(DISPLAY)
    ball.render(DISPLAY)
    
    WINDOW.blit(pygame.transform.scale(DISPLAY, (800,600)), (0,0))
    pygame.display.update()
    CLOCK.tick(60)