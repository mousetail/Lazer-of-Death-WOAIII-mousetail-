'''
Created on 10 aug. 2015

@author: Maurits
'''
import pygame
import basic_shape
import random


class GUI(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.objects=pygame.sprite.Group()
    def start(self):
        self.score=0
        
        pygame.init()
        self.screen=pygame.display.set_mode((1200,600))
        self.planeimage=pygame.image.load("plane.png").convert_alpha()
        self.backimage=pygame.image.load("background.png").convert()
        self.bullet_img=pygame.image.load("bullet.png").convert_alpha()
        self.coin_img=pygame.image.load("coin.png").convert_alpha()
        self.running=True;
        self.world_size=(3000,3000)
        self.player=basic_shape.Player((self.world_size[0]/2,self.world_size[1]/2),self.planeimage,45,(10,10),gui=self,maxpos=self.world_size,
                                       )
        #self.player.gui=self
        
        self.enemies=pygame.sprite.Group()
        self.bullets=pygame.sprite.Group()
        self.coins=pygame.sprite.Group()
        
        self.objects.add(self.player)
        pygame.key.set_repeat(100,100)
        self.clock=pygame.time.Clock()
        for i in range(50):
            self.addrandom()
        self.font=pygame.font.SysFont("Subway Ticker", 30, False, False)
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.event()
            self.update()
            self.draw()
    def draw(self):
        #self.screen.fill((0,0,0))
        self.offset=tuple(-self.player.position[i] + self.screen.get_size()[i]//2 for i in xrange(2))
        
        first=tuple(self.offset[i]%128 - 128 for i in xrange(2))
        for x in range(11):
            for y in range(6):
                self.screen.blit(self.backimage,(first[0]+x*128,first[1]+y*128))
        
        for i in self.objects:
            i.draw(self.screen, self.offset)
        
        self.screen.blit(self.font.render(str(self.score),1,(255,255,255)),(10,10))
        
        pygame.display.flip()
    def update(self):
        for i in self.objects:
            i.update();
        for en, bul in pygame.sprite.groupcollide(self.enemies, self.bullets, False, True, pygame.sprite.collide_circle).iteritems():
            #self.enemies.remove(i)
            en.explode()
            en.kill()
            self.addrandom()
        for i in pygame.sprite.spritecollide(self.player, self.bullets, False, pygame.sprite.collide_circle):
            
            if i.timeout==0:
                i.kill()
            #else:
                #print "ignored due to timeout"
        for i in pygame.sprite.spritecollide(self.player, self.enemies, True, pygame.sprite.collide_circle):
            self.objects.remove(i)
            self.addrandom()
        for i in pygame.sprite.spritecollide(self.player, self.coins, True, pygame.sprite.collide_circle):
            self.score+=1
            #print "collision"
    def event(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
            else:
                for i in self.objects:
                    i.event(event)
    def addrandom(self):
        position=[0,0]
        side=random.choice((0,1))
        if random.choice((0,1)):
            position[side-1]=self.world_size[side-1]
        position[side]=random.randint(0,self.world_size[side])
        obj=basic_shape.Accelerator(position,self.planeimage,45,maxpos=self.world_size,gui=self)
        self.enemies.add(obj)
        self.objects.add(obj)
    def add_bullet(self,bullet):
        self.bullets.add(bullet)
        self.objects.add(bullet)
    def add_coin(self,coin):
        self.coins.add(coin)
        self.objects.add(coin)
if __name__=="__main__":
    x=GUI()
    x.start()
    x.run()
        