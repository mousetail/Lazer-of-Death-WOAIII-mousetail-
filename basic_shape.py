'''
Created on 10 aug. 2015

@author: Maurits
'''
import math, pygame, random

WALLBEHAVIOR_DIE=3
WALLBEHAVIOR_BOUNCE=5
WALLBEHAVIOR_NONE=9

class Shape(pygame.sprite.Sprite):
    '''
    Any shape
    '''
    numcoins=7

    def __init__(self, position, image, angle=0, speed=(0,0),friction=0.1,maxspeed=20,maxpos=(1000,500),
                 radius=32,groups=(), numcoins=None,
                 gui=None, rotates=True, wallbehavior=WALLBEHAVIOR_BOUNCE,
                 ID=0):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self,*groups)
        
        self.position=list(position)
        self.image=image
        self.angle=angle
        self.speed=list(speed)
        self.rotates=rotates
        self.friction=1-friction
        self.maxspeed=maxspeed
        self.maxspeed2=maxspeed**2
        self.radius=radius
        self.rotate(0)
        self.maxpos=maxpos
        self.rect=self.image.get_rect()
        self.GUI=gui
        self.wallbehavior=wallbehavior
        self.firerate=20
        self.num=0
        self.ID=ID
        if numcoins is not None:
            self.numcoins=numcoins
    def update(self):
        for i in xrange(2):
            
            self.position[i]=self.position[i]+self.speed[i]
            self.speed[i]*=self.friction
            if self.position[i]>self.maxpos[i]:
                if self.wallbehavior==WALLBEHAVIOR_DIE:
                    self.kill()
                elif self.wallbehavior==WALLBEHAVIOR_BOUNCE:
                    self.position[i]=self.maxpos[i]
                    self.speed[i]=-self.speed[i]
                    if self.rotates:
                        self.angle=math.degrees(math.atan2(-self.speed[0], -self.speed[1]))
                        self.rotate(0)
                elif self.wallbehavior==WALLBEHAVIOR_NONE:
                    pass
                else:
                    raise ValueError(str(self.wallbehavior)+" is not a valid value")
            elif self.position[i]<0:
                if self.wallbehavior==WALLBEHAVIOR_DIE:
                    self.kill()
                elif self.wallbehavior==WALLBEHAVIOR_BOUNCE:
                    self.position[i]=0
                    self.speed[i]=-self.speed[i]
                    if self.rotates:
                        self.angle=math.degrees(math.atan2(-self.speed[0], -self.speed[1]))
                        self.rotate(0)
                elif self.wallbehavior==WALLBEHAVIOR_NONE:
                    pass
                else:
                    raise ValueError(str(self.wallbehavior)+" is not a valid value")
        self.rect.center=self.position
    def rotate(self, angle):
        
        self.angle+=angle
        if self.rotates:
            self.rotimage=pygame.transform.rotate(self.image,self.angle)
        
    def draw(self,surface,offset):
        if self.rotates:
            img=self.rotimage
            size=self.rotimage.get_size()
        else:
            img=self.image
            size=self.image.get_size()
            
        if sum(self.position[i]+offset[i]+size[i]>0 for i in xrange(2)):
            surface.blit(img,tuple(self.position[i]-size[i]/2+offset[i] for i in xrange(2)))
    def event(self,event):
        pass
    def accelarate(self, ammount):
        x=-math.sin(math.radians(self.angle))*ammount
        y=-math.cos(math.radians(self.angle))*ammount
        self.speed[0]+=x
        self.speed[1]+=y
        
   
    
    def fire(self, calcscore=True):
        if self.num==0:
            bul=Bullet(self.position,self.GUI.bullet_img,angle=self.angle,friction=0,radius=4,maxpos=self.maxpos,rotates=False)
            bul.accelarate(12)
            bul.calcscore=calcscore
            bul.shooter=self
            self.GUI.add_bullet(bul)
        self.num-=1
        if self.num<0:
            self.num=self.firerate
    def explode(self,bullet):
        coins=[]
        for i in range(self.numcoins):
            angle=random.randint(0,360)
            coins.append(coin.Coin(self.position,self.GUI.coin_img,angle,radius=128,gui=self.GUI,value=random.randint(1,3),
                                   maxpos=self.maxpos,calcscore=bullet.calcscore,rotates=False))
        for i in coins:
            i.accelarate(random.randint(2,self.numcoins//2))
            self.GUI.add_coin(i)
        
    def hit(self):
        """Return killself, killbullet"""
        return True, True
class Bullet(Shape):
    def __init__(self,*args,**kwargs):
        Shape.__init__(self,*args,**kwargs)
        #print "made bullet"
        self.wallbehavior=WALLBEHAVIOR_DIE
        self.timeout=7
    def update(self):
        Shape.update(self)
        if self.timeout:
            self.timeout-=1
            
class Orange_Rect(Shape):
    def __init__(self, otherimage, *args, **kwargs):
        Shape.__init__(self, *args, **kwargs)
        self.subitems=[]
        self.rotAngle=0
        for i in range(4):
            self.subitems.append(Rect_orbit(position=self.position[:], gui=self.GUI, speed=[0,0],
                                            radius=16, image=otherimage, groups=self.groups(),
                                            rotates=False, wallbehavior=WALLBEHAVIOR_NONE,
                                            friction=0, maxpos=self.maxpos, ID=-1))
    def update(self):
        Shape.update(self)
        self.rotAngle+=0.1
        sin=math.sin(self.rotAngle)*128
        cos=math.cos(self.rotAngle)*128
        if self.subitems[0]!=None:
            self.subitems[0].position[0]=self.position[0]+sin
            self.subitems[0].position[1]=self.position[1]+cos
        if self.subitems[1]!=None:
            self.subitems[1].position[0]=self.position[0]+cos
            self.subitems[1].position[1]=self.position[1]-sin
        if self.subitems[2]!=None:
            self.subitems[2].position[0]=self.position[0]-sin
            self.subitems[2].position[1]=self.position[1]-cos
        if self.subitems[3]!=None:
            self.subitems[3].position[0]=self.position[0]-cos
            self.subitems[3].position[1]=self.position[1]+sin
    def hit(self):
        l=list(range(4))
        random.shuffle(l)
        item=None
        index=-1
        for i in l:
            if self.subitems[i]!=None:
                item=self.subitems[i]
                index=i
                break
        if item is None:
            return True, True
        self.subitems[index]=None
        item.speed=[math.cos(self.rotAngle+(index*math.pi/2))*12,-math.sin(self.rotAngle+(index*math.pi/2))*12]
        item.wallbehavior=WALLBEHAVIOR_DIE
        return False, True
        
class Rect_orbit(Shape):
    def hit(self):
        return False, True
    def updateF(self):
        pass
            
class Player(Shape):
    def update(self):
        Shape.update(self)
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
                self.rotate(5)
        if keys[pygame.K_RIGHT]:
                self.rotate(-5)
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
    numcoins=15
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
class RotateCellerator(Accelerator):
    numcoins=20
    def __init__(self, *args, **kwargs):
        Accelerator.__init__(self,*args,**kwargs)
        self.direction=1
    def update(self):
        Accelerator.update(self)
        self.rotate(self.direction)
        if random.randint(0,12)==0:
            self.direction+=random.randint(-2,2)
            if self.direction>10:
                self.direction=10
            elif self.direction<-10:
                self.direction=-10
class Shooter(RotateCellerator):
    numcoins=25
    def update(self):
        RotateCellerator.update(self)
        if random.randint(0,2)==1:
            self.fire(False)
class Turtle(Shape):
    numcoins=30
    def __init__(self, *args, **kwargs):
        Shape.__init__(self, *args, **kwargs)
        self.lives=9
        self.maxlives=9
    def draw(self, surface, offset):
        Shape.draw(self, surface, offset)
        surface.fill((0,255,0),(self.position[0]+offset[0]-90,self.position[1]-100+offset[1],10*self.lives,10))
    def hit(self):
        self.lives-=1
        if self.lives<=0:
            return True, True
        else:
            return False, True
        
import coin