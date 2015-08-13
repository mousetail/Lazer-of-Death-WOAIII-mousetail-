'''
Created on 10 aug. 2015

@author: Maurits
'''
import math, pygame, random


class Shape(pygame.sprite.Sprite):
    '''
    Any shape
    '''


    def __init__(self, position, image, angle=0, speed=(0,0),friction=0.1,maxspeed=20,maxpos=(1000,500),radius=32,groups=(), gui=None):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self,*groups)
        
        self.position=list(position)
        self.image=image
        self.angle=angle
        self.speed=list(speed)
        self.friction=1-friction
        self.maxspeed=maxspeed
        self.maxspeed2=maxspeed**2
        self.radius=radius
        self.rotate(0)
        self.maxpos=maxpos
        self.rect=self.image.get_rect()
        self.GUI=gui
        self.dieonwall=False
        
        self.firerate=5
        self.num=0
    def update(self):
        for i in xrange(2):
            
            self.position[i]=self.position[i]+self.speed[i]
            self.speed[i]*=self.friction
            if self.position[i]>self.maxpos[i]:
                if self.dieonwall:
                    self.kill()
                else:
                    self.position[i]=self.maxpos[i]
                    self.speed[i]=-self.speed[i]
                    self.angle=math.degrees(math.atan2(-self.speed[0], -self.speed[1]))
                    self.rotate(0)
            elif self.position[i]<0:
                if self.dieonwall:
                    self.kill()
                else:
                    self.position[i]=0
                    self.speed[i]=-self.speed[i]
                    self.angle=math.degrees(math.atan2(-self.speed[0], -self.speed[1]))
                    self.rotate(0)
        self.rect.center=self.position
    def rotate(self, angle):
        
        self.angle+=angle
        self.rotimage=pygame.transform.rotate(self.image,self.angle)
        
    def draw(self,surface,offset):
        size=self.rotimage.get_size()
        if sum(self.position[i]+offset[i]+size[i]>0 for i in xrange(2)):
            surface.blit(self.rotimage,tuple(self.position[i]-size[i]/2+offset[i] for i in xrange(2)))
    def event(self,event):
        pass
    def accelarate(self, ammount):
        x=-math.sin(math.radians(self.angle))*ammount
        y=-math.cos(math.radians(self.angle))*ammount
        self.speed[0]+=x
        self.speed[1]+=y
        
   
    
    def fire(self):
        if self.num==0:
            bul=Bullet(self.position,self.GUI.bullet_img,angle=self.angle,friction=0,radius=4,maxpos=self.maxpos)
            bul.accelarate(12)
            self.GUI.add_bullet(bul)
        self.num-=1
        if self.num<0:
            self.num=self.firerate
    def explode(self):
        coins=[]
        for i in range(14):
            angle=random.randint(0,360)
            coins.append(coin.Coin(self.position,self.GUI.coin_img,angle,radius=128,gui=self.GUI,value=1,maxpos=self.maxpos))
        for i in coins:
            i.accelarate(random.randint(6,12))
            self.GUI.add_coin(i)
class Bullet(Shape):
    def __init__(self,*args,**kwargs):
        Shape.__init__(self,*args,**kwargs)
        #print "made bullet"
        self.dieonwall=True
        self.timeout=60
    def update(self):
        Shape.update(self)
        if self.timeout:
            self.timeout-=1
class Player(Shape):
    def update(self):
        Shape.update(self)
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
                self.rotate(-5)
        if keys[pygame.K_RIGHT]:
                self.rotate(5)
        if keys[pygame.K_UP]:
                self.accelarate(1)
        if keys[pygame.K_DOWN]:
                self.accelarate(-1)
        if keys[pygame.K_z]:
                self.fire()
    def event(self, event):
        pass
        #if event.type==pygame.KEYDOWN:
        #    if event.key==pygame.K_z:
    def draw(self, *args, **kwargs):
        if self.GUI.player_immune%16<8:
            Shape.draw(self, *args, **kwargs)
class Accelerator(Shape):
    def __init__(self, *args, **kwargs):
        if ("accel" in kwargs.keys()):
            self.acceleration=kwargs["accel"]
            del kwargs["accel"]
        else:
            self.acceleration=1
        
        Shape.__init__(self, *args, **kwargs)
    def update(self):
        Shape.update(self)
        self.accelarate(self.acceleration)
import coin