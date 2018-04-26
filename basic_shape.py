'''
Created on 10 aug. 2015

@author: Maurits
'''
import math, pygame, random

WALLBEHAVIOR_DIE = 3
WALLBEHAVIOR_BOUNCE = 5
WALLBEHAVIOR_NONE = 9


class Shape(pygame.sprite.Sprite):
    '''
    Any shape
    '''
    numcoins = 7

    def __init__(self, position, image, angle=0, speed=(0, 0), friction=0.1, maxspeed=20, maxpos=(1000, 500),
                 radius=32, groups=(), numcoins=None,
                 gui=None, rotates=True, wallbehavior=WALLBEHAVIOR_BOUNCE,
                 ID=0):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self, *groups)

        self.position = list(position)
        self.image = image
        self.angle = angle
        self.speed = list(speed)
        self.rotates = rotates
        self.friction = 1 - friction
        self.maxspeed = maxspeed
        self.maxspeed2 = maxspeed ** 2
        self.radius = radius
        self.rotate(0)
        self.maxpos = maxpos
        self.rect = self.image.get_rect()
        self.GUI = gui
        self.wallbehavior = wallbehavior
        self.firerate = 20
        self.num = 0
        self.ID = ID
        if numcoins is not None:
            self.numcoins = numcoins

    def update(self):
        for i in range(2):

            self.position[i] = self.position[i] + self.speed[i]
            self.speed[i] *= self.friction
            if self.position[i] > self.maxpos[i]:
                if self.wallbehavior == WALLBEHAVIOR_DIE:
                    self.kill()
                elif self.wallbehavior == WALLBEHAVIOR_BOUNCE:
                    self.position[i] = self.maxpos[i]
                    self.speed[i] = -self.speed[i]
                    if self.rotates:
                        self.angle = math.degrees(math.atan2(-self.speed[0], -self.speed[1]))
                        self.rotate(0)
                elif self.wallbehavior == WALLBEHAVIOR_NONE:
                    pass
                else:
                    raise ValueError(str(self.wallbehavior) + " is not a valid value")
            elif self.position[i] < 0:
                if self.wallbehavior == WALLBEHAVIOR_DIE:
                    self.kill()
                elif self.wallbehavior == WALLBEHAVIOR_BOUNCE:
                    self.position[i] = 0
                    self.speed[i] = -self.speed[i]
                    if self.rotates:
                        self.angle = math.degrees(math.atan2(-self.speed[0], -self.speed[1]))
                        self.rotate(0)
                elif self.wallbehavior == WALLBEHAVIOR_NONE:
                    pass
                else:
                    raise ValueError(str(self.wallbehavior) + " is not a valid value")
        self.rect.center = self.position

    def rotate(self, angle):

        self.angle += angle
        if self.rotates:
            self.rotimage = pygame.transform.rotate(self.image, self.angle)

    def draw(self, surface, offset):
        if self.rotates:
            img = self.rotimage
            size = self.rotimage.get_size()
        else:
            img = self.image
            size = self.image.get_size()

        if sum(self.position[i] + offset[i] + size[i] > 0 for i in range(2)):
            surface.blit(img, tuple(self.position[i] - size[i] / 2 + offset[i] for i in range(2)))

    def event(self, event):
        pass

    def accelarate(self, ammount):
        x = -math.sin(math.radians(self.angle)) * ammount
        y = -math.cos(math.radians(self.angle)) * ammount
        self.speed[0] += x
        self.speed[1] += y

    def fire(self, calcscore=True):
        if self.num == 0:
            bul = Bullet(self.position, self.GUI.bullet_img, angle=self.angle, friction=0, radius=4,
                         maxpos=self.maxpos, rotates=False)
            bul.accelarate(12)
            bul.calcscore = calcscore
            bul.shooter = self
            self.GUI.add_bullet(bul)
        self.num -= 1
        if self.num < 0:
            self.num = self.firerate

    def explode(self, bullet):
        print ("exploded: "+str(self)+" with "+str(bullet))
        pass

    def hit(self):
        """Return killself, killbullet"""
        return True, True


class Bullet(Shape):
    def __init__(self, *args, **kwargs):
        Shape.__init__(self, *args, **kwargs)
        # print "made bullet"
        self.wallbehavior = WALLBEHAVIOR_DIE
        self.timeout = 7

    def update(self):
        Shape.update(self)
        if self.timeout:
            self.timeout -= 1





import coin
