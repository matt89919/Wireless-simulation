import pygame
import random
import os

#from pygame.draw import rect
from varieble import *
from scipy.stats import poisson

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

class car(pygame.sprite.Sprite):
    def __init__(self,x,y,dir):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((10,10))
        self.image.fill(red)
        self.rect=self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.center=((x,y))
        self.dir=dir
        
        #self.speed=speed
        
    def update(self):
        #print(self.x,self.y)
        mx= round((self.x-50) %60 , 3)
        my= round((self.y-50) %60 , 3)

        #print(mx,my)
        if (mx == 60.000 or mx == 0 ) and (my == 0 or my==60.000):
            self.turn()
            
        if self.dir == 0:
            self.y -= speed
        elif self.dir == 1:
            self.x -= speed
        elif self.dir == 2:
            self.x += speed
        elif self.dir == 3:
            self.y += speed     
        else:
            print(self.dir)  
            
        self.rect.center=(self.x,self.y)
        if self.rect.centerx > 650 or self.rect.centery < 50 or self.rect.centerx < 50 or self.rect.centery > 650:
            self.kill()
        
    def turn(self):
        r=random.randint(1,33)
        print('turn')
        ## dir=0=go up, 1=go left, 2=go right, 3=go down
        if r<=16:
            #no turn
            self.dir=self.dir
            print('no turn')
            
        elif r==17:
            #turn back
            if self.dir==0:
                self.dir=3
            if self.dir==1:
                self.dir=2
            if self.dir==2:
                self.dir=1
            if self.dir==3:
                self.dir=0
            print('turn back')
                
        elif r<=24:
            #turn left
            if self.dir==0:
                self.dir=1
            if self.dir==1:
                self.dir=3
            if self.dir==2:
                self.dir=0
            if self.dir==3:
                self.dir=2   
            print('turn left')        
            
        else :
            #turn right
            if self.dir==0:
                self.dir=2
            if self.dir==1:
                self.dir=0
            if self.dir==2:
                self.dir=3
            if self.dir==3:
                self.dir=1
            print('turn right')
                 
            
        

def initserver():
    for i in range(0,10):
        for j in range(0,10):
            r=random.randint(1,11)
            if r==1:
                basearr[i][j]=1
                x = 50+i*60+30
                y = 50+j*60+30
                newbase = base(x,y)
                bases.add(newbase)
                all.add(newbase)
                

def newcar():
    for i in range(0,4):
        for j in range(1,10):
            r=random.randint(0,10000)
            #the prob. of per FPS after calculate is about 0.001283, so i take 0.0013 to simulate
            if r<13:
                if i==0:
                    n=car(51,50+60*j,2)
                if i==1:
                    n=car(649,50+60*j,1)
                if i==2:
                    n=car(50+60*j,51,3)
                if i==3:
                    n=car(50+60*j,649,0)
                
                cars.add(n)
                all.add(n)

#initialization      
initserver()


running=True

#start simulation
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            
            
    newcar()        
    drawmap()
    all.draw(screen)
    all.update()
    pygame.display.update()
    
#quit
pygame.quit()