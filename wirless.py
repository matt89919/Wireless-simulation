import pygame
import random
import math
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

basearr = [[[0 for k in range(2)] for j in range(10)] for i in range(10)]

def path_loss(f,d):
    pl=32.45+20*math.log(f,10)+20*math.log(d,10)
    return pl

def drawmap():
    screen.fill((255,255,255))
    for i in range(11):
        pygame.draw.line(screen,black, (50,50+i*60) , (650,50+i*60) ,2)
    for i in range(11):
        pygame.draw.line(screen,black, (50+i*60,50) , (50+i*60,650))
       
class base(pygame.sprite.Sprite):
    def __init__(self,x,y,f):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((10,10))
        self.image.fill(blue)
        self.rect=self.image.get_rect()
        self.rect.center=self.get(x,y)
        self.f=f
        print(f'init basestation at {self.rect.center},frequency={self.f}')
    '''  
    def getdist(self):  
        i=0
        for car in cars:
                x=(self.rect.centerx-car.rect.centerx) ** 2
                y=(self.rect.centery-car.rect.centery) ** 2
                self.dist[i]= (x+y) ** (1/2)
                #print(f'dist to bs{i}={self.dist[i]}') 
                pl=path_loss()
                i+=1
                '''
        
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
        self.pl=[0 for i in range(len(bases.sprites()))]
        self.getdist()      #also calculate path loss and put in self.pl[]
        
    def getdist(self):
        i=0
        for bs in bases.sprites():
            x=(self.rect.centerx-bs.rect.centerx) ** 2
            y=(self.rect.centery-bs.rect.centery) ** 2
            d= ((x+y) ** (1/2)) / km
            #print(f'dist to bs{i}={self.dist[i]}')
            #k=(bs.rect.centerx-80)/60
            #print(bs.f)            
            self.pl[i]=120-path_loss(bs.f,d)
            #print(self.pl[i])
            i+=1
                   
    def update(self):
        #print(self.x,self.y)
        mx= round((self.x-50) %60 , 3)
        my= round((self.y-50) %60 , 3)

        #print(mx,my)
        if (mx == 60.000 or mx == 0 ) and (my == 0 or my == 60.000):
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
        #self.getdist()
        
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
                basearr[i][j][1]=1
                f=random.randrange(100,1100,100)
                basearr[i][j][1]=f
                x = 50+i*60+30
                y = 50+j*60+30
                newbase = base(x,y,f)
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
for i in range(60):
    newcar()

running=True

#start simulation
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            
            
    #newcar()        
    drawmap()
    all.draw(screen)
    all.update()
    pygame.display.update()
    
#quit
pygame.quit()