import pygame
import neat
import time
import os
import random

WIN_WID = 500
WIN_HEI = 750

BIRDS = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird1.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird2.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird3.png")))
        ]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bg.png")))

class Bird:
    IMGS = BIRDS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIM_T = 5
    
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        if d >= 16 :
            d = 16
        if d < 0:
            d -= 2
        self.y = self.y + d
        
        if d < 0 or self.y < self.height + 50 :
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else :
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.img_count += 1
        if self.img_count < self.ANIM_T:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIM_T * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIM_T * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIM_T * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIM_T * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0  
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIM_T * 2
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0            
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL    
        
    def draw(self,win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x , self.top - round(bird.y))    
        bottom_offset = (self.x - bird.x , self.botyom - round(bird.y))
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if t_point or b_point:
            return True 
        return False       

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
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


def draw_window(win, bird, pipes, base):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)    
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(230,350)
    base = Base(700)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WID,WIN_HEI))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #bird.move()       
        base.move() 
        draw_window(win, bird, pipes, base)
                
    pygame.quit()
    quit()
   
main()                        
                                                                  