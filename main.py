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
import os
import math

from collections import OrderedDict

class GUI(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    
        
    def start(self):
        
        os.environ["SDL_VIDEO_WINDOW_POS"]="50,50"
        
        self.score=0
        self.trans=False
        pygame.init()
        self.screen=pygame.display.set_mode((1200,600))
        
        
        self.font=pygame.font.Font("font/SUBWAY.ttf", 30)
        textutil.drawtextcentered(self.screen, (600,300), self.font, "Loading...", 0, (255,255,255))
        
        pygame.display.flip()
        
        
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.load("sound/Ouroboros.ogg")
        pygame.mixer.music.play(-1)
        
        self.endtime=int(time.time())
        
        
        
        self.planeimage=pygame.image.load("art/plane.png").convert_alpha()
        self.astroid_image=pygame.image.load("art/astroid.png").convert_alpha()
        self.redguy_image=pygame.image.load("art/redguy.png").convert_alpha()
        self.backimage=pygame.image.load("art/background.png").convert()
        self.bullet_img=pygame.image.load("art/bullet.png").convert_alpha()
        self.coin_img=pygame.image.load("art/coin.png").convert_alpha()
        self.life_img=pygame.image.load("art/life.png").convert_alpha()
        self.glowring_img=pygame.image.load("art/glowring.png").convert_alpha()
        self.player_image=pygame.image.load("art/player_plane.png").convert_alpha()
        self.instructions_image=pygame.image.load("art/instructions.png").convert_alpha()
        self.background_special_image=pygame.image.load("art/background_special.png").convert()
        self.turtle_image=pygame.image.load("art/turtle.png").convert_alpha()
        self.orange_square_image=pygame.image.load("art/orange_rect.png").convert_alpha()
        self.white_circle_image=pygame.image.load("art/neon_tube.png").convert_alpha()
        self.arrow_right_pic=pygame.image.load("art/Arrow_right.png").convert_alpha()
        
        self.coin_snd=pygame.mixer.Sound("sound/coin2.wav")
        self.coin_snd_chan=pygame.mixer.Channel(0)
        self.expl_snd=pygame.mixer.Sound("sound/explosion.wav")
        self.expl_snd_chan=tuple(pygame.mixer.Channel(i+1) for i in range(2))
        self.door_snd=pygame.mixer.Sound("sound/door2.wav")
        self.door_snd_chan=pygame.mixer.Channel(3)
        
        self.menu_index=0
        
        self.easy=True
        
        self.help_text=None
        self.help_text_ID=0
        
        self.running=True;
        self.world_size=(3000,3000)
        #self.player.gui=self
        pygame.display.set_caption("Lazer of Death")
        pygame.display.set_icon(self.player_image)
        
        self.menu_items=(("Help",self.startHelp),
                   ("Settings",self.startSettings),
                   ["Sound: [ON]", self.toggleSound],
                   ["Music: [ON]", self.toggleMusic]
                   )
        
        self.settings=OrderedDict((("Music Volume",1.0),
                       ("Sound Volume",1.0),
                       ("Precise FPS",False)))
        
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
        
        self.fpsfunc=self.clock.tick
        
        self.transsurface=pygame.Surface(self.screen.get_size())
        self.menu=False
        
        self.target_monster=None
        
        for i in range(50):
            self.addrandommonster()
        self.state="menu"
        
        self.startmenu(False)
        
        print "load time="+str(time.time()-(self.endtime))+"s"
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
        if self.easy:
            num=25
        else:
            num=50
        
        for i in range(num):
            self.addrandommonster()
        self.score=0
        self.endtime=time.time()+60
        self.deaths=0
        self.deathscore=0
        self.player_immune=False
        self.lives=3
        if self.easy:
            self.pen=50
        else:
            self.pen=100
        
    def startmenu(self, trans=True):
        print "FPS: ",self.clock.get_fps()
        if trans:
            self.transstart()
        self.state="menu"
        size=self.screen.get_size()
        
        
        self.offset=tuple(-self.world_size[i]//2+size[i]//2 for i in xrange(2))
        
        self.menusurf=pygame.Surface(size,pygame.SRCALPHA)
        self.menusurf.fill((0,255,0,200),(size[0]//2-200,0,400,600))
        textutil.drawtextcentered(self.menusurf, (size[0]//2,60), self.font, "Lazer of death")
        
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2, 470), self.font, "\"z\" to "+("select menu item" if self.menu else"change difficulty"))
        textutil.drawtextcentered(self.menusurf, (size[0]//2,size[1]-30), self.font, "Press Space to Play")
        
        if self.easy:
        
            self.highscores=textutil.loadhighscores()
        else:
            self.highscores=textutil.loadhighscores("highscores/hardhiscores.csv")
        pygame.draw.rect(self.menusurf,(255,255,255),(size[0]//2-180,100,360,335),2)
        for num, i in enumerate(sorted(self.highscores.keys(), reverse=True)):
            if num<10:
                textutil.drawtextcentered(self.menusurf, (size[0]//2-175,130+30*num), self.font, "{0: >2d}:{1}".format(num+1,self.highscores[i]),alignment=(0,1))
                textutil.drawtextcentered(self.menusurf, (size[0]//2+175,130+30*num), self.font, str(i),alignment=(2,1))
        
        
        if not self.menu:
            self.menusurf.fill((200,200,0,200),(size[0]//2+200,size[1]-110,180,50))
            textutil.drawtextcentered(self.menusurf,(size[0]//2+290,size[1]-85),self.font,"menu",True,(255,255,255),(1,1))
            self.menusurf.blit(self.arrow_right_pic,(size[0]//2+205,size[1]-105))
            self.menusurf.blit(self.arrow_right_pic, (size[0]//2+335,size[1]-105))
        else:
            self.menusurf.fill((200,200,0,200),(size[0]//2+200,50,220,500))
            for index, (name, func) in enumerate(self.menu_items):
                textutil.drawtextcentered(self.menusurf, (size[0]//2+310,75+70*index), self.font, name, True
                                          ,(255,255,255))
            
            pygame.draw.rect(self.menusurf, (255,255,255), (size[0]//2+205,55+70*self.menu_index,210,60), 2)
        
        if self.player:
            self.player.kill()
            self.player=None
            
    def startHelp(self):
        
        self.endtime=int(time.time())
        
        #print "Menu index: ",self.menu_index,"Gui page",self.help_text_ID,"Text len", \
        #    len(self.help_text) if self.help_text else "None"
        
        IDchange=False
        
        self.state="help"
        size=self.screen.get_size()
        self.menusurf=pygame.Surface(size,pygame.SRCALPHA)
        self.menusurf.fill((0,255,0,200),(size[0]//2-200,0,400,600))
        
        
            
        textutil.drawtextcentered(self.menusurf, (size[0]//2, 40), self.font,
                                  "Instructions")
        
        
        
        if self.menu_index<0:
            self.help_text_ID-=1
            self.menu_index=0
            IDchange=True
            if self.help_text_ID==0:
                self.target_monster=None
                
        if self.help_text_ID<0:
            self.help_text_ID=0
        
        
        if self.help_text_ID==0:
            
            if self.help_text==None or IDchange:
                self.menu_index=0
                f=open("data/Help.txt")
                self.help_text=f.read().splitlines()
                f.close()
            
            if self.menu_index-len(self.help_text)+15>0:
                self.help_text_ID+=1
                self.menu_index=0
                IDchange=True
            else:
                for i in range(16):
                    if (i+self.menu_index<len(self.help_text)):
                        textutil.drawtextcentered(self.menusurf, (size[0]//2,90+30*i), self.font,
                                              self.help_text[i+self.menu_index])
                    
            
                
        if self.help_text_ID>0:
            
            
            self.menusurf.fill((0,0,0,0), (size[0]//2-170,70,340,340))
            
            
            
            if self.menu_index>len(self.help_text)-4:
                if self.help_text_ID<5:
                    self.menu_index=0
                    self.help_text_ID+=1
                    IDchange=True
                else:
                    self.menu_index-=1
                    
            
                
            
            ID=self.help_text_ID-1
                
            if (self.target_monster==None or self.target_monster.ID!=ID or
                not self.target_monster.alive):
                #print ("Changing Monster, current is "+str(self.target_monster)+" ID: "+
                #    (str(self.target_monster.ID) if self.target_monster !=None else "N/A"))
                self.target_monster=None
                for i in self.enemies:
                    if i.ID==ID:
                        self.target_monster=i
                        break
                if self.target_monster==None:
                    self.target_monster=self.addrandommonster(ID)
                    
                self.offset=list(self.offset)
            
            if IDchange or self.help_text==None:
                f=open("Data/"+str(ID+1)+".txt")
                self.help_text=f.read().splitlines()
                f.close()
                
            for index in range(5):
                if index+self.menu_index<len(self.help_text):
                    text=self.help_text[index+self.menu_index]
                    textutil.drawtextcentered(self.menusurf, (size[0]//2,430+30*index), self.font, 
                                              text)
        
        pygame.draw.rect(self.menusurf,(255,255,255),(size[0]//2-180,60,360,size[1]-80),1)
        
    def startSettings(self):
        self.state="conf"
        size=self.screen.get_size()
        self.menusurf=pygame.Surface(size,pygame.SRCALPHA)
        self.menusurf.fill((0,255,0,200),(size[0]//2-200,0,400,600))    
        textutil.drawtextcentered(self.menusurf, (size[0]//2, 40), self.font,
                                  "Settings")
        
        pygame.draw.rect(self.menusurf,(255,255,255),(size[0]//2-180,60,360,size[1]-80),2)
        
        for index, (text, value) in enumerate( self.settings.items()):
            textutil.drawtextcentered(self.menusurf, (size[0]//2,90+100*index), self.font,
                                                      text)
            
            if self.menu_index==index:
                pygame.draw.rect(self.menusurf,(255,255,255),(size[0]//2-175,70+100*index,350,80),2)
            
            if isinstance(value, float):
                textutil.drawtextcentered(self.menusurf, (size[0]//2-170,120+100*index),
                                          self.font, "|"*int(value*16), alignment=(0,1))
            elif isinstance(value, bool):
                if value:
                    textutil.drawtextcentered(self.menusurf, (size[0]//2,120+100*index), self.font,
                                                      "Yes",color=(0,255,0))
                else:
                    textutil.drawtextcentered(self.menusurf, (size[0]//2,120+100*index), self.font,
                                                      "No",color=(255,0,0))
                    
    def applySettings(self):
        pygame.mixer.music.set_volume(self.settings["Music Volume"])
        self.toggleSound()
        self.toggleSound()
        
        if self.settings["Precise FPS"]:
            self.fpsfunc=self.clock.tick_busy_loop
        else:
            self.fpsfunc=self.clock.tick
        
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
        
        print self.score-(self.pen*self.deaths)+self.deathscore
        
        size=self.screen.get_size()
        self.offset=tuple(-self.world_size[i]//2+size[i]//2 for i in xrange(2))
        self.menusurf=pygame.Surface(size, pygame.SRCALPHA)
        self.menusurf.fill((0,255,0,200),(size[0]//2-200,0,400,600))
        textutil.drawtextcentered(self.menusurf, (size[0]//2,40), self.font, "Lazer of death")
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2-180,100), self.font, "Base score:",alignment=(0,1))
        textutil.drawtextcentered(self.menusurf, (size[0]//2+180,100), self.font, "{0:05d}".format(self.score), alignment=(2,1))
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2-180,160), self.font, "Death Penalty:",alignment=(0,1))
        textutil.drawtextcentered(self.menusurf, (size[0]//2+180,160), self.font, "{0:05d}".format(self.pen*self.deaths),color=(255,0,0),
                                   alignment=(2,1))
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2-180,220), self.font, "Death coins:",alignment=(0,1))
        textutil.drawtextcentered(self.menusurf, (size[0]//2+180,220), self.font, "{0:05d}".format(self.deathscore),color=(0,0,255),
                                   alignment=(2,1))
        
        print self.score-(self.pen*self.deaths)+self.deathscore
        textutil.drawtextcentered(self.menusurf, (size[0]//2-180,280), self.font, "Total score:",alignment=(0,1))
        textutil.drawtextcentered(self.menusurf, (size[0]//2+180,280), self.font, 
                                  "{0:05d}".format(self.score-self.pen*self.deaths+self.deathscore),
                                   alignment=(2,1))
        
        print self.score-(self.pen*self.deaths)+self.deathscore
        
        pygame.draw.line(self.menusurf,(255,255,255),(size[0]//2-185,250),(size[0]//2+185,250),2)
        pygame.draw.line(self.menusurf,(255,255,255),(size[0]//2+60,80),(size[0]//2+60,300),2)
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2,370), self.font, "enter your name: ")
        pygame.draw.rect(self.menusurf,(255,255,255),(size[0]//2-180,420,360,80),2)
        
        textutil.drawtextcentered(self.menusurf, (size[0]//2,size[1]-10),self.font, "press enter to continue",alignment=(1,2))
        """
        self.menusurf.blit(self.font.render("Lazer of death",1,(255,255,255)),(size[0]//2-135,20))
        self.menusurf.blit(self.font.render("Base score: "+str(self.score),1,(255,255,255)),(size[0]//2-135,80))
        self.menusurf.blit(self.font.render("Death penalty: -"+str(100*self.deaths),1,(255,0,0)),(size[0]//2-135,140))
        self.menusurf.blit(self.font.render("Total score: "+str(self.score-100*self.deaths),1,(255,255,255)),(size[0]//2-135,200))
        """
        print self.score-(self.pen*self.deaths)+self.deathscore
        self.finscore=self.score-(self.pen*self.deaths)+self.deathscore
        print self.finscore
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
            speed=7
            if self.easy:
                speed=4
            self.addrandom( image=self.astroid_image, groups=(self.astroids, self.objects), rotates=False, speed=random.random()*speed+5)
        for i in range(300):
            self.addrandom(coin.Coin, self.coin_img, None, random.random()*12, value=10, rotates=False,groups=(self.objects,self.special_coins,self.coins),friction=0,timeout=-1)
    
    def toggleSound(self):
        channels=(self.coin_snd_chan,self.door_snd_chan)+self.expl_snd_chan
        print channels
        
        if (self.menu_items[2][0].endswith("[OFF]")):
            for i in channels:
                i.set_volume(self.settings["Sound Volume"])
            self.menu_items[2][0]="Sound [ON]"
        else:
            for i in channels:
                print (i)
                i.set_volume(0)
            self.menu_items[2][0]="Sound [OFF]"
            
        self.startmenu(False)
            
    def toggleMusic(self):
        if (self.menu_items[3][0].endswith("[OFF]")):
            pygame.mixer.music.unpause()
            self.menu_items[3][0]="Music [ON]"
        else:
            pygame.mixer.music.pause()
            self.menu_items[3][0]="Music [OFF]"
            
        self.startmenu(False)
    def run(self):
        while self.running:
            self.fpsfunc(60)
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
        
        if self.state=="menu" or self.state=="score" or self.state=="help" or self.state=="conf":
            self.screen.blit(self.menusurf,(0,0))
            if self.state=="score":
                textutil.drawtextcentered(self.screen,(size[0]//2,460),self.font,self.name)
            elif self.state=="menu":
                if self.easy:
                    textutil.drawtextcentered(self.screen,(size[0]//2,520),self.font,"Easy",color=(0,0,255))
                else:
                    textutil.drawtextcentered(self.screen,(size[0]//2,520),self.font,"Hard",color=(255,0,0))
             
        elif self.state=="game" or self.state=="dead":
            tsurf=self.font.render(str(self.score),1,(255,255,255))#,(10,10))
            self.screen.blit(tsurf,(10,10))
            if self.deathscore!=0 or self.deaths!=0:
                num=self.deathscore-self.deaths*self.pen
                if num>=0:
                    self.screen.blit(self.font.render("+"+str(num),1,(0,0,255)),(10+tsurf.get_width(),10))
                else:
                    self.screen.blit(self.font.render(str(num),1,(255,0,0)),(10+tsurf.get_width(),10))
            
            if self.state=="dead":
                color=(100,100,100)
                ltime=self.timeleft
            else:
                color=(255,255,255)
                ltime=int(self.endtime-time.time())
                if self.lives!=3:
                    for i in range(self.lives):
                        self.screen.blit(self.life_img,(size[0]//2-65+36*i,10))
            
            textutil.drawtextcentered(self.screen, (1180,10), self.font, "0:{0:02d}".format(ltime), 
                                      alignment=(2,0),color=color)
            if self.score==0:
                self.screen.blit(self.instructions_image,(0,size[1]-64))
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
                for en, bul in pygame.sprite.groupcollide(self.enemies, self.bullets, False, False, pygame.sprite.collide_circle).iteritems():
                    #self.enemies.remove(i)
                    killen, killbul=en.hit()
                    
                    if killen and bul[0].shooter is not en:
                        en.explode(bul[0])
                        en.kill()
                        self.addrandommonster()
                        if hasattr(self,"offset"):
                            pos=tuple(en.position[i]+self.offset[i] for i in xrange(2))
                        
                            if (all(pos[i]>-32 and pos[i]<self.screen.get_size()[i]+32 for i in xrange(2))):
                                self.play_explo()
                                
                        if self.state=="help" and  en is self.target_monster:
                            self.target_monster=None
                            self.startHelp()
                            self.endtime=int(time.time())+3
                    if killbul:
                        for x in bul:
                            if x.shooter!=en:
                                x.kill()
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
                for i in pygame.sprite.spritecollide(self.player, self.coins, False, pygame.sprite.collide_circle):
                    if i.age>10:
                        self.playcoin()
                    
                        if self.state=="dead":
                            self.deathscore+=i.value
                        else:
                        
                            self.score+=i.value
                        i.kill()
                        
            #print "collision"
        
            if self.state=="game":
                if time.time()>self.endtime:
                    self.starthighscore()
                    
            elif self.state=="help":
                if self.target_monster!=None and (int(time.time()>self.endtime)):
                    size=self.screen.get_size()
                    distance=(self.target_monster.position[0]+self.offset[0]-size[0]//2,
                              self.target_monster.position[1]+self.offset[1]-240)
                    
                    dist=(distance[0]**2+distance[1]**2)
                    
                    if dist>(175):
                        if dist<1200:
                            speed=15
                        else:
                            speed=30
                        
                        angle=math.atan2(distance[0], distance[1])
                    
                        self.offset[0]+=-int(math.sin(angle)*speed)
                        self.offset[1]+=-int(math.cos(angle)*speed)
                    else:
                        self.offset[0]=-self.target_monster.position[0]+size[0]//2
                        self.offset[1]=-self.target_monster.position[1]+240
                
                #rect pos=(size[0]//2-170,70,340,340)
                #self.offset=tuple(-self.world_size[i]//2+size[i]//2 for i in xrange(2))
    def event(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
            elif self.state=="score":
                if (event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN):
                    self.state="menu"
                    error=False
                    if self.name.strip():
                        print "score: "+str(self.score)
                        self.highscores[self.finscore]=self.name
                        
                        if (not os.path.isdir("highscores")):
                            os.mkdir("highscores")
                        
                        if self.easy:
                            textutil.savehighscores(self.highscores)
                        else:
                            textutil.savehighscores(self.highscores,"highscores/hardhiscores.csv")
                        
                        
                    self.startmenu()
                elif event.type==pygame.KEYDOWN:
                    char=event.unicode
                    if char in string.ascii_letters or char in string.digits or char in "_-!@#^&*=+/?<>":
                        if len(self.name)<10:
                            self.name+=char
                    elif event.key==pygame.K_BACKSPACE:
                        self.name=self.name[:-1]
            elif self.state=="menu":
                if (event.type==pygame.KEYDOWN):
                    if event.key==pygame.K_SPACE or (not self.menu and event.key==pygame.K_RETURN):
                        self.state="game"
                        self.startgame()
                    elif event.key==pygame.K_z or (self.menu and event.key==pygame.K_RETURN):
                        if (not self.menu):
                            self.easy=not self.easy
                            self.startmenu(False)
                        else:
                            self.menu_items[self.menu_index][1]()
                    elif event.key==pygame.K_RIGHT:
                        self.menu=True
                        self.startmenu(False)
                    elif event.key==pygame.K_LEFT:
                        self.menu=False
                        self.startmenu(False)
                    elif event.key==pygame.K_UP:
                        self.menu=True
                        self.menu_index-=1
                        if self.menu_index<0:
                            self.menu_index=len(self.menu_items)-1
                        self.startmenu(False)
                    elif event.key==pygame.K_DOWN:
                        self.menu=True
                        self.menu_index+=1
                        if self.menu_index>=len(self.menu_items):
                            self.menu_index=0
                        self.startmenu(False)
            elif self.state=="help" or self.state=="conf":
                
                func=self.startHelp if self.state=="help" else self.startSettings
                
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_DOWN:
                        self.menu_index+=1
                        func()
                    elif event.key==pygame.K_UP:
                        self.menu_index-=1
                        func()
                        
                    elif (event.key==pygame.K_ESCAPE or event.key==pygame.K_SPACE or
                        event.key==pygame.K_RETURN):
                        self.startmenu(False)
                        self.help_text=None
                        self.menu_index=0
                        self.help_text_ID=0
                        
                        if self.state=="conf":
                            self.applySettings()
                        
                    elif event.key==pygame.K_x:
                        if self.target_monster:
                            b=basic_shape.Bullet(self.target_monster.position, self.orange_square_image,
                                                               radius=256)
                            b.timeout=0
                            b.shooter=self.addrandommonster(2)
                            b.calcscore=False
                            self.add_bullet(b)
                            
                    elif self.state=="conf":
                        if event.key==pygame.K_z:
                            sdict=tuple(self.settings.items())
                            if isinstance(sdict[self.menu_index][1],bool):
                                self.settings[sdict[self.menu_index][0]]=not sdict[self.menu_index][1]
                                self.applySettings()
                                self.startSettings()
                        elif event.key==pygame.K_LEFT:
                            sdict=tuple(self.settings.items())
                            if isinstance(sdict[self.menu_index][1],float):
                                self.settings[sdict[self.menu_index][0]]=max(0.0,
                                                                sdict[self.menu_index][1]-0.064)
                                self.applySettings()
                                self.startSettings()
                        elif event.key==pygame.K_RIGHT:
                            sdict=tuple(self.settings.items())
                            if isinstance(sdict[self.menu_index][1],float):
                                self.settings[sdict[self.menu_index][0]]=min(1.0,
                                                                sdict[self.menu_index][1]+0.064)
                                self.applySettings()
                                self.startSettings()   
            elif self.state=="game":
                if event.type==pygame.KEYDOWN and event.key==pygame.K_q:
                    self.endtime=time.time()+2
                else:
                    for i in self.objects:
                        i.event(event)
                        
    enemy_types=("normal",14),("wave",4),("shooter",2),("turtle",3),("orange_rect",1)
                        
    def addrandommonster(self, ID=-1):
        if ID==-1:
            c=random.choice(sum(((i[0],)*i[1] for i in self.enemy_types), ())  )
        else:
            c=""
        #c="orange_rect"
        if ID==0 or c=="normal":
            return self.addrandom()
        elif ID==1 or c=="wave":
            return self.addrandom(cls=basic_shape.RotateCellerator,image=self.glowring_img,speed=0,accel=1.5,friction=0.1,rotates=False,
                           numcoins=14, ID=1)
        elif ID==2 or c=="shooter":
            return self.addrandom(cls=basic_shape.Shooter,image=self.redguy_image,speed=0,accel=1.25,friction=0.1,rotates=True,radius=17,
                           numcoins=7, ID=2)
        elif ID==3 or c=="turtle":
            return self.addrandom(cls=basic_shape.Turtle,image=self.turtle_image,radius=96,speed=2,
                           numcoins=28, ID=3)
        elif ID==4 or c=="orange_rect":
            return self.addrandom(cls=basic_shape.Orange_Rect, image=self.orange_square_image, speed=2, radius=48, otherimage=self.white_circle_image,
                           numcoins=32, rotates=False, ID=4)
        else:
            raise ValueError("c="+str(c)+", ID="+str(ID))
    def addrandom(self, cls=basic_shape.Shape, image=None, angle=NotImplemented, speed=5, groups=None,
                  friction=0, ID=0, *args, **kwargs):
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
        obj=cls(position=position,image=image,angle=angle,speed=speed,friction=friction,
                maxpos=self.world_size,*args, groups=groups, gui=self, ID=ID, **kwargs)
        obj.accelarate(s0)
        #self.enemies.add(obj)
        #self.objects.add(obj)
        return obj
    
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
    pygame.quit()
        