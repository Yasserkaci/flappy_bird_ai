import pygame
import neat
import time 
import os
import random
from InquirerPy import inquirer

pygame.init()

FONT = pygame.font.Font('flappy-font.ttf', 40)
BIRDS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
GAME_OVER = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","gameover.png")))
WIDTH = 550
HEIGHT = 900



class Bird:
    IMGS = BIRDS
    MAX_ROT = 25
    ROT_VAL = 20 
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilte = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.image_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d > 16 :
            d = 16

        if d < 0 :
            d -= 2

        self.y  = self.y + d

        if d < 0 or self.y < self.height + 50 :
            if self.tilte < self.MAX_ROT:
                self.tilte = self.MAX_ROT
        else:
            if self.tilte > -90 :
                self.tilte -= self.ROT_VAL

    def draw(self,win):
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.image_count < self.ANIMATION_TIME * 2 :
            self.img = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME * 3 :
            self.img = self.IMGS[2]
        elif self.image_count < self.ANIMATION_TIME * 4 :
            self.img = self.IMGS[1]
        elif self.image_count == self.ANIMATION_TIME * 4 + 1 :
            self.img = self.IMGS[0]
            self.image_count = 0

        if self.tilte <= -80 :
            self.img = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME * 2

        # stolen from stack overflow

        rotated_image = pygame.transform.rotate(self.img, self.tilte)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    

class Pipe:
    GAP = 200
    VEL  = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.TOP_PIPE = pygame.transform.flip(PIPE, False, True)
        self.BOTTOM_PIPE = PIPE

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.TOP_PIPE.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.TOP_PIPE, (self.x, self.top))
        win.blit(self.BOTTOM_PIPE, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_PIPE)
        bottom_mask = pygame.mask.from_surface(self.BOTTOM_PIPE)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            print("true")
            return True

        print("false")
        return False

class Base:

    VEL = 5
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):

        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

    def collide(self, bird):
        if bird.y >= 750 :
            return True
        return False

        

def draw_window(win, bird, pipes, base,score):
    
    win.blit(BG,(0,0))
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255)) 

   
    for pipe in pipes:
        pipe.draw(win)
        

        

    base.draw(win)


    bird.draw(win)

    win.blit(score_text, (10, 10)) 

def game():

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    # Bring the window to the front
    pygame.event.post(pygame.event.Event(pygame.ACTIVEEVENT, gain=1, state=6))
    bird = Bird(50, 400)
    pipes = [Pipe(300),Pipe(600),Pipe(900)]
    base = Base(800)
    run = True
    game_over = False
    add_pipe = False
    score = 0
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))

    

    while run:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                   bird.jump()
                      
        

        draw_window(win, bird, pipes,base,score)

        for pipe in pipes:
            if pipe.collide(bird) or base.collide(bird) :
                game_over = True
                win.blit(GAME_OVER, (100,350))
                win.blit(score_text, (200, 500)) 

            rem=[]

            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x :
                pipe.passed = True
                add_pipe = True
            
            if add_pipe :
                score += 1
                pipes.append(Pipe(900))
                add_pipe = False

            for r in rem :
                pipes.remove(r)
                  
            if not game_over : pipe.move()

        if not game_over : 
            base.move()
            bird.move()
        print(bird.image_count)
        pygame.display.update()
                
    pygame.quit()
    quit()


game()
