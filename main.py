'''
Created on 10 aug. 2015

@author: Maurits
'''
import pygame
import basic_shape
import random
import time
import coin
import textutil
import string

class GUI(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def start(self):
        self.score=0
        self.trans=False
        pygame.init()
        self.screen=pygame.display.set_mode((1200,600))
        self.planeimage=pygame.image.load("plane.png").convert_alpha()
        self.astroid_image=pygame.image.load("astroid.png").convert_alpha()
        self.backimage=pygame.image.load("background.png").convert()
        self.bullet_img=pygame.image.load("bullet.png").convert_alpha()
        self.coin_img=pygame.image.load("coin.png").convert_alpha()
        self.player_image=pygame.image.load("player_plane.png").convert_alpha()
        self.background_special_image=pygame.image.load("background_special.png").convert()
        self.running=True;
        self.world_size=(3000,3000)
        #self.player.gui=self
        
        
        self.player=None
        self.state="menu"
        self.objects=pygame.sprite.Group()
        self.enemies=pygame.sprite.Group()
        self.bullets=pygame.sprite.Group()
        self.coins=pygame.sprite.Group()
        self.astroids=pygame.sprite.Group()
        self.special_coins=pygame.sprite.Group()
        pygame.key.set_repeat(100,100)
        self.clock=pygame.time.Clock()
        self.transsurface=pygame.Surface(self.screen.get_size())
        for i in range(50):
            self.addrandom()
        self.font=pygame.font.SysFont("Subway Ticker", 30, False, False)
        self.startmenu()
        
    def startgame(self):
        self.transstart()
        self.player=basic_shape.Player((self.world_size[0]/2,self.world_size[1]/2),self.player_image,45,(10,10),gui=self,maxpos=self.world_size,
                                       )
        self.state="game"
        self.objects.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.coins.empty()
        self.astroids.empty()
        self.objects.add(self.player)
        for i in range(50):
            self.addrandom()
        self.score=0
        self.endtime=time.time()+60
        self.deaths=0
        self.player_immune=False
    def startmenu(self):
        self.transstart()
        self.state="menu"
        size=self.screen.get_size()
        self.menusurf=pygame.Surface(size,pygame.SRCALPHA)
        self.menusurf.fill((0,255,0,200),(size[0]//2-200,0,400,600))
        textutil.drawtextcentered(self.menusurf, (size[0]//2,60), self.font, "Lazer of death")
        textutil.drawtextcentered(self.menusurf, (size[0]//2,550), self.font, "Press enter to play")
        if self.player:
            self.player.kill()
            self.player=None
    def starthighscore(self):
        self.transstart()
        if self.player:
            self.player.kill()
            self.player=None
        self.state="score"
        
        self.name="Bob"
        
        size=self.screen.get_size()
        self.menusurf=pygame.Surface(size, pygame.SRCALPHA)
        self.menusurf.fill((0,255,0,200),(size[0]//2-200,0,400,600))
        textutil.drawtextcentered(self.menusurf, (size[0]//2,40), self.font, "Lazer of death")
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2-180,100), self.font, "Base score:",alignment=(0,1))
        textutil.drawtextcentered(self.menusurf, (size[0]//2+180,100), self.font, "{0:05d}".format(self.score), alignment=(2,1))
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2-180,160), self.font, "Death Penalty:",alignment=(0,1))
        textutil.drawtextcentered(self.menusurf, (size[0]//2+180,160), self.font, "{0:05d}".format(100*self.deaths),color=(255,0,0),
                                   alignment=(2,1))
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2-180,220), self.font, "Total score:",alignment=(0,1))
        textutil.drawtextcentered(self.menusurf, (size[0]//2+180,220), self.font, "{0:05d}".format(self.score-100*self.deaths),
                                   alignment=(2,1))
        
        pygame.draw.line(self.menusurf,(255,255,255),(size[0]//2-185,190),(size[0]//2+185,190),2)
        pygame.draw.line(self.menusurf,(255,255,255),(size[0]//2+60,80),(size[0]//2+60,240),2)
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2,300), self.font, "enter your name: ")
        pygame.draw.rect(self.menusurf,(255,255,255),(size[0]//2-180,350,360,100),2)
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2,size[1]-10),self.font, "press enter to continue",alignment=(1,2))
        """
        self.menusurf.blit(self.font.render("Lazer of death",1,(255,255,255)),(size[0]//2-135,20))
        self.menusurf.blit(self.font.render("Base score: "+str(self.score),1,(255,255,255)),(size[0]//2-135,80))
        self.menusurf.blit(self.font.render("Death penalty: -"+str(100*self.deaths),1,(255,0,0)),(size[0]//2-135,140))
        self.menusurf.blit(self.font.render("Total score: "+str(self.score-100*self.deaths),1,(255,255,255)),(size[0]//2-135,200))
        """
        self.score=self.score-100*self.deaths
    def transstart(self):
        self.trans=True
        self.transsurface.blit(self.screen,(0,0))
        self.transamount=0
    def startdie(self):
        
        self.state="dead"
        self.transstart()
        self.transamount=0
        self.timeleft=-int(time.time()-self.endtime)
        
        for i in range(75):
            self.addrandom(angle=None, image=self.astroid_image, groups=(self.astroids, self.objects), speed=random.random()*5+3)
        for i in range(150):
            self.addrandom(coin.Coin, self.coin_img, None, random.random()*5, groups=(self.objects,self.special_coins),friction=0)
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.event()
            self.update()
            self.draw()
    def draw(self):
        size=self.screen.get_size()
        
        #self.screen.fill((0,0,0))
        if self.player:
            self.offset=[-self.player.position[i] + self.screen.get_size()[i]//2 for i in xrange(2)]
            for i in xrange(2):
                if self.offset[i]<-self.world_size[i]+size[i]:
                    self.offset[i]=-self.world_size[i]+size[i]
                elif self.offset[i]>0:
                    self.offset[i]=0
        else:
            self.offset=tuple(-self.world_size[i]//2+size[i]//2 for i in xrange(2))
        first=tuple(self.offset[i]%128 - 128 for i in xrange(2))
        for x in range(11):
            for y in range(6):
                if (self.state)=="dead":
                    image=self.background_special_image
                else:
                    image=self.backimage
                self.screen.blit(image,(first[0]+x*128,first[1]+y*128))
        
        for i in self.objects:
            if (self.state!="dead" or i not in self.enemies):
                i.draw(self.screen, self.offset)
        
        if self.state=="menu" or self.state=="score":
            self.screen.blit(self.menusurf,(0,0))
            if self.state=="score":
                textutil.drawtextcentered(self.screen,(size[0]//2,400),self.font,self.name)
        elif self.state=="game":
            self.screen.blit(self.font.render(str(self.score),1,(255,255,255)),(10,10))
            textutil.drawtextcentered(self.screen, (1180,10), self.font, "0:"+str(int(self.endtime-time.time())), 
                                      alignment=(2,0))
        
        if self.trans:
            self.screen.blit(self.transsurface,(-self.transamount,0),(0,0,size[0]//2,size[1]))
            self.screen.blit(self.transsurface,(size[0]//2+self.transamount,0),(size[0]//2,0,size[0]//2,size[1]))
            self.transamount+=15
            if self.transamount>size[0]//2:
                self.trans=False
        pygame.display.flip()
    def update(self):
        if not self.trans:
            if self.state=="game" and self.player_immune:
                self.player_immune-=1
            for i in self.objects:
                if (self.state!="dead" or i not in self.enemies):
                    i.update();
            if self.state!="dead":
                for en, bul in pygame.sprite.groupcollide(self.enemies, self.bullets, False, True, pygame.sprite.collide_circle).iteritems():
                    #self.enemies.remove(i)
                    en.explode()
                    en.kill()
                    self.addrandom()
            if self.player:
                for i in pygame.sprite.spritecollide(self.player, self.bullets, False, pygame.sprite.collide_circle):
                    
                    if i.timeout==0:
                        i.kill()
                    #else:
                        #print "ignored due to timeout"
                num=0
                
                if self.state=="game" and not self.player_immune:
                    for i in pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_circle):
                        i.kill()
                        self.addrandom()
                        self.startdie()
                        self.deaths+=1
                elif self.state=="dead":
                    for i in pygame.sprite.spritecollide(self.player, self.astroids, False, pygame.sprite.collide_circle):
                        self.state="game"
                        self.revive()
                    #if self.player.position==[1510,1510]:
                    #    num+=1
                    #    print i.rect.center, i.radius, self.player.position, self.player.radius, num
                for i in pygame.sprite.spritecollide(self.player, self.coins, True, pygame.sprite.collide_circle):
                    self.score+=1
            #print "collision"
        
            if self.state=="game":
                if time.time()>self.endtime:
                    self.starthighscore()
    def event(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
            elif self.state=="score":
                if event.type==pygame.MOUSEBUTTONDOWN or (event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN):
                    self.state="menu"
                    self.startmenu()
                elif event.type==pygame.KEYDOWN:
                    char=event.unicode
                    if char in string.printable:
                        self.name+=char
                    elif event.key==pygame.K_BACKSPACE:
                        self.name=self.name[:-1]
            elif self.state=="menu":
                if event.type==pygame.MOUSEBUTTONDOWN or (event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN):
                    self.state="game"
                    self.startgame()
            elif self.state=="game":
                if event.type==pygame.KEYDOWN and event.key==pygame.K_q:
                    self.endtime=time.time()+2
                else:
                    for i in self.objects:
                        i.event(event)
    def addrandom(self, cls=basic_shape.Shape, image=None, angle=45, speed=5, groups=None, friction=0, *args, **kwargs):
        position=[0,0]
        if image is None:
            image=self.planeimage
        side=random.choice((0,1))
        
        if random.choice((0,1)):
            position[side-1]=self.world_size[side-1]
        if groups==None:
            groups=self.enemies, self.objects
        if isinstance(speed,int) or isinstance(speed,float):
            s0=speed
            speed=(0,0)
        elif speed is None:
            speed=(0,0)
            s0=0
        else:
            s0=0
        position[side]=random.randint(0,self.world_size[side])
        if angle==None:
            angle=90*side
        obj=cls(position,image,angle,speed,friction,maxpos=self.world_size,*args, groups=groups, gui=self,**kwargs)
        obj.accelarate(s0)
        #self.enemies.add(obj)
        #self.objects.add(obj)
    
    
    def add_bullet(self,bullet):
        self.bullets.add(bullet)
        self.objects.add(bullet)
    def add_coin(self,coin):
        self.coins.add(coin)
        self.objects.add(coin)
    def revive(self):
        self.endtime=time.time()+self.timeleft
        self.player_immune=30
        for i in tuple(self.astroids)+tuple(self.special_coins):
            i.kill()
if __name__=="__main__":
    x=GUI()
    x.start()
    x.run()
        