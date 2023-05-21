import pygame as pg
import os
from settings import *
from sprites import *
from settings import PLAYER_JUMP
# Sources: http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
# Sources: https://www.w3schools.com/
# Sources: https://www.w3schools.com/c/c_syntax.php
# Sources: https://www.w3schools.com/c/c_data_types.php
# Sources: https://www.geeksforgeeks.org/python-arcade-player-movement/
# Sources: https://www.geeksforgeeks.org/how-to-move-your-game-character-around-in-pygame/
# Sources: https://www.geeksforgeeks.org/python-arcade-collision-detection/
# Goals:
# Make a two player game-Done
# Add collisions between players and basketball-Done
# Add Basketball Hoops-Done
# Add a scoreboard-Done
# Add a winner screen for player and player 2- done
# 1v1 game complete






pg.init()

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
        self.timer = 0  # Total elapsed time in milliseconds
        self.start_time = pg.time.get_ticks()  # Starting time of the game in milliseconds
        self.timer_font = pg.font.Font(None, 36)  # Font for the timer
        self.winner = None
        self.paused = False

    def update(self):
        self.update_timer()

        events2 = pygame.event.get()

        for event2 in events2:
            if event2.type ==pygame.KEYDOWN:
                self.paused = False

        if not self.paused:
            self.all_sprites.update()
        else:
            self.player2.update()
        self.player.game_over()
        self.player2.game_over()

        delta = 0.2

        if self.player.vel.x > 0:
            self.player.vel.x -=delta
        if self.player.vel.x < 0:
            self.player.vel.x +=delta

        if(self.player.vel.x <= 0.1 and self.player.vel.x >= -0.1):
            self.player.vel.x = 0

        if self.player2.vel.x > 0:
            self.player2.vel.x -=delta
        if self.player2.vel.x < 0:
            self.player2.vel.x +=delta

        if(self.player2.vel.x <= 0.1 and self.player2.vel.x >= -0.1):
            self.player2.vel.x = 0

        #hit basketball
        if self.player2.vel.y > 0:
            hits =  pg.sprite.spritecollide(self.player2, self.platforms, False)

            if hits:
                self.player2.standing = True

                if hits[0].variant == "disappearing":
                    hits[0].kill()
                elif hits[0].variant == "bouncey":
                    self.player2.pos.y = hits[0].rect.top
                    self.player2.vel.y = -PLAYER_JUMP
                else:
                    self.player2.pos.y = hits[0].rect.top
                    self.player2.vel.y = 0
            else:
                self.player2.standing = False

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)

            if hits:
                self.player.standing = True

                if hits[0].variant == "disappearing":
                    hits[0].kill()
                elif hits[0].variant == "bouncey":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -PLAYER_JUMP
                else:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
            else:
                self.player.standing = False

        
        hit_ball = pg.sprite.collide_rect(self.player, self.b)
        if hit_ball:
            self.b.vel.y -=5
            if self.player.rect.x <= self.b.rect.x:
                self.b.vel.x=5
            if self.player.rect.x > self.b.rect.x:
                self.b.vel.x=-5

        hit_ball = pg.sprite.collide_rect(self.player2, self.b)
        if hit_ball:
            self.b.vel.y -=5

            if self.player2.rect.x <= self.b.rect.x:
                self.b.vel.x=5
            if self.player2.rect.x > self.b.rect.x:
                self.b.vel.x=-5


        delta = 0.01
        if self.b.vel.x > 0:
            self.b.vel.x -=delta
        if self.b.vel.x < 0:
            self.b.vel.x +=delta

        if(self.b.vel.x <= 0.1 and self.b.vel.x >= -0.1):
            self.b.vel.x = 0

        #check if basketball hit hoops
        
        hit_right_hoop = pg.sprite.collide_rect(self.b, self.right_hoop)
        hit_left_hoop = pg.sprite.collide_rect(self.b, self.left_hoop)

        if hit_right_hoop:
            self.player.score+=1
            
        if hit_left_hoop:
            self.player2.score+=1

        if hit_right_hoop or hit_left_hoop:
            self.all_sprites.remove(self.b)
            self.b = Basketball(40, 40)
            self.all_sprites.add(self.b)

        #reach 10 points to win
        if self.player.score >= 10 and self.winner == None:
            self.winner = "Player 1"
            self.paused = True
        
        if self.player2.score >= 10 and self.winner == None:
            self.winner = "Player 2"
            self.paused = True



    def update_timer(self):
        # Calculate the elapsed time in milliseconds
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.start_time

        # Update the timer variable with the elapsed time
        self.timer = elapsed_time

        # Check if one minute (60 seconds) has passed
 

    def game_over(self):
        # Game over logic goes here
        pass

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)

        # Display the score on the top-right corner of the screen
        score_text = "Player 1 score: {}".format(self.player.score)  # Convert milliseconds to seconds
        score_surface = self.timer_font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(topright=(WIDTH - 300, 100))
        self.screen.blit(score_surface, score_rect)

        score_text = "Player 2 score: {}".format(self.player2.score)  # Convert milliseconds to seconds
        score_surface = self.timer_font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(topright=(WIDTH - 300, 150))
        self.screen.blit(score_surface, score_rect)

        #draw winner
        if self.winner!=None:
            score_text = "Winner: {}".format(self.winner)  # Convert milliseconds to seconds
            score_surface = self.timer_font.render(score_text, True, WHITE)
            score_rect = score_surface.get_rect(topright=(WIDTH - 300, 200))
            self.screen.blit(score_surface, score_rect)

        if self.player.standing:
            self.draw_text("1v1 first to 10 remember to stay inbonds press any key to restart", 24, RED, WIDTH/2, HEIGHT/2)

        if self.player.death or self.player2.death:
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

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150, 150, 150), "normal")
        self.all_sprites.add(self.plat1)
        self.platforms.add(self.plat1)
        self.all_sprites.add(self.player)

        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        for _ in range(0, 10):
            m = Mob(20, 20, (0, 255, 0))
            self.all_sprites.add(m)
            self.enemies.add(m)

        for _ in range(0, 1):
            self.b = Basketball(40, 40)
            self.all_sprites.add(self.b)
            self.enemies.add(self.b)

        self.left_hoop = BasketballHoop(WIDTH/4, HEIGHT/2)
        self.right_hoop = BasketballHoop(WIDTH * 3/4, HEIGHT/2)
        self.all_sprites.add(self.left_hoop, self.right_hoop)
        self.enemies.add(self.left_hoop, self.right_hoop)

        self.player2 = Player2(self)
        self.all_sprites.add(self.player2)
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
            if self.paused:
                self.paused = False
                self.winner = None
                self.player.score = 0
                self.player.score = 0
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
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            # Player 2 movement
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and self.player2.acc.x < 0:
                    self.player2.acc.x = 0
                elif event.key == pg.K_RIGHT and self.player2.acc.x > 0:
                    self.player2.acc.x = 0

g = Game()

while g.running:
    g.new()

pg.quit()
