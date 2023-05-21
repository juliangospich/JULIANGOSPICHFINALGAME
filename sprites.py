import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
import sys
import pygame.mixer

vec = pg.math.Vector2

# player class

# initialization
pg.init()
pg.mixer.init()

# Fetching music from folder and looping it
pg.mixer.music.load("Lil Baby, Gunna - Drip Too Hard - Beat-Instrumental (1).mp3")
pg.mixer.music.play(-1)

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load('MJ.jpg').convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image.set_colorkey((255, 255, 255))  # Set white color as transparent
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.cofric = 0.1
        self.canjump = False
        self.standing = False
        self.num_jumps = 0
        self.death = False
        self.max_jumps = 50
        self.score = 0

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and (self.num_jumps < self.max_jumps):
            self.vel.y = -PLAYER_JUMP
            self.canjump = True
            self.num_jumps += 1
            # Reset vertical acceleration of Player 2
            #self.game.player2.acc.y = 0

    def game_over(self):
        if(self.rect.x > WIDTH or self.rect.x < 0):
            self.death = True

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.input()

        # Adjust the acceleration based on the player's current velocity
        if abs(self.vel.x) < PLAYER_MAX_SPEED:
            self.acc.x = self.vel.x * PLAYER_FRICTION
        else:
            self.acc.x = 0

       

        self.vel += self.acc
        self.vel.x = max(-PLAYER_MAX_SPEED, min(self.vel.x, PLAYER_MAX_SPEED))  # Limit the maximum velocity
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        if self.rect.top <= 0:
            self.game_over()

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        elif keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        else:
            self.acc.x = 0
        if keys[pg.K_w]:
            if self.canjump:
                self.jump()
        if keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
    def inbounds(self):
        if self.rect.x > WIDTH - 50:
            self.pos.x = WIDTH - 25
            self.vel.x = 0
            print("I am off the right side of the screen...")
        if self.rect.x < 0:
            self.pos.x = 25
            self.vel.x = 0
            print("I am off the left side of the screen...")
        if self.rect.y > HEIGHT:
            print("I am off the bottom of the screen")
        if self.rect.y < 0:
            print("I am off the top of the screen...")


    def mob_collide(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            print("You collided with an enemy...")
            self.game.score += 1
            print(SCORE)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

class Mob(Sprite):
    def __init__(self, width, height, color):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height))
        
        self.image = pg.image.load('money1.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image.set_colorkey((255, 255, 255))  # Set white color as transparent
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(randint(1, 5), randint(1, 5))
        self.acc = vec(1, 1)
        self.cofric = 0.01

    def inbounds(self):
        if self.rect.x > WIDTH:
            self.vel.x *= -1
        if self.rect.x < 0:
            self.vel.x *= -1
        if self.rect.y < 0:
            self.vel.y *= -1
        if self.rect.y > HEIGHT:
            self.vel.y *= -1

    def update(self):
        self.inbounds()
        self.pos += self.vel
        self.rect.center = self.pos


# create a new platform class...

class Platform(Sprite):
    def __init__(self, x, y, width, height, color, variant):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.variant = variant


class Basketball(Sprite):
    def __init__(self, width, height):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.image.load('basketball.jpg').convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image.set_colorkey((255, 255, 255))  # Set white color as transparent
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, 0.5)

    def update(self):
        self.vel += self.acceleration
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vel.x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vel.y *= -1

        


class BasketballHoop(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pg.image.load('basketballhoop.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        # Calculate the x-coordinate based on the screen width and given x position
        if x < WIDTH / 2:
            self.rect.x = x - 150  # Adjust position on the left side, 150 pixels to the left
        else:
            self.rect.x = x + 50  # Adjust position on the right side, 50 pixels to the right
            self.image = pg.transform.flip(self.image, True, False)  # Flip the image horizontally

        # Set the y-coordinate
        self.rect.y = y








class Player2(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load('lebron.jpg').convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image.set_colorkey((255, 255, 255))  # Set white color as transparent
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.cofric = 0.1
        self.canjump = False
        self.standing = False
        self.num_jumps = 0
        self.death = False
        self.max_jumps = 20
        self.score = 0

    def jump(self):
        
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and (self.num_jumps < self.max_jumps):
            self.vel.y = -PLAYER_JUMP
            self.canjump = True
            self.num_jumps += 1
            # Reset vertical acceleration of Player 2
            #self.game.player2.acc.y = 0

        #self.vel.y = -PLAYER_JUMP
        #self.canjump = False
        #self.num_jumps += 1
        

    def game_over(self):
        if not self.canjump and (self.pos.x > WIDTH or self.pos.x < 0):
            self.death = True

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc

        if self.rect.top <= 0:
            self.game_over()

        # Check if no keys are pressed and set acceleration and velocity to zero
        """if not any(pg.key.get_pressed()):
            self.acc.x = 0
            self.vel.x = 0
            self.acc.y = 0  # Set vertical acceleration to zero
        """
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        # Update canjump flag based on collision with platforms
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.canjump = True
            self.num_jumps = 0
        else:
            self.canjump = False

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        elif keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        else:
            self.acc.x = 0
        if keys[pg.K_UP]:
           # if self.canjump:
            self.jump()
        if keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if keys[pg.K_SPACE]:
            # Add additional movement logic here for player two sprite
            # For example, you can modify self.vel.y or self.vel.x to move the sprite vertically or horizontally
            pass
