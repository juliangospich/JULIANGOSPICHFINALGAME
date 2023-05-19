import pygame as pg
import os
from settings import *
from sprites import *
# Sources: http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
# Sources: https://www.w3schools.com/
# Sources: https://www.w3schools.com/c/c_syntax.php
# Sources: https://www.w3schools.com/c/c_data_types.php


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.score = 0

    def game_over(self):
        if self.player.pos.x > 800 or self.player.pos.x < 0:
            self.player.death = True

    def new(self):
        def new(self):
            self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.player2 = Player2(self)  # Create an instance for Player2
        self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150, 150, 150), "normal")
        self.all_sprites.add(self.plat1)
        self.platforms.add(self.plat1)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player2)  # Add the second player sprite to the all_sprites group

    # Rest of the code...

        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        for _ in range(0, 10):
            m = Mob(20, 20, (0, 255, 0))
            self.all_sprites.add(m)
            self.enemies.add(m)

        for _ in range(0, 1):
            b = Basketball(40, 40)
            self.all_sprites.add(b)
            self.enemies.add(b)

        left_hoop = BasketballHoop(WIDTH/4, HEIGHT/2)
        right_hoop = BasketballHoop(WIDTH * 3/4, HEIGHT/2)
        self.all_sprites.add(left_hoop, right_hoop)
        self.enemies.add(left_hoop, right_hoop)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
     for event in pg.event.get():
        if event.type == pg.QUIT:
            if self.playing:
                self.playing = False
            self.running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.player.jump()
            # Player 2 movement
            if event.key == pg.K_LEFT:
                self.player2.acc.x = -PLAYER_ACC
            elif event.key == pg.K_RIGHT:
                self.player2.acc.x = PLAYER_ACC
            elif event.key == pg.K_UP and self.player2.standing:
                self.player2.jump()
        # Player 2 movement
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT and self.player2.acc.x < 0:
                self.player2.acc.x = 0
            elif event.key == pg.K_RIGHT and self.player2.acc.x > 0:
                self.player2.acc.x = 0

    def update(self):
        self.all_sprites.update()
        self.game_over()

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False) or pg.sprite.spritecollide(self.player2, self.platforms, False)

            if hits:
                self.player.standing = True
                self.player2.standing = True

                if hits[0].variant == "disappearing":
                    hits[0].kill()
                elif hits[0].variant == "bouncey":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -PLAYER_JUMP
                    self.player2.pos.y = hits[0].rect.top
                    self.player2.vel.y = -PLAYER_JUMP
                else:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                    self.player2.pos.y = hits[0].rect.top
                    self.player2.vel.y = 0
            else:
                self.player.standing = False
                self.player2.standing = False

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)

        if self.player.standing:
            self.draw_text("1v1 First one to 3!!!", 24, RED, WIDTH/2, HEIGHT/2)

        if self.player.death:
            self.screen.fill(BLACK)
            self.draw_text("Out of Bounds!!!!", 24, WHITE, WIDTH/2, HEIGHT/2)

        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def get_mouse_now(self):
        x, y = pg.mouse.get_pos()
        return (x, y)
    

g = Game()

while g.running:
    g.new()

pg.quit()
