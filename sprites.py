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
        # these are the properties
        self.game = game
        self.image = pg.image.load('MJ.jpg').convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
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

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and (self.num_jumps < self.max_jumps):
            self.vel.y = -PLAYER_JUMP
            self.canjump = True
            self.num_jumps += 1
        elif self.num_jumps >= self.max_jumps:
            self.game_over()

    def game_over(self):
        self.game.screen.fill((0, 0, 0))
        font = pg.font.Font(None, 48)
        text = font.render("You have won it! You're the champion!!!", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (WIDTH/2, HEIGHT/2)
        self.game.screen.blit(text, text_rect)
        pg.display.flip()
        pg.time.wait(3000)
        pg.quit()
        sys.exit()

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

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
        self.color = color
        self.image.fill(self.color)
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
            self.rect.x = x - self.rect.width  # Adjust position on the left side
        else:
            self.rect.x = x  # Adjust position on the right side

        # Set the y-coordinate
        self.rect.y = y




class Player2(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load('lebron.jpg').convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(3, 7)
        self.acc = vec(0, 0)
        self.cofric = 0.1
        self.canjump = False
        self.standing = False
        self.num_jumps = 0
        self.death = False
        self.max_jumps = 12

def input(self):
    keys = pg.key.get_pressed()
    if self.standing:  # Only allow movement if Player 2 is standing on the ground
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        else:
            self.acc.x = 0
        if keys[pg.K_UP] or keys[pg.K_w]:
            if self.canjump:
                self.jump()
    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()


   
