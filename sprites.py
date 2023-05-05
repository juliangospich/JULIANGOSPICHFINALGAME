import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
import sys



vec = pg.math.Vector2

# player class


class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # these are the properties
        self.game = game
        self.image = pg.image.load('MJ.jpg').convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
        self.standing = False
        self.num_jumps = 0
        self.death = False
        self.max_jumps = 4  # new attribute to allow four jumps
           
    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and (self.num_jumps < self.max_jumps):  # check if max_jumps is not reached
            self.vel.y = -PLAYER_JUMP
            self.canjump = True
            self.num_jumps += 1  # increment num_jumps when the player jumps
        elif self.num_jumps >= self.max_jumps:  # check if max_jumps is reached
            self.game_over()
    
    def game_over(self):
        self.game.screen.fill((0, 0, 0))  # fill screen with black
        font = pg.font.Font(None, 48)  # create a font object
        text = font.render("You have won it! You're the champion!!!", True, (255, 255, 255))  # create a text object
        text_rect = text.get_rect()  # get the rectangle of the text object
        text_rect.center = (WIDTH/2, HEIGHT/2)  # center the rectangle on the screen
        self.game.screen.blit(text, text_rect)  # draw the text object on the screen
        pg.display.flip()  # update the screen
        pg.time.wait(3000)  # wait for 3 seconds
        pg.quit()  # quit pygame
        sys.exit()  # exit the program
    
    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        
        # check if player falls off the screen
        if self.rect.top > HEIGHT:
            self.game_over()

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP] or keys[pg.K_w]:
            if self.canjump:
                self.jump()
        if keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()


        

    
    def inbounds(self):
        if self.rect.x > WIDTH - 50:
            self.pos.x = WIDTH - 25
            self.vel.x = 0
            print("i am off the right side of the screen...")
        if self.rect.x < 0:
            self.pos.x = 25
            self.vel.x = 0
            print("i am off the left side of the screen...")
        if self.rect.y > HEIGHT:
            print("i am off the bottom of the screen")
        if self.rect.y < 0:
            print("i am off the top of the screen...")
    def mob_collide(self):
            hits = pg.sprite.spritecollide(self, self.game.enemies, True)
            if hits:
                print("you collided with an enemy...")
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
    def __init__(self,width,height, color):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(randint(1,5),randint(1,5))
        self.acc = vec(1,1)
        self.cofric = 0.01
    # ...
    def inbounds(self):
        if self.rect.x > WIDTH:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.x < 0:
            self.vel.x *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y < 0:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
        if self.rect.y > HEIGHT:
            self.vel.y *= -1
            # self.acc = self.vel * -self.cofric
    def update(self):
        self.inbounds()
        # self.pos.x += self.vel.x
        # self.pos.y += self.vel.y
        self.pos += self.vel
        self.rect.center = self.pos

# create a new platform class...

class Platform(Sprite):
    def __init__(self, x, y, width, height, color, variant):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.variant = variant