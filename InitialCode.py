import pygame
import random
import math
 
# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
 
# Classes
 
class Player(pygame.sprite.Sprite):
    # this is the class for the player
    def __init__(self):
        # constructor for the class, defining it's attributes
        super().__init__()
        self.x_size = 20
        self.y_size = 20
        self.original_image = pygame.Surface([self.x_size, self.y_size])
        self.image = self.original_image
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2

        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0

    def move(self, x_speed, y_speed):
        # method to change the speed variables of the player

        self.x_speed = self.x_speed + x_speed
        self.y_speed = self.y_speed + y_speed
    def update(self):
        # update sprite position
        self.rect.x = self.rect.x + self.x_speed
        self.rect.y = self.rect.y + self.y_speed

        # making the sprite rotate
        # mouse/target position
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        # player centre finder
        player_centre_x = self.rect.x + self.x_size / 2
        player_centre_y = self.rect.y + self.y_size / 2
        
        # maths to find angle to rotate sprite by
        y_difference = player_centre_y - y
        x_difference = x - player_centre_x
        
        if x_difference == 0 and y_difference >= 0:
            self.angle = 90
        elif x_difference == 0 and y_difference < 0:
            self.angle = -90
        elif x_difference < 0 and y_difference <= 0:
            self.angle = math.degrees(math.atan( y_difference / x_difference ))
            self.angle = self.angle - 180
        elif x_difference < 0 and y_difference > 0:
            self.angle = math.degrees(math.atan( y_difference / x_difference ))
            self.angle = 180 + self.angle
        else:
            self.angle = math.degrees(math.atan( y_difference / x_difference ))
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
 
class Game(object):
    # This class represents an instance of the game. If we need to
    #    reset the game we'd just need to create a new instance of this
    #    class
 
    def __init__(self):
        # Constructor. Create all our attributes and initialize
        #    the game.
        

        # Sprite groups
        self.all_sprites_list = pygame.sprite.Group()

        # Create the player
        self.player = Player()
        self.all_sprites_list.add(self.player)
    def process_events(self):
        # Process all of the events. Return a "True" if we need
        #    to close the window. 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            # Player movement code
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.move(0,-5)
                if event.key == pygame.K_s:
                    self.player.move(0,5)
                if event.key == pygame.K_a:
                    self.player.move(-5,0)
                if event.key == pygame.K_d:
                    self.player.move(5,0)
            
            # Code to stop the player moving when key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.move(0,5)
                if event.key == pygame.K_s:
                    self.player.move(0,-5)
                if event.key == pygame.K_a:
                    self.player.move(5,0)
                if event.key == pygame.K_d:
                    self.player.move(-5,0)
            
    
        return False
 
    def run_logic(self):
        
        #This method is run each time through the frame. It
        #updates positions and checks for collisions.
        
        self.all_sprites_list.update()
 
    def display_frame(self, screen):
        # Display everything to the screen for the game. 
        screen.fill(WHITE)


        # draw all the sprites
        self.all_sprites_list.draw(screen)
 
        pygame.display.flip()
 
 
def main():
    # Main program function.
    # Initialize Pygame and set up the window
    pygame.init()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(True)
 
    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
 
    # Create an instance of the Game class
    game = Game()
 
    # Main game loop
    while not done:
 
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
 
        # Update object positions, check for collisions
        game.run_logic()
 
        # Draw the current frame
        game.display_frame(screen)
 
        # Pause for the next frame
        clock.tick(60)
 
    # Close window and exit
    pygame.quit()
 
# Call the main function, start up the game
if __name__ == "__main__":
    main()