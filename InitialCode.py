import pygame
import random
import math
from os import path
 
# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (34,139,34)
YELLOW = (255,255,0)
BROWN = (210,105,30)
 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# highscore file
HIGHSCORE_FILE = "highscore.txt"
 
# Classes
class Bank(pygame.sprite.Sprite):
    # this will be the class for the bank in the shop that the player can use
    def __init__(self):
        super().__init__()
        self.x_size = 115
        self.y_size = 115
        self.image = pygame.Surface([self.x_size, self.y_size])
        

        self.rect = self.image.get_rect()
        self.rect.x = 760
        self.rect.y = 510

        self.balance = 0


class Shop(pygame.sprite.Sprite):
    # this will be the class for the shop that the player will be able to enter
    def __init__(self, x, y):
        super().__init__()
        self.x_size = 100
        self.y_size = 100
        self.image = pygame.Surface([self.x_size, self.y_size])
        self.shop_image = pygame.image.load("shop.png").convert()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Zombie(pygame.sprite.Sprite):
    #this is the basic zombie class that will follow the player
    def __init__(self, x, y):
        super().__init__()
        self.x_size = 15
        self.y_size = 15
        self.original_image = pygame.Surface([self.x_size, self.y_size])
        self.image = self.original_image
        
        self.orig_zombie_image = pygame.image.load("zumbi.png").convert()
        self.zombie_image = self.orig_zombie_image
        self.zombie_image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.x_speed = 0
        self.y_speed = 0

        self.health = 30

        self.entered_map = False
        # variables to make the zombie follow the player

        self.player_centre_x = 0
        self.player_centre_y = 0

    def follow_player(self):
        # making the zombie follow the player
        self.zombie_centre_x = self.rect.x + self.x_size / 2
        self.zombie_centre_y = self.rect.y + self.y_size / 2

        self.y_difference = self.player_centre_y - self.zombie_centre_y
        self.x_difference = self.player_centre_x - self.zombie_centre_x
        
        self.diagonal = math.sqrt((self.y_difference ** 2) + (self.x_difference ** 2))
        
        self.x_speed = round(2*(self.x_difference /self.diagonal))
        self.y_speed = round(2*(self.y_difference /self.diagonal))

        if self.x_difference == 0 and self.y_difference >= 0:
            self.angle = 90
        elif self.x_difference == 0 and self.y_difference < 0:
            self.angle = -90
        elif self.x_difference < 0 and self.y_difference <= 0:
            self.angle = math.degrees(math.atan( self.y_difference / self.x_difference ))
            self.angle = self.angle - 180
        elif self.x_difference < 0 and self.y_difference > 0:
            self.angle = math.degrees(math.atan( self.y_difference / self.x_difference ))
            self.angle = 180 + self.angle
        else:
            self.angle = math.degrees(math.atan( self.y_difference / self.x_difference ))
    
    


        self.zombie_image = pygame.transform.rotate(self.orig_zombie_image, -self.angle)
        
    def update(self):
        
        # making zombies enter the map slowly
        if self.entered_map == False:
            if self.rect.y < 20:
                self.y_speed = 1
            if self.rect.y > 665:
                self.y_speed = -1
            if self.rect.x < 20:
                self.x_speed = 1
            if self.rect.x > 965:
                self.x_speed = -1
        else:
            self.follow_player()

        if self.rect.x == 20 or self.rect.x == 965 or self.rect.y == 20 or self.rect.y == 665:
            self.entered_map = True

   
class Powerup(pygame.sprite.Sprite):
    # this is the class to give the player powerups
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50,50])
       
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # assigning random powerup to the sprite
        powerup_list = ["Shotgun", "Speed"]
        x = random.randint(0, len(powerup_list) - 1)
        self.type = powerup_list[x]

        if self.type == "Shotgun":
            self.cost = 5
            self.item_image = pygame.image.load("shotgun.png").convert()
            self.item_image.set_colorkey(BLACK)
        elif self.type == "Speed":
            self.cost = 4
            self.item_image = pygame.image.load("bolt.png").convert()
            self.item_image.set_colorkey(BLACK)
     

class Tree(pygame.sprite.Sprite):
    # this is the class for our trees in the map
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20,20])
       
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 50

        self.tree_image = pygame.image.load("tree.png").convert()
      
        self.tree_image.set_colorkey(BLACK)
        

class Money(pygame.sprite.Sprite):
    # this is the class for our Money in the map that spawns under trees and zombies
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10,10])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # list for our animated coin and pointer
        self.image_timer = 0
        self.image_pointer = 0
        self.image_list = ["coin1.png", "coin2.png", "coin3.png", "coin4.png", "coin5.png", "coin6.png", "coin7.png", "coin8.png"]
        self.money_image = pygame.image.load("coin1.png").convert()
        self.money_image.set_colorkey(BLACK)

    def update(self):

        self.image_timer = self.image_timer + 1
        if self.image_timer % 5 == 0:
            self.image_pointer = (self.image_pointer + 1) % 8
        self.money_image = pygame.image.load(self.image_list[self.image_pointer]).convert()
        self.money_image.set_colorkey(BLACK)

class Bullet(pygame.sprite.Sprite):
    # This is the class for our bullets that the player will shoot
    def __init__(self, x, y, gun):
        # constructor
        super().__init__()
        self.x_size = 4
        self.y_size = 4
        self.image = pygame.Surface([self.x_size, self.y_size])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = 10

        self.range = 40
        self.gun = gun

        # variable to check how long bullet has been shot for (range)
        self.timer = 0
        self.shoot()

    def shoot(self):
        # mouse position when bullet is shot

        pos = pygame.mouse.get_pos()

        
        x = pos[0]
        y = pos[1]
        

        self.bullet_centre_x = self.rect.x + self.x_size / 2
        self.bullet_centre_y = self.rect.y + self.y_size / 2

        self.y_difference = y - self.bullet_centre_y
        self.x_difference = x - self.bullet_centre_x
        
        self.diagonal = math.sqrt((self.y_difference ** 2) + (self.x_difference ** 2))

        if self.gun == "Shotgun":
            self.damage = 20
            self.range = 10

            x = random.randint(pos[0] - round(self.diagonal / 2) , round(pos[0] + self.diagonal / 2))
            y = random.randint(pos[1] - round(self.diagonal / 2), round(pos[1] + self.diagonal / 2))

            self.y_difference = y - self.bullet_centre_y
            self.x_difference = x - self.bullet_centre_x
        
            self.diagonal = math.sqrt((self.y_difference ** 2) + (self.x_difference ** 2))

    def update(self):
        
        self.timer = self.timer + 1
        # maths to make the bullet fire in the direction of the mouse
        
        self.rect.x = self.rect.x + round(10* (self.x_difference /self.diagonal))
        self.rect.y = self.rect.y + round(10* (self.y_difference /self.diagonal))
        


class Player(pygame.sprite.Sprite):
    # this is the class for the player
    def __init__(self, x, y, character):
        # constructor for the class, defining it's attributes
        super().__init__()
        self.x_size = 15
        self.y_size = 15
        self.original_image = pygame.Surface([self.x_size, self.y_size])
        self.image = self.original_image
        
        if character == "Jim":
            self.orig_player_image = pygame.image.load("jim.png").convert()
          
        elif character == "Emma":
            self.orig_player_image = pygame.image.load("emma.png").convert()
          
        elif character == "Hank":
            self.orig_player_image = pygame.image.load("hank.png").convert()
       
        self.money = 0
        self.score = 0

        self.player_image = self.orig_player_image
        self.player_image.set_colorkey(BLACK)

        self.orig_rect = self.player_image.get_rect()
        

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0
        
        self.player_centre_x = self.rect.x + self.x_size / 2
        self.player_centre_y = self.rect.y + self.y_size / 2

        

        # variable to track which gun player has
        self.gun = "Pistol"

        self.reload_time = 20
        self.shot_timer = 0
        self.gun_reloaded = True

        

        # image for the hearts
        self.heart_image = pygame.image.load("heart.png").convert()
        self.heart_image.set_colorkey(BLACK)

        self.font = pygame.font.SysFont('Calibri', 25, True, False)
 
        
    def move(self, x_speed, y_speed):
        # method to change the speed variables of the player
        
        self.x_speed = self.x_speed + x_speed
        self.y_speed = self.y_speed + y_speed
        
    def reload(self):
        # check is reload time is finished
        if self.reload_time == self.shot_timer:
            self.gun_reloaded = True

    def rotate(self):

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
        
        # rotation for player


        self.player_image = pygame.transform.rotate(self.orig_player_image, self.angle)

    def update(self):
        
        
        

        if self.gun_reloaded == False:
            self.shot_timer = self.shot_timer + 1


        self.rotate()
        
        
 
class Game(object):
    # This class represents an instance of the game. If we need to
    #    reset the game we'd just need to create a new instance of this
    #    class
 
    def __init__(self):
        # Constructor. Create all our attributes and initialize
        #    the game.
        
        # loading highscores

        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HIGHSCORE_FILE), 'r') as f:
            try:
                self.highscore = [[f.readline()[:-1] , int(f.readline())], [f.readline()[:-1] , int(f.readline())], [f.readline()[:-1] , int(f.readline())]]   
            except:
                self.highscore = [["xxx", 0], ["xxx", 0], ["xxx", 0]]

        self.characters = ["Jim", "Emma", "Hank"]
        self.character_pointer = 0

        self.restart(0, 0, 0, 0 , 3 ,5, "Pistol", False)

    def process_events(self):
        # Process all of the events. Return a "True" if we need
        #    to close the window. 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            # bullet shooting
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_start:
                    if self.player.gun_reloaded == True:
                        self.player.gun_reloaded = False
                        self.player.shot_timer = 0
                        if self.player.gun == "Pistol":
                            self.bullet = Bullet(self.player.player_centre_x, self.player.player_centre_y, self.player.gun)
                            self.all_sprites_list.add(self.bullet)
                            self.bullet_list.add(self.bullet)
                        elif self.player.gun == "Shotgun":
                            for i in range(5):
                                self.bullet = Bullet(self.player.player_centre_x, self.player.player_centre_y, self.player.gun)
                                self.all_sprites_list.add(self.bullet)
                                self.bullet_list.add(self.bullet)
                else:
                    
                    # Chech if player clicks buttons
                    pos = pygame.mouse.get_pos()
                    x = pos[0]
                    y = pos[1]

                    if self.instructions and x > 205 and x < 240 and y > 130 and y < 165:
                        self.instructions = False

                    if x > 100 and x < 300 and y > 580 and y < 640:
                        self.character_selection = True

                    elif x > 400 and x < 600 and y > 580 and y < 640:
                        if self.character_selection:
                            if self.characters[self.character_pointer] == "Jim":
                                self.restart(0, 0, 0, 0 , 3 ,5, "Pistol", False)

                            elif self.characters[self.character_pointer] == "Emma":
                                self.restart(0, 0, 0, 0 , 4 ,3, "Pistol", False)

                            elif self.characters[self.character_pointer] == "Hank":
                                self.restart(0, 0, 0, 0 , 2 ,7, "Pistol", False)
                        else:
                            self.game_start = True

                       
                    elif x > 700 and x < 900 and y > 580 and y < 640:
                        self.instructions = True
                    
                
            # Player movement code
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.move(0,-self.player.speed)
                if event.key == pygame.K_s:
                    self.player.move(0,self.player.speed)
                if event.key == pygame.K_a:
                    self.player.move(-self.player.speed,0)
                if event.key == pygame.K_d:
                    self.player.move(self.player.speed,0)

                if self.character_selection:
                    # picking character 
                    if event.key == pygame.K_LEFT:
                        self.character_pointer = (self.character_pointer - 1) % 3
                    if event.key == pygame.K_RIGHT:
                        self.character_pointer = (self.character_pointer + 1) % 3
            
            # Code to stop the player moving when key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.move(0,self.player.speed)
                if event.key == pygame.K_s:
                    self.player.move(0,-self.player.speed)
                if event.key == pygame.K_a:
                    self.player.move(self.player.speed,0)
                if event.key == pygame.K_d:
                    self.player.move(-self.player.speed,0)
            

        return False
    
    def restart(self, player_x_speed, player_y_speed, money, score, lives, speed, gun, game_start):
        # method for restarting the game 

        # restarting game
        # variable to determine when the game is on start screen of not 
        self.game_start = game_start
        self.shop_screen = False
        self.round_over = False
        self.instructions = False
        self.character_selection = False
        self.background_image = pygame.image.load("lea.png").convert()

        # Sprite groups
        self.all_sprites_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.tree_list = pygame.sprite.Group()
        self.zombie_list = pygame.sprite.Group()
        self.money_list = pygame.sprite.Group()
        self.shop_list = pygame.sprite.Group()
        

        # timer in game used for bullets and zombies
        self.timer = 0

        
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
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
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
    
        # variable to keep track of where there arn't trees
        self.empty_spaces = []
        for j in range(35):
            for i in range(50):
                if self.map[j][i] == 1:
                    self.tree = Tree(i*20,j*20)
                    self.all_sprites_list.add(self.tree)
                    self.tree_list.add(self.tree)
                else:
                    self.empty_spaces.append((j,i))
        # Create the player

        self.player = Player(500, 405, self.characters[self.character_pointer])
        self.player.x_speed = player_x_speed
        self.player.y_speed = player_y_speed
        self.player.score = score
        self.player.lives = lives
        self.player.money = money
        self.player.speed = speed
        self.player.gun = gun
        self.all_sprites_list.add(self.player)

        


        self.shop = Shop(460, 300)
        self.all_sprites_list.add(self.shop)
        self.shop_list.add(self.shop)

    def create_zombie(self):

        # Create zombie 
        if self.timer % 120 == 0:
            if not(self.round_over):
                zombie_created = False
                while zombie_created == False:
                    x = random.randint(-15, 1000)
                    y = random.randint(-15, 700)
                    # check is zombie is out of screen
                    if x == -15 or x == 1000 or y == -15 or y == 700:
                        zombie_created = True
                        self.zombie = Zombie(x,y)
                        self.all_sprites_list.add(self.zombie)
                        self.zombie_list.add(self.zombie)


    def game_over(self):

        # algorithm to find where in list highscore goes
        pointer = 999
        count = 0
        found = False
        while count < 3 and not(found):
            if self.highscore[count][1] < self.player.score:
                pointer = count
                found = True
            count = count + 1
            
        if pointer != 999:
            count = 2
            while count != pointer:
                count = count - 1
                self.highscore[count + 1] = self.highscore[count]
            
            inp = input("Enter name")
            self.highscore[pointer] = [inp, self.player.score]
            
                


            with open(path.join(self.dir, HIGHSCORE_FILE), 'w') as f:
                f.write(self.highscore[0][0] + "\n")
                
                f.write(str(self.highscore[0][1]) + "\n")
                
                f.write(self.highscore[1][0] + "\n")
                
                f.write(str(self.highscore[1][1]) + "\n")
                
                f.write(self.highscore[2][0] + "\n")
                
                f.write(str(self.highscore[2][1]))


        self.restart(self.player.x_speed,self.player.y_speed, 0, 0, 3, 5, "Pistol", False)

    def bullet_collisions(self):

        # collide with zombie
        zombie_hit = pygame.sprite.spritecollide(self.bullet, self.zombie_list, False) 
        for self.zombie in zombie_hit:
            self.zombie.health = self.zombie.health - self.bullet.damage
            self.bullet_list.remove(self.bullet)
            self.all_sprites_list.remove(self.bullet)
            if self.zombie.health < 1:
                    # remove zombie if its health goes below 0
                    self.player.score = self.player.score + 10

                    # dropping money on death
                    x = random.randint(0,1)
                    if x == 1:
                        self.money = Money(self.zombie.zombie_centre_x,self.zombie.zombie_centre_y)
                        self.all_sprites_list.add(self.money)
                        self.money_list.add(self.money)

                    self.zombie_list.remove(self.zombie)
                    self.all_sprites_list.remove(self.zombie)
        # collide with tree
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
                    self.player.score = self.player.score + 5
                    # one in 3 chance for money drop
                    x = random.randint(0,3)
                    if x == 1:
                        self.money = Money(self.tree.rect.x, self.tree.rect.y)
                        self.all_sprites_list.add(self.money)
                        self.money_list.add(self.money)
                    self.tree_list.remove(self.tree)
                    self.all_sprites_list.remove(self.tree)

    def shop_move_player(self):
        # update sprite position and keep in screen

        if self.player.rect.x < 985 and self.player.rect.x > 0:
            self.player.rect.x = self.player.rect.x + self.player.x_speed
            self.bank_collision("x")
        elif self.player.rect.x <= 0:
            self.player.rect.x = self.player.rect.x + self.player.speed
        elif self.player.rect.x >= 985:
            self.player.rect.x = self.player.rect.x - self.player.speed

        if self.player.rect.y < 685 and self.player.rect.y > 0:
            self.player.rect.y = self.player.rect.y + self.player.y_speed
            self.bank_collision("y")
        elif self.player.rect.y <= 0:
            self.player.rect.y = self.player.rect.y + self.player.speed
        elif self.player.rect.y >= 685:
            if self.player.rect.x > 460 and self.player.rect.x < 540:    
                if self.shop_screen:
                    self.game_start = True
                    self.restart(self.player.x_speed, self.player.y_speed, self.player.money, self.player.score, self.player.lives, self.player.speed, self.player.gun, self.game_start)
            else:
                self.player.rect.y = self.player.rect.y - self.player.speed  

    def gameplay_move_player(self):
        # update sprite position
        self.player.rect.x = self.player.rect.x + self.player.x_speed
        
        # check for collision with the shop
        # check if round is over to let player enter shop through door

        
        if pygame.sprite.spritecollide(self.player, self.shop_list, False):
            if self.player.x_speed > 0:
                self.player.rect.right = self.shop.rect.left
            elif self.player.x_speed < 0:
                self.player.rect.left = self.shop.rect.right
                

        # making it so player can't pass through tree
        tree_hit_list = pygame.sprite.spritecollide(self.player, self.tree_list, False)
        for self.tree in tree_hit_list:
            if self.player.x_speed > 0:
                self.player.rect.right = self.tree.rect.left
            else:
                self.player.rect.left = self.tree.rect.right
            
        self.player.rect.y = self.player.rect.y + self.player.y_speed

        if self.round_over:
            # check for collision with the shop in right area
            
            if pygame.sprite.spritecollide(self.player, self.shop_list, False):
                if self.player.y_speed < 0:
                    # if player collides with shop door they enter shop
                    if self.player.rect.x > 480 and self.player.rect.x < 520:
                        self.enter_shop(self.player.x_speed, self.player.y_speed, self.player.money, self.player.score, self.player.lives, self.player.speed, self.player.gun)
                    else:
                        self.player.rect.top = self.shop.rect.bottom
                elif self.player.y_speed > 0:
                    self.player.rect.bottom = self.shop.rect.top
        else:
            if pygame.sprite.spritecollide(self.player, self.shop_list, False):
                if self.player.y_speed > 0:
                    self.player.rect.bottom = self.shop.rect.top
                elif self.player.y_speed < 0:
                    self.player.rect.top = self.shop.rect.bottom

        tree_hit_list = pygame.sprite.spritecollide(self.player, self.tree_list, False)
        for self.tree in tree_hit_list:
            if self.player.y_speed > 0:
                self.player.rect.bottom = self.tree.rect.top
            else:
                self.player.rect.top = self.tree.rect.bottom


    def enter_shop(self, player_x_speed, player_y_speed, money, score, lives, speed, gun):
        # method for restarting the game 

        # restarting game
        # variable to determine when the game is on start screen of not 
        self.game_start = False
        self.shop_screen = True
        self.round_over = False


        # Sprite groups
        self.all_sprites_list = pygame.sprite.Group() 
        self.powerup_list = pygame.sprite.Group()
        self.bank_list = pygame.sprite.Group()
        

        

        # Create the player

        self.player = Player(500, 650, self.characters[self.character_pointer])
        self.player.x_speed = player_x_speed
        self.player.y_speed = player_y_speed
        self.player.score = score
        self.player.lives = lives
        self.player.money = money
        self.player.speed = speed
        self.player.gun = gun
        self.all_sprites_list.add(self.player)

        # create bank
        self.bank = Bank()
        self.all_sprites_list.add(self.bank)
        self.bank_list.add(self.bank)

        # Create powerup
        for i in range(3):

            self.powerup = Powerup(i * 250 + 125 ,130)
            self.all_sprites_list.add(self.powerup)
            self.powerup_list.add(self.powerup)
        for i in range(2):

            self.powerup = Powerup(i * 250 + 250 ,350)
            self.all_sprites_list.add(self.powerup)
            self.powerup_list.add(self.powerup)


    def move_zombie(self):

        # make the zombies unable to pass through trees when in map
                
        self.zombie.rect.x = self.zombie.rect.x + self.zombie.x_speed

        # check for collision with the shop
        if pygame.sprite.spritecollide(self.zombie, self.shop_list, False):
            if self.zombie.x_speed > 0:
                self.zombie.rect.right = self.shop.rect.left
            elif self.zombie.x_speed < 0:
                self.zombie.rect.left = self.shop.rect.right
        
        
        if self.zombie.entered_map == True:    
            tree_hit_list = pygame.sprite.spritecollide(self.zombie, self.tree_list, False)
            for self.tree in tree_hit_list:
                if self.zombie.x_speed > 0:
                    self.zombie.rect.right = self.tree.rect.left
                else:
                    self.zombie.rect.left = self.tree.rect.right
                
        self.zombie.rect.y = self.zombie.rect.y + self.zombie.y_speed

        if pygame.sprite.spritecollide(self.zombie, self.shop_list, False):
            if self.zombie.y_speed > 0:
                    self.zombie.rect.bottom = self.shop.rect.top
            elif self.zombie.y_speed < 0:
                self.zombie.rect.top = self.shop.rect.bottom

        if self.zombie.entered_map == True:
            tree_hit_list = pygame.sprite.spritecollide(self.zombie, self.tree_list, False)
            for self.tree in tree_hit_list:
                if self.zombie.y_speed > 0:
                    self.zombie.rect.bottom = self.tree.rect.top
                else:
                    self.zombie.rect.top = self.tree.rect.bottom            
    def powerup_collisions(self):
        # check for collision with powerup 
            powerup_hit = pygame.sprite.spritecollide(self.player, self.powerup_list, False) 
            for self.powerup in powerup_hit:
                if self.player.money >= self.powerup.cost:
                    # defining what each powerup does by its name
                    if self.powerup.type == "Shotgun":
                        self.player.gun = self.powerup.type
                        self.player.reload_time = 40

                    elif self.powerup.type == "Speed":
                        if self.player.x_speed > 0:
                            self.player.x_speed = self.player.speed + 1
                        if self.player.x_speed < 0:
                            self.player.x_speed = -(self.player.speed + 1)
                        if self.player.y_speed > 0:
                            self.player.y_speed = self.player.speed + 1
                        if self.player.y_speed < 0:
                            self.player.y_speed = -(self.player.speed + 1)
                        self.player.speed = self.player.speed + 1

                    self.player.money = self.player.money - self.powerup.cost
                    self.powerup_list.remove(self.powerup)
                    self.all_sprites_list.remove(self.powerup)

    def bank_collision(self, movement):
        # code for the function of the bank
        if pygame.sprite.spritecollide(self.player, self.bank_list, False):
            if not(self.bank.balance == 0 and self.player.money == 0):
                transaction_complete = False
                while transaction_complete == False:
                    transaction = input("Withdraw or deposit? (w/d)")
                    if transaction == "w":
                        valid = False
                        while not(valid):
                            try:
                                inp = int(input("How much?"))
                                valid = True
                            except ValueError:
                                print("Error, not a number")
                        inp = int(input("How much?"))
                        if self.bank.balance >= inp:
                            self.player.money = self.player.money + inp
                            self.bank.balance = self.bank.balance - inp
                            transaction_complete = True
                        else:
                            print("Error, insufficient amount")
                    elif transaction == "d":
                        valid = False
                        while not(valid):
                            try:
                                inp = int(input("How much?"))
                                valid = True
                            except ValueError:
                                print("Error, not a number")
                        if self.player.money >= inp:
                            self.bank.balance = self.bank.balance + inp
                            self.player.money = self.player.money - inp
                            transaction_complete = True
                        else:
                            print("Error, insufficient amount")
            
            if movement == "y":
                if self.player.y_speed > 0:
                    self.player.rect.bottom = self.bank.rect.top
                else:
                    self.player.rect.top = self.bank.rect.bottom
            if movement == "x":
                if self.player.x_speed > 0:
                    self.player.rect.right = self.bank.rect.left
                else:
                    self.player.rect.left = self.bank.rect.right

    def run_logic(self):
        
        #This method is run each time through the frame. It
        #updates positions and checks for collisions.

        if self.shop_screen:
            # what happens in the shop
            
            # update the position of all sprites
            self.all_sprites_list.update()
            self.shop_move_player()
            

            self.powerup_collisions()
            

        

            
        if self.game_start:
            self.create_zombie()
            if self.timer % 2500 == 0 and self.timer != 0:
                if self.round_over == False:
                    self.player.score = self.player.score + 50
                    self.round_over = True

            # make the timer increase every second
            self.timer = self.timer + 1

            
            # give the zombie the players co ords so it can follow
            for self.zombie in self.zombie_list:
                self.zombie.player_centre_x = self.player.player_centre_x
                self.zombie.player_centre_y = self.player.player_centre_y


            # update the position of all sprites
            self.all_sprites_list.update()
            
            self.player.reload()

            # removing bullets from sprite list if they collide or reach range limit
            for self.bullet in self.bullet_list:
                # remove bullets if their range is reached
                if self.bullet.timer == self.bullet.range:
                    self.bullet_list.remove(self.bullet)
                    self.all_sprites_list.remove(self.bullet)
            
                else:
                    self.bullet_collisions()
                        
            
            money_collect = pygame.sprite.spritecollide(self.player, self.money_list, True) 
            for self.money in money_collect:
                self.player.money = self.player.money + 1

            zombie_hit = pygame.sprite.spritecollide(self.player, self.zombie_list, True) 
            for self.zombie in zombie_hit:
                self.player.lives = self.player.lives - 1
                self.player.money = 0
                self.zombie_list.remove(self.zombie)
                self.all_sprites_list.remove(self.zombie)
                # when player dies
                if self.player.lives < 0:
                    self.game_over()


            


            
            
            


            self.gameplay_move_player()
            
            
            for self.zombie in self.zombie_list:
                self.move_zombie()
            
        
    def display_frame(self, screen):

        if self.game_start:
            # Display everything to the screen for the game. 
            self.background_image = pygame.image.load("lea.png").convert()
            screen.blit(self.background_image, [0, 0])


            
            self.all_sprites_list.draw(screen)
            

            #player and zombie images
            screen.blit(self.player.player_image, [self.player.rect.x, self.player.rect.y])
            for self.zombie in self.zombie_list:
                screen.blit(self.zombie.zombie_image, [self.zombie.rect.x, self.zombie.rect.y])

            screen.blit(self.shop.shop_image, [self.shop.rect.x, self.shop.rect.y])

            # drawing tree images
            for self.tree in self.tree_list:
                screen.blit(self.tree.tree_image, [self.tree.rect.x, self.tree.rect.y])

            for self.money in self.money_list:
                screen.blit(self.money.money_image, [self.money.rect.x, self.money.rect.y])

            text = self.player.font.render("Score: " + str(self.player.score),True,WHITE)
            screen.blit(text, [780, 2])
            text = self.player.font.render("Money: " + str(self.player.money),True,WHITE)
            screen.blit(text, [660, 2])

            # drawing the hearts and score and money of the player
            for i in range(self.player.lives):
                screen.blit(self.player.heart_image, [i * 20 + 900, 2])
            
    
        elif self.shop_screen:
            # display the screen for the shop 
            
            self.background_image = pygame.image.load("Holz Clean.jpg").convert()
            screen.blit(self.background_image, [0, 0])

            

            

            self.plank_image = pygame.image.load("plank.png").convert()
            for i in range(3):
                screen.blit(self.plank_image, [i* 250 + 75, 80])
            for i in range(2):
                screen.blit(self.plank_image, [i* 250 + 200 , 300])

           
            for self.powerup in self.powerup_list:
                text = self.player.font.render("Cost: " + str(self.powerup.cost),True,WHITE)
                screen.blit(text, [self.powerup.rect.x - 10, self.powerup.rect.y + 70 ])
                screen.blit(self.powerup.item_image, [self.powerup.rect.x, self.powerup.rect.y])
              
         

            self.all_sprites_list.draw(screen)
            self.bank_image = pygame.image.load("bag.png").convert()
            self.bank_image.set_colorkey(BLACK) 
            screen.blit(self.bank_image, [self.bank.rect.x - 20 , self.bank.rect.y - 20])
            
            # player image
            screen.blit(self.player.player_image, [self.player.rect.x, self.player.rect.y])
            


            text = self.player.font.render("Score: " + str(self.player.score),True,WHITE)
            screen.blit(text, [780, 2])
            text = self.player.font.render("Money: " + str(self.player.money),True,WHITE)
            screen.blit(text, [660, 2])
            font = pygame.font.SysFont('Calibri', 35, True, False)
            text = font.render("$" + str(self.bank.balance),True,WHITE)
            screen.blit(text, [797, 575])

            # drawing the hearts and score and money of the player
            for i in range(self.player.lives):
                screen.blit(self.player.heart_image, [i * 20 + 900, 2])

        elif self.character_selection:
            screen.fill(BLACK)
            font = pygame.font.SysFont("YouMurderer BB", 130)
            text = font.render("CHARACTER SELECTION", True, RED)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = 30
            screen.blit(text, [center_x, center_y])

            font = pygame.font.SysFont("YouMurderer BB", 90)
            text = font.render(self.characters[self.character_pointer], True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = 120
            screen.blit(text, [center_x, center_y])           

            self.right_arrow_image = pygame.image.load("right.png").convert()
            screen.blit(self.right_arrow_image, [800, 200])

            self.left_arrow_image = pygame.image.load("left.png").convert()
            screen.blit(self.left_arrow_image, [10, 200])

            self.select_button = pygame.image.load("select.png").convert()
            self.select_button.set_colorkey(BLACK)    
            screen.blit(self.select_button, [400, 580])

            # displaying currently selected character
            if self.character_pointer == 0:
                self.selection_image = pygame.image.load("jim_selection.png").convert()
            elif self.character_pointer == 1:
                self.selection_image = pygame.image.load("emma_selection.png").convert()
            elif self.character_pointer == 2:
                self.selection_image = pygame.image.load("hank_selection.png").convert()
                
            self.selection_image.set_colorkey(BLACK)    
            screen.blit(self.selection_image, [400, 200])
            

        else:

            
            
            self.background_image = pygame.image.load("start_screen.jpg").convert()
            screen.blit(self.background_image, [0, 0])

            font = pygame.font.SysFont("YouMurderer BB", 220)
            text = font.render("ZOMBIE", True, RED)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = 30
            screen.blit(text, [center_x, center_y])

            font = pygame.font.SysFont("YouMurderer BB", 220)
            text = font.render("SHOOTER", True, RED)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = 170
            screen.blit(text, [center_x, center_y])

            self.leaderboard_image = pygame.image.load("leaderboard.png").convert()
            self.leaderboard_image.set_colorkey(BLACK)
            center_x = (SCREEN_WIDTH // 2) - (self.leaderboard_image.get_width() // 2)

            screen.blit(self.leaderboard_image, [center_x, 320])

            font = pygame.font.SysFont("YouMurderer BB", 50)
            text = font.render("Leaderboard: ", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2) + 30
            screen.blit(text, [center_x, center_y])

            text = font.render(self.highscore[0][0] + " " + str(self.highscore[0][1]), True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2) + 90
            screen.blit(text, [center_x, center_y])

            text = font.render(self.highscore[1][0] + " " + str(self.highscore[1][1]), True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2) + 120
            screen.blit(text, [center_x, center_y])

            text = font.render(self.highscore[2][0] + " " + str(self.highscore[2][1]), True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2) + 150
            screen.blit(text, [center_x, center_y])


            font = pygame.font.SysFont("YouMurderer BB", 20)
            text = font.render("", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2) + 30
            screen.blit(text, [center_x, 510])

            self.character_selection_button = pygame.image.load("character_selection.png").convert()
            self.character_selection_button.set_colorkey(BLACK)    
            screen.blit(self.character_selection_button, [100, 580])

            self.start_button = pygame.image.load("start.png").convert()
            self.start_button.set_colorkey(BLACK)    
            screen.blit(self.start_button, [400, 580])

            self.instructions_button = pygame.image.load("instructions.png").convert()
            self.instructions_button.set_colorkey(BLACK)    
            screen.blit(self.instructions_button, [700, 580])

            if self.instructions:
                self.instructions_image = pygame.image.load("parchment.png").convert()
                self.instructions_image.set_colorkey(BLACK)
                screen.blit(self.instructions_image, [180, 100])

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
    