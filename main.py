'''
Created on 10 aug. 2015

@author: Maurits
'''
import pygame
import basic_shape
import random
import time


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
        
        pygame.init()
        self.screen=pygame.display.set_mode((1200,600))
        self.planeimage=pygame.image.load("plane.png").convert_alpha()
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
        pygame.key.set_repeat(100,100)
        self.clock=pygame.time.Clock()
        for i in range(50):
            self.addrandom()
        self.font=pygame.font.SysFont("Subway Ticker", 30, False, False)
        self.startmenu()
        
    def startgame(self):
        self.player=basic_shape.Player((self.world_size[0]/2,self.world_size[1]/2),self.player_image,45,(10,10),gui=self,maxpos=self.world_size,
                                       )
        self.state="game"
        self.objects.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.coins.empty()
        self.objects.add(self.player)
        for i in range(50):
            self.addrandom()
        self.score=0
        self.endtime=time.time()+60
    def startmenu(self):
        self.state="menu"
        size=self.screen.get_size()
        self.menusurf=pygame.Surface(size,pygame.SRCALPHA)
        self.menusurf.fill((0,255,0,200),(size[0]//2-200,0,400,600))
        self.menusurf.blit(self.font.render("Lazer of death",1,(255,255,255)),(size[0]//2-135,20))
        self.menusurf.blit(self.font.render("Press space to play!",1,(255,255,255)),(size[0]/2-180,500))
        if self.player:
            self.player.kill()
            self.player=None
    def startdie(self):
        self.state="dead"
        self.timeleft=-int(time.time()-self.endtime)
        
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.event()
            self.update()
            self.draw()
    def draw(self):
        #self.screen.fill((0,0,0))
        size=self.screen.get_size()
        if self.player:
            self.offset=[-self.player.position[i] + self.screen.get_size()[i]//2 for i in xrange(2)]
            for i in xrange(2):
                if self.offset[i]<-self.world_size[i]+size[i]:
                    self.offset[i]=-self.world_size[i]+size[i]
                elif self.offset[i]>0:
                    self.offset[i]=0
        else:
            self.offset=tuple(-self.world_size[i]+size[i]//2 for i in xrange(2))
        first=tuple(self.offset[i]%128 - 128 for i in xrange(2))
        for x in range(11):
            for y in range(6):
                if (self.state)=="dead":
                    image=self.background_special_image
                else:
                    image=self.backimage
                self.screen.blit(image,(first[0]+x*128,first[1]+y*128))
        
        for i in self.objects:
        
            i.draw(self.screen, self.offset)
        
        if self.state=="menu":
            self.screen.blit(self.menusurf,(0,0))
        elif self.state=="game":
            self.screen.blit(self.font.render(str(self.score),1,(255,255,255)),(10,10))
            self.screen.blit(self.font.render("0:"+str(-int(time.time()-self.endtime)),0,(255,255,255)),(950,10))
        
        pygame.display.flip()
    def update(self):
        
        for i in self.objects:
            i.update();
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
            for i in pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_circle):
                i.kill()
                if self.state=="game":
                    self.addrandom()
                    self.startdie()
                elif self.state=="dead":
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
                self.startmenu()
    def event(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
            elif self.state=="menu":
                if event.type==pygame.MOUSEBUTTONDOWN or (event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE):
                    self.state="game"
                    self.startgame()
            else:
                for i in self.objects:
                    i.event(event)
    def addrandom(self, cls=basic_shape.Accelerator, image=None, angle=45, **kwargs):
        position=[0,0]
        if image is None:
            image=self.planeimage
        side=random.choice((0,1))
        
        if random.choice((0,1)):
            position[side-1]=self.world_size[side-1]
        
        position[side]=random.randint(0,self.world_size[side])
        if angle==None:
            angle=90+90*side
        obj=cls(position,image,angle,maxpos=self.world_size,gui=self,**kwargs)
        self.enemies.add(obj)
        self.objects.add(obj)
    
    
    def add_bullet(self,bullet):
        self.bullets.add(bullet)
        self.objects.add(bullet)
    def add_coin(self,coin):
        self.coins.add(coin)
        self.objects.add(coin)
    def revive(self):
        self.endtime=time.time()+self.timeleft
if __name__=="__main__":
    x=GUI()
    x.start()
    x.run()
        