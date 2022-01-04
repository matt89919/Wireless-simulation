import pygame
import random
import math
import numpy as np
import os

from varieble import *
#from scipy.stats import poisson

pygame.init()
screen = pygame.display.set_mode((700,700))
clock = pygame.time.Clock()

all = pygame.sprite.Group()
cars = pygame.sprite.Group()
bases = pygame.sprite.Group()

swt = 0
dc = 0

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
        self.pl=[0 for i in range(0,len(bases)+1)]
        self.getdist()                              #also calculate path loss and put in self.pl[]
        self.connect_to0=0                           #0 means didnt conncet to bs
        self.connect_to1=0
        self.connect_to2=0
        self.connect_to3=0
        self.switch0=0   
        self.switch1=0
        self.switch2=0
        self.switch3=0
        self.iscalling=0 
        self.count=0
        self.n=float(np.random.normal(300,10,1))*60    #the call time of this car
        #self.firstconnect()
        self.call()
   
    def getdist(self):
        i=0
        for bs in bases:
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
            
        self.getdist()
        if self.iscalling > 0:
            self.besteffort()           #algoalgo is here
            self.minimum_threshold()
            self.entropy()
            self.myalgo()
            self.count+=1
            if self.count>=self.n:
                self.iscalling=0
                self.connect_to=0
                print("release")
                
        else:
            self.call()
        
    def turn(self):
        r=random.randint(1,33)
        #print('turn')
        ## dir=0=go up, 1=go left, 2=go right, 3=go down
        if r<=16:
            #no turn
            self.dir=self.dir
            #print('no turn')
            
        elif r==17:
            #turn back
            if self.dir==0:
                self.dir=3
            elif self.dir==1:
                self.dir=2
            elif self.dir==2:
                self.dir=1
            elif self.dir==3:
                self.dir=0
            #print('turn back')
                
        elif r<=24:
            #turn left
            if self.dir==0:
                self.dir=1
            elif self.dir==1:
                self.dir=3
            elif self.dir==2:
                self.dir=0
            elif self.dir==3:
                self.dir=2   
            #print('turn left')        
            
        else :
            #turn right
            if self.dir==0:
                self.dir=2
            elif self.dir==1:
                self.dir=0
            elif self.dir==2:
                self.dir=3
            elif self.dir==3:
                self.dir=1
            #print('turn right')

    def besteffort(self):
        max=0
        b=0
        previous=self.connect_to0
        for bs in bases:
            if self.pl[b]>max:
                max=self.pl[b]
                self.connect_to0=bs
                b+=1
                
        if previous!=self.connect_to0:
            #print(f'connected to {self.connect_to.rect.center}')
            self.switch0+=1
            #print(f'switch={self.switch}')
        pygame.draw.line(screen,yellow, self.rect.center , self.connect_to0.rect.center)
        pygame.draw.line(screen,brown, self.rect.center , self.connect_to1.rect.center)
        pygame.draw.line(screen,purple, self.rect.center , self.connect_to2.rect.center)
        pygame.draw.line(screen,green, self.rect.center , self.connect_to3.rect.center)
            
    def minimum_threshold(self):
        threshold=25
        b=0
        previous=self.connect_to1
        for bs in bases:
            if self.connect_to1==bs:
                break
            else :b+=1
            
        if self.pl[b] < threshold:
            max=0
            b=0
            for bs in bases:
                if self.pl[b]>max:
                    max=self.pl[b]
                    self.connect_to1=bs
                    b+=1
        else: return
                
        if previous!=self.connect_to1:
            #print(f'connected to {self.connect_to.rect.center}')
            self.switch1+=1
            #print(f'switch={self.switch}')
            
        pygame.draw.line(screen,yellow, self.rect.center , self.connect_to0.rect.center)
        pygame.draw.line(screen,brown, self.rect.center , self.connect_to1.rect.center)
        pygame.draw.line(screen,purple, self.rect.center , self.connect_to2.rect.center)
        pygame.draw.line(screen,green, self.rect.center , self.connect_to3.rect.center)
     
    def entropy(self):
        entropy=5
        b=0
        previous=self.connect_to2
        for bs in bases:
            if self.connect_to2==bs:
                break
            else: b+=1
            
        original=self.pl[b]
        b=0
        for bs in bases:
            if self.pl[b] - original > entropy:
                original=self.pl[b]
                self.connect_to2=bs
                b+=1
            
                
        if previous!=self.connect_to2:
            #print(f'connected to {self.connect_to.rect.center}')
            self.switch2+=1
            #print(f'switch={self.switch}') 
        pygame.draw.line(screen,yellow, self.rect.center , self.connect_to0.rect.center)
        pygame.draw.line(screen,brown, self.rect.center , self.connect_to1.rect.center)
        pygame.draw.line(screen,purple, self.rect.center , self.connect_to2.rect.center)
        pygame.draw.line(screen,green, self.rect.center , self.connect_to3.rect.center)          
        
    def myalgo(self):
        entropy=10
        threshold=50
        b=0
        previous=self.connect_to3
        for bs in bases:
            if self.connect_to3==bs:
                break
            else: b+=1
            
        original=self.pl[b]
        if original > threshold:
            return
        b=0
        for bs in bases:
            if self.pl[b] - original > entropy:
                original=self.pl[b]
                self.connect_to3=bs
                b+=1
            
                
        if previous!=self.connect_to3:
            #print(f'connected to {self.connect_to.rect.center}')
            self.switch3+=1
            #print(f'switch={self.switch}')  
            
        pygame.draw.line(screen,yellow, self.rect.center , self.connect_to0.rect.center)
        pygame.draw.line(screen,brown, self.rect.center , self.connect_to1.rect.center)
        pygame.draw.line(screen,purple, self.rect.center , self.connect_to2.rect.center)
        pygame.draw.line(screen,green, self.rect.center , self.connect_to3.rect.center)          
        
    def firstconnect(self):
        max=0
        b=0

        for bs in bases:
            if self.pl[b]>max:
                max=self.pl[b]
                self.connect_to0=bs
                self.connect_to1=bs
                self.connect_to2=bs
                self.connect_to3=bs
                b+=1
                
        pygame.draw.line(screen,yellow, self.rect.center , self.connect_to0.rect.center)
        pygame.draw.line(screen,brown, self.rect.center , self.connect_to0.rect.center)
        pygame.draw.line(screen,purple, self.rect.center , self.connect_to0.rect.center)
        pygame.draw.line(screen,green, self.rect.center , self.connect_to0.rect.center)
                                
    def call(self):
        #print(self.n)
        r=random.randint(0,3600*10)
        if r==0:
            self.iscalling=1
            #print("call")
            self.firstconnect()
        
        
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
            #the prob. of per FPS(60) after calculate is about 0.001283, so i take 0.0013 to simulate
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
s0=0
ps0=0
s1=0
ps1=0
s2=0
ps2=0
s3=0
ps3=0
count=0

#start simulation
while running:
    clock.tick(240)         #time is 4 time quiker
    count+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
           
    n=0
    call=0
    for c in cars:
        n+=1
        if c.iscalling==1:
            call+=1
        
    if n!=0:
            
        ps0=s0     
        s0=0 
        n0=0
        for c in cars:
            s0+=c.switch0
            n0+=1
        
        

        #if ps0!=s0:
        
        
        ps1=s1     
        s1=0 
        n1=0
        for c in cars:
            s1+=c.switch1
            n1+=1

        #if ps1!=s1:
        

        ps2=s2     
        s2=0 
        n2=0
        for c in cars:
            s2+=c.switch2
            n2+=1

        #if ps2!=s2:
        

        ps3=s3     
        s3=0 
        n3=0
        for c in cars:
            s3+=c.switch3
            n3+=1

        #if ps3!=s3:
        

        if count==60:
            os.system("cls")
            count=0
            print(f'number of cars : {n}')
            print(f'number of calls : {call}')
            print(f'switch time per car (my algo)= {s3/n3}')  #the total switch time of all cars in system(if the car got out, thw switch time cause by it will be deduct)
            print(f'switch time per car (entropy)= {s2/n2}')  #the total switch time of all cars in system(if the car got out, thw switch time cause by it will be deduct)
            print(f'switch time per car (minimum threshold)= {s1/n1}')  #the total switch time of all cars in system(if the car got out, thw switch time cause by it will be deduct)
            print(f'switch time per car (best effort)= {s0/n0}')  #the total switch time of all cars in system(if the car got out, thw switch time cause by it will be deduct)
            
    newcar()        
    drawmap()
    all.draw(screen)
    all.update()
    pygame.display.update()
    
#quit
pygame.quit()