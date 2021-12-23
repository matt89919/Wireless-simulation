import pygame
import random
import os

#from pygame.draw import rect
from varieble import *


pygame.init()
screen = pygame.display.set_mode((700,700))
clock = pygame.time.Clock()

all = pygame.sprite.Group()
cars = pygame.sprite.Group()
bases = pygame.sprite.Group()

basearr = [[0 for x in range(10)] for y in range(10)]

def drawmap():
    screen.fill((255,255,255))
    for i in range(11):
        pygame.draw.line(screen,black, (50,50+i*60) , (650,50+i*60) ,2)
    for i in range(11):
        pygame.draw.line(screen,black, (50+i*60,50) , (50+i*60,650))
       
class base(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((10,10))
        self.image.fill(blue)
        self.rect=self.image.get_rect()
        self.rect.center=self.get(x,y)
        self.f=random.randint(100,1000)
        print(f'init basestation at {self.rect.center}')
        
    def get(self,x,y):
        num=random.randint(0,3)
        if num==0:
            x+=15
        if num==1:
            x-=15
        if num==2:
            y+=15
        if num==3:
            y-=15
        return (x,y)

def initserver():
    for i in range(0,10):
        for j in range(0,10):
            r=random.randint(1,10)
            if r==1:
                basearr[i][j]=1
                x = 50+i*60+30
                y = 50+j*60+30
                newbase = base(x,y)
                bases.add(newbase)
                all.add(newbase)
                

#initialization      
initserver()
running=True

#start simulation
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            
            
            
    drawmap()
    all.draw(screen)
    pygame.display.update()
    
pygame.quit()