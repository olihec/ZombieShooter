import pygame
import random
import math
 
# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (34,139,34)
 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
 
# Classes
class Zombie(pygame.sprite.Sprite):
    #this is the basic zombie class that will follow the player
    def __init__(self, x, y):
        super().__init__()
        self.x_size = 15
        self.y_size = 15
        self.original_image = pygame.Surface([self.x_size, self.y_size])
        self.image = self.original_image
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.x_speed = 0
        self.y_speed = 0

        # variables to make the zombie follow the player

        self.player_centre_x = 0
        self.player_centre_y = 0
        
    def update(self):
        # making the zombie follow the player



        self.zombie_centre_x = self.rect.x + self.x_size / 2
        self.zombie_centre_y = self.rect.y + self.y_size / 2

        self.y_difference = self.player_centre_y - self.zombie_centre_y
        self.x_difference = self.player_centre_x - self.zombie_centre_x
        
        self.diagonal = math.sqrt((self.y_difference ** 2) + (self.x_difference ** 2))
        
        self.x_speed = round(2*(self.x_difference /self.diagonal))
        self.y_speed = round(2*(self.y_difference /self.diagonal))
    
        

class Tree(pygame.sprite.Sprite):
    # this is the class for our trees in the map
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20,20])
        self.image.fill(DARK_GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 50

class Bullet(pygame.sprite.Sprite):
    # This is the class for our bullets that the player will shoot
    def __init__(self, x, y):
        # constructor
        super().__init__()
        self.x_size = 5
        self.y_size = 5
        self.image = pygame.Surface([self.x_size, self.y_size])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = 10
        # mouse position when bullet is shot

        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]

        self.bullet_centre_x = self.rect.x + self.x_size / 2
        self.bullet_centre_y = self.rect.y + self.y_size / 2

        self.y_difference = y - self.bullet_centre_y
        self.x_difference = x - self.bullet_centre_x
        
        self.diagonal = math.sqrt((self.y_difference ** 2) + (self.x_difference ** 2))
    def update(self):
        
        # maths to make the bullet fire in the direction of the mouse
        
        self.rect.x = self.rect.x + round(10* (self.x_difference /self.diagonal))
        self.rect.y = self.rect.y + round(10* (self.y_difference /self.diagonal))
        


class Player(pygame.sprite.Sprite):
    # this is the class for the player
    def __init__(self):
        # constructor for the class, defining it's attributes
        super().__init__()
        self.x_size = 15
        self.y_size = 15
        self.original_image = pygame.Surface([self.x_size, self.y_size])
        self.image = self.original_image
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2

        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0
        
        self.player_centre_x = self.rect.x + self.x_size / 2
        self.player_centre_y = self.rect.y + self.y_size / 2

    def move(self, x_speed, y_speed):
        # method to change the speed variables of the player
        
        self.x_speed = self.x_speed + x_speed
        self.y_speed = self.y_speed + y_speed
    def update(self):
        
        


        # making the sprite rotate
        # mouse/target position
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        # player centre finder
        self.player_centre_x = round(self.rect.x + self.x_size / 2)
        self.player_centre_y = round(self.rect.y + self.y_size / 2)
        
        # maths to find angle to rotate sprite by
        y_difference = self.player_centre_y - y
        x_difference = x - self.player_centre_x
        
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
        self.bullet_list = pygame.sprite.Group()
        self.tree_list = pygame.sprite.Group()
        self.zombie_list = pygame.sprite.Group()


        # Creating the map of trees
        self.map = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    ]

        # putting in the trees randomly
        count = 0
        while count < 100:
            
            x = random.randint(1,49)
            y = random.randint(1,34)
            if self.map[y][x] == 0:
                self.map[y][x] = 1
                count = count + 1
    

        for j in range(35):
            for i in range(50):
                if self.map[j][i] == 1:
                    self.tree = Tree(i*20,j*20)
                    self.all_sprites_list.add(self.tree)
                    self.tree_list.add(self.tree)
        # Create the player
        self.player = Player()
        self.all_sprites_list.add(self.player)

        # Create zombie 
        self.zombie = Zombie(600,600)
        self.all_sprites_list.add(self.zombie)
        self.zombie_list.add(self.zombie)
    def process_events(self):
        # Process all of the events. Return a "True" if we need
        #    to close the window. 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            # bullet shooting
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.bullet = Bullet(self.player.player_centre_x, self.player.player_centre_y)
                self.all_sprites_list.add(self.bullet)
                self.bullet_list.add(self.bullet)
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

        # give the zombie the players co ords so it can follow
        self.zombie.player_centre_x = self.player.player_centre_x
        self.zombie.player_centre_y = self.player.player_centre_y

        self.all_sprites_list.update()
        
        # removing bullets from sprite list if they collide with
        for self.bullet in self.bullet_list:
            trees_hit = pygame.sprite.spritecollide(self.bullet, self.tree_list, False)
            for self.tree in trees_hit:
                # checking if tree is a side tree
                self.bullet_list.remove(self.bullet)
                self.all_sprites_list.remove(self.bullet)
                if not(self.tree.rect.x == 0 or self.tree.rect.x == 980 or self.tree.rect.y == 0 or self.tree.rect.y == 680):
                    
                    self.tree.health = self.tree.health - self.bullet.damage
                    self.bullet_list.remove(self.bullet)
                    self.all_sprites_list.remove(self.bullet)
                    if self.tree.health < 1:
                        # remove tree if its health goes below 0
                        
                        self.tree_list.remove(self.tree)
                        self.all_sprites_list.remove(self.tree)
                    
                    

        
        # update sprite position
        self.player.rect.x = self.player.rect.x + self.player.x_speed
        

        # making it so player can't pass through tree
        tree_hit_list = pygame.sprite.spritecollide(self.player, self.tree_list, False)
        for self.tree in tree_hit_list:
            if self.player.x_speed > 0:
                self.player.rect.right = self.tree.rect.left
            else:
                self.player.rect.left = self.tree.rect.right
            
        self.player.rect.y = self.player.rect.y + self.player.y_speed

        tree_hit_list = pygame.sprite.spritecollide(self.player, self.tree_list, False)
        for self.tree in tree_hit_list:
            if self.player.y_speed > 0:
                self.player.rect.bottom = self.tree.rect.top
            else:
                self.player.rect.top = self.tree.rect.bottom

        # make the zombies unable to pass through trees
        self.zombie.rect.x = self.zombie.rect.x + self.zombie.x_speed
        
        tree_hit_list = pygame.sprite.spritecollide(self.zombie, self.tree_list, False)
        for self.tree in tree_hit_list:
            if self.zombie.x_speed > 0:
                self.zombie.rect.right = self.tree.rect.left
            else:
                self.zombie.rect.left = self.tree.rect.right
            
        self.zombie.rect.y = self.zombie.rect.y + self.zombie.y_speed

        tree_hit_list = pygame.sprite.spritecollide(self.zombie, self.tree_list, False)
        for self.tree in tree_hit_list:
            if self.zombie.y_speed > 0:
                self.zombie.rect.bottom = self.tree.rect.top
            else:
                self.zombie.rect.top = self.tree.rect.bottom
        

        
    def display_frame(self, screen):
        # Display everything to the screen for the game. 
        screen.fill(GREEN)


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
    