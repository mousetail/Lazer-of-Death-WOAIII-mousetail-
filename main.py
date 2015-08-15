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
        self.splash=pygame.image.load("splash.png").convert()
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.load("Ouroboros.ogg")
        pygame.mixer.music.play(-1)
        self.screen.blit(self.splash,(0,0))
        pygame.display.flip()
        self.planeimage=pygame.image.load("plane.png").convert_alpha()
        self.astroid_image=pygame.image.load("astroid.png").convert_alpha()
        self.redguy_image=pygame.image.load("redguy.png").convert_alpha()
        self.backimage=pygame.image.load("background.png").convert()
        self.bullet_img=pygame.image.load("bullet.png").convert_alpha()
        self.coin_img=pygame.image.load("coin.png").convert_alpha()
        self.life_img=pygame.image.load("life.png").convert_alpha()
        self.glowring_img=pygame.image.load("glowring.png").convert_alpha()
        self.player_image=pygame.image.load("player_plane.png").convert_alpha()
        self.instructions_image=pygame.image.load("instructions.png").convert_alpha()
        self.background_special_image=pygame.image.load("background_special.png").convert()
        self.turtle_image=pygame.image.load("turtle.png").convert_alpha()
        
        self.coin_snd=pygame.mixer.Sound("coin2.wav")
        self.coin_snd_chan=pygame.mixer.Channel(0)
        self.expl_snd=pygame.mixer.Sound("explosion.wav")
        self.expl_snd_chan=tuple(pygame.mixer.Channel(i+1) for i in range(2))
        self.door_snd=pygame.mixer.Sound("door2.wav")
        self.door_snd_chan=pygame.mixer.Channel(3)
        
        
        self.running=True;
        self.world_size=(3000,3000)
        #self.player.gui=self
        pygame.display.set_caption("Lazer of Death")
        pygame.display.set_icon(self.player_image)
        
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
            self.addrandommonster()
        self.font=pygame.font.Font("SUBWAY.ttf", 30)
        self.state="splash"
        self.endtime=int(time.time()+3)
    def playcoin(self):
        #pygame.mixer.get_busy()
        if not self.coin_snd_chan.get_busy():
            self.coin_snd_chan.play(self.coin_snd)
    def playdoor(self):
        if not self.door_snd_chan.get_busy():
            self.door_snd_chan.play(self.door_snd)
    def play_explo(self):
        for i in self.expl_snd_chan:
            if not i.get_busy():
                i.play(self.expl_snd)
                return
    def startgame(self):
        print "FPS: ",self.clock.get_fps()
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
            self.addrandommonster()
        self.score=0
        self.endtime=time.time()+60
        self.deaths=0
        self.deathscore=0
        self.player_immune=False
        self.lives=3
        
    def startmenu(self):
        print "FPS: ",self.clock.get_fps()
        self.transstart()
        self.state="menu"
        size=self.screen.get_size()
        self.menusurf=pygame.Surface(size,pygame.SRCALPHA)
        self.menusurf.fill((0,255,0,200),(size[0]//2-200,0,400,600))
        textutil.drawtextcentered(self.menusurf, (size[0]//2,60), self.font, "Lazer of death")
        textutil.drawtextcentered(self.menusurf, (size[0]//2,550), self.font, "Press enter to play")
        
        self.highscores=textutil.loadhighscores()
        pygame.draw.rect(self.menusurf,(255,255,255),(size[0]//2-180,100,360,420),2)
        for num, i in enumerate(sorted(self.highscores.keys(), reverse=True)):
            if num<13:
                textutil.drawtextcentered(self.menusurf, (size[0]//2-175,130+30*num), self.font, str(num+1)+": "+self.highscores[i],alignment=(0,1))
                textutil.drawtextcentered(self.menusurf, (size[0]//2+175,130+30*num), self.font, str(i),alignment=(2,1))
        
        if self.player:
            self.player.kill()
            self.player=None
    def starthighscore(self):
        self.transstart()
        if self.player:
            self.player.kill()
            self.player=None
        self.state="score"
        
        self.name=""
        
        print "deaths:          "+str(self.deaths)
        print "score while dead "+str(self.deathscore)
        if self.deaths>0:
            print "score per death: "+str(self.deathscore/self.deaths)
        
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
        self.playdoor()
    def startdie(self):
        print "FPS: ",self.clock.get_fps()
        self.state="dead"
        self.lives=3
        self.transstart()
        self.timeleft=-int(time.time()-self.endtime)
        self.player.position=[self.world_size[i]//2 for i in xrange(2)]
        
        for i in tuple(self.coins):
            i.kill()
        
        for i in range(75):
            self.addrandom( image=self.astroid_image, groups=(self.astroids, self.objects), rotates=False, speed=random.random()*7+5)
        for i in range(300):
            self.addrandom(coin.Coin, self.coin_img, None, random.random()*12, value=10, rotates=False,groups=(self.objects,self.special_coins,self.coins),friction=0,timeout=-1)
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.event()
            self.update()
            self.draw()
    def draw(self):
        size=self.screen.get_size()
        if self.state!="splash":
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
            elif self.state=="game" or self.state=="dead":
                self.screen.blit(self.font.render(str(self.score),1,(255,255,255)),(10,10))
                if self.state=="dead":
                    color=(100,100,100)
                    ltime=self.timeleft
                else:
                    color=(255,255,255)
                    ltime=int(self.endtime-time.time())
                    if self.lives!=3:
                        for i in range(self.lives):
                            self.screen.blit(self.life_img,(size[0]//2-65+36*i,10))
                
                textutil.drawtextcentered(self.screen, (1180,10), self.font, "0:"+str(ltime), 
                                          alignment=(2,0),color=color)
                if self.score==0:
                    self.screen.blit(self.instructions_image,(0,size[1]-64))
            
        else:
            self.screen.blit(self.splash,(0,0))
        if self.trans:
            self.screen.blit(self.transsurface,(-self.transamount,0),(0,0,size[0]//2,size[1]))
            self.screen.blit(self.transsurface,(size[0]//2+self.transamount,0),(size[0]//2,0,size[0]//2,size[1]))
            self.transamount+=15
            if self.transamount>size[0]//2:
                self.trans=False
        pygame.display.flip()
    def update(self):
        if not self.trans or self.state=="menu" or self.state=="score":
            if self.state=="splash" and time.time()>self.endtime:
                self.startmenu()
                del self.splash
            if self.state=="game" and self.player_immune:
                self.player_immune-=1
            for i in self.objects:
                if (self.state!="dead" or i not in self.enemies):
                    i.update();
            if self.state!="dead":
                for en, bul in pygame.sprite.groupcollide(self.enemies, self.bullets, False, False, pygame.sprite.collide_circle).iteritems():
                    #self.enemies.remove(i)
                    l=True
                    if isinstance(en, basic_shape.Turtle):
                        en.lives-=1
                        if en.lives>0:
                            l=False
                    
                    if l and bul[0].shooter is not en:
                        en.explode(bul[0])
                        en.kill()
                        self.addrandommonster()
                        bul[0].kill()
                        if hasattr(self,"offset"):
                            pos=tuple(en.position[i]+self.offset[i] for i in xrange(2))
                        
                            if (all(pos[i]>-32 and pos[i]<self.screen.get_size()[i]+32 for i in xrange(2))):
                                self.play_explo()
            if self.player:
                if self.state=="game" and not self.player_immune:
                    for i in pygame.sprite.spritecollide(self.player, self.bullets, False, pygame.sprite.collide_circle):
                        
                        if i.shooter is not self.player:
                            i.kill()
                            self.lives-=1
                            if self.lives<=0:
                                self.lives=3
                                self.startdie()
                                self.deaths+=1
                    #else:
                        #print "ignored due to timeout"
                #num=0
                
                    for i in pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_circle):
                        i.kill()
                        self.addrandommonster()
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
                    self.score+=i.value
                    
                    self.playcoin()
                    
                    if self.state=="dead":
                        self.deathscore+=i.value
            #print "collision"
        
            if self.state=="game":
                if time.time()>self.endtime:
                    self.starthighscore()
    def event(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
            elif self.state=="splash":
                if event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN:
                    self.startmenu()
                    del self.splash
            elif self.state=="score":
                if event.type==pygame.MOUSEBUTTONDOWN or (event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN):
                    self.state="menu"
                    error=False
                    if self.name.strip():
                        self.highscores[self.score]=self.name
                        try:
                            textutil.savehighscores(self.highscores)
                        except TypeError as ex:
                            print self.name, self.score
                            print self.highscores
                            print "ERROR ERROR ERRRRRRRRRRRRROR"
                            print ex
                            error=True
                        
                        if error:
                            self.menusurf.fill((255,0,0),(10,10,100,60))
                            textutil.drawtextcentered(self.menusurf, (60,40), self.font, "ERROR")
                        
                    self.startmenu()
                elif event.type==pygame.KEYDOWN:
                    char=event.unicode
                    if char in string.ascii_letters or char in string.digits:
                        if len(self.name)<10:
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
    def addrandommonster(self):
        c=random.choice(("normal",)*14+("wave",)*4+("shooter",)*1+("turtle",)*5)
        if c=="normal":
            self.addrandom()
        elif c=="wave":
            self.addrandom(cls=basic_shape.RotateCellerator,image=self.glowring_img,speed=0,accel=1.5,friction=0.1,rotates=False)
        elif c=="shooter":
            self.addrandom(cls=basic_shape.Shooter,image=self.redguy_image,speed=0,accel=1.25,friction=0.1,rotates=True,radius=17)
        elif c=="turtle":
            self.addrandom(cls=basic_shape.Turtle,image=self.turtle_image,radius=96,speed=2)
    def addrandom(self, cls=basic_shape.Shape, image=None, angle=NotImplemented, speed=5, groups=None, friction=0, *args, **kwargs):
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
        if angle is None:
            angle=90*side
        elif angle is NotImplemented:
            angle=random.randint(0,360)
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
        