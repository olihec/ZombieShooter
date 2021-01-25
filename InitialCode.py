import pygame
import random
import math
 
# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (34,139,34)
YELLOW = (255,255,0)
 
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

        self.health = 100

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
    
class Powerup(pygame.sprite.Sprite):
    # this is the class to give the player powerups
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # assigning random powerup to the sprite
        powerup_list = ["Shotgun"]
        x = random.randint(0, len(powerup_list) - 1)
        self.type = powerup_list[x]
     

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
    def __init__(self, x, y, gun):
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

        self.range = 40
        

        # variable to check how long bullet has been shot for (range)
        self.timer = 0
        # mouse position when bullet is shot

        pos = pygame.mouse.get_pos()

        
        x = pos[0]
        y = pos[1]
        

        self.bullet_centre_x = self.rect.x + self.x_size / 2
        self.bullet_centre_y = self.rect.y + self.y_size / 2

        self.y_difference = y - self.bullet_centre_y
        self.x_difference = x - self.bullet_centre_x
        
        self.diagonal = math.sqrt((self.y_difference ** 2) + (self.x_difference ** 2))

        if gun == "Shotgun":
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

        self.lives = 3
        self.score = 0

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
    def update(self):
        
        self.text = self.font.render("Score: " + str(self.score),True,WHITE)


        if self.gun_reloaded == False:
            self.shot_timer = self.shot_timer + 1


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
        self.powerup_list = pygame.sprite.Group()

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

        self.player = Player()
        self.all_sprites_list.add(self.player)

        # Create zombie 
        self.zombie = Zombie(600,600)
        self.all_sprites_list.add(self.zombie)
        self.zombie_list.add(self.zombie)

        # Create powerup
        self.powerup = Powerup(600,600)
        self.all_sprites_list.add(self.powerup)
        self.powerup_list.add(self.powerup)
    def process_events(self):
        # Process all of the events. Return a "True" if we need
        #    to close the window. 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            # bullet shooting
            if event.type == pygame.MOUSEBUTTONDOWN:
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

        # make the timer increase every second
        self.timer = self.timer + 1

        # give the zombie the players co ords so it can follow
        self.zombie.player_centre_x = self.player.player_centre_x
        self.zombie.player_centre_y = self.player.player_centre_y

        self.all_sprites_list.update()
        
        # check is reload time is finished
        if self.player.reload_time == self.player.shot_timer:
            self.player.gun_reloaded = True

        # removing bullets from sprite list if they collide or reach range limit
        for self.bullet in self.bullet_list:
            # remove bullets if their range is reached
            if self.bullet.timer == self.bullet.range:
                self.bullet_list.remove(self.bullet)
                self.all_sprites_list.remove(self.bullet)
        
            else:
                # collide with zombie
                zombie_hit = pygame.sprite.spritecollide(self.bullet, self.zombie_list, False) 
                for self.zombie in zombie_hit:
                    self.zombie.health = self.zombie.health - self.bullet.damage
                    self.bullet_list.remove(self.bullet)
                    self.all_sprites_list.remove(self.bullet)
                    if self.tree.health < 1:
                            # remove zombie if its health goes below 0
                            self.player.score = self.player.score + 10
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
                            self.tree_list.remove(self.tree)
                            self.all_sprites_list.remove(self.tree)
                    
        
        zombie_hit = pygame.sprite.spritecollide(self.player, self.zombie_list, True) 
        for self.zombie in zombie_hit:
            self.player.lives = self.player.lives - 1
            self.zombie_list.remove(self.zombie)
            self.all_sprites_list.remove(self.zombie)

        # check for collision with powerup
        powerup_hit = pygame.sprite.spritecollide(self.player, self.powerup_list, True) 
        for self.powerup in powerup_hit:
            if self.powerup.type == "Shotgun":
                self.player.gun = self.powerup.type
                self.player.reload_time = 40
            self.powerup_list.remove(self.powerup)
            self.all_sprites_list.remove(self.powerup)
        
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

        # drawing the hearts and score of the player
        for i in range(self.player.lives):
            screen.blit(self.player.heart_image, [i * 20 + 900, 2])
        screen.blit(self.player.text, [780, 2])
 
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
    