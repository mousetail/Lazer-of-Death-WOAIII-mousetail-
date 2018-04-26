import random, math
import pygame
import basic_shape
import coin


class Enemy(basic_shape.Shape):
    def explode(self, bullet):
        coins = []
        for i in range(self.numcoins):
            angle = random.randint(0, 360)
            coins.append(
                coin.Coin(self.position, self.GUI.coin_img, angle, radius=128, gui=self.GUI, value=random.randint(1, 3),
                          maxpos=self.maxpos, calcscore=bullet.calcscore, rotates=False))
        for i in coins:
            i.accelarate(random.randint(2, self.numcoins // 2))
            self.GUI.add_coin(i)


class Orange_Rect(Enemy):
    def __init__(self, otherimage, *args, **kwargs):
        basic_shape.Shape.__init__(self, *args, **kwargs)
        self.subitems = []
        self.rotAngle = 0
        for i in range(4):
            self.subitems.append(Rect_orbit(position=self.position[:], gui=self.GUI, speed=[0, 0],
                                            radius=16, image=otherimage, groups=self.groups(),
                                            rotates=False, wallbehavior=basic_shape.WALLBEHAVIOR_NONE,
                                            friction=0, maxpos=self.maxpos, ID=-1))

    def update(self):
        basic_shape.Shape.update(self)
        self.rotAngle += 0.1
        sin = math.sin(self.rotAngle) * 128
        cos = math.cos(self.rotAngle) * 128
        if self.subitems[0] != None:
            self.subitems[0].position[0] = self.position[0] + sin
            self.subitems[0].position[1] = self.position[1] + cos
        if self.subitems[1] != None:
            self.subitems[1].position[0] = self.position[0] + cos
            self.subitems[1].position[1] = self.position[1] - sin
        if self.subitems[2] != None:
            self.subitems[2].position[0] = self.position[0] - sin
            self.subitems[2].position[1] = self.position[1] - cos
        if self.subitems[3] != None:
            self.subitems[3].position[0] = self.position[0] - cos
            self.subitems[3].position[1] = self.position[1] + sin

    def hit(self):
        l = list(range(4))
        random.shuffle(l)
        item = None
        index = -1
        for i in l:
            if self.subitems[i] is not None:
                item = self.subitems[i]
                index = i
                break
        if item is None:
            return True, True
        self.subitems[index] = None
        item.speed = [math.cos(self.rotAngle + (index * math.pi / 2)) * 12,
                      -math.sin(self.rotAngle + (index * math.pi / 2)) * 12]
        item.wallbehavior = basic_shape.WALLBEHAVIOR_DIE
        return False, True


class Rect_orbit(Enemy):
    def hit(self):
        return False, True

    def updateF(self):
        pass


class Player(Enemy):
    def update(self):
        basic_shape.Shape.update(self)
        keys = pygame.key.get_pressed()
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
        # if event.type==pygame.KEYDOWN:
        #    if event.key==pygame.K_z:

    def draw(self, *args, **kwargs):
        if self.GUI.player_immune % 16 < 8:
            basic_shape.Shape.draw(self, *args, **kwargs)


class Accelerator(Enemy):
    numcoins = 15

    def __init__(self, *args, **kwargs):
        if "accel" in list(kwargs.keys()):
            self.acceleration = kwargs["accel"]
            del kwargs["accel"]
        else:
            self.acceleration = 1

        basic_shape.Shape.__init__(self, *args, **kwargs)

    def update(self):
        basic_shape.Shape.update(self)
        self.accelarate(self.acceleration)


class RotateCellerator(Accelerator):
    numcoins = 20

    def __init__(self, *args, **kwargs):
        Accelerator.__init__(self, *args, **kwargs)
        self.direction = 1

    def update(self):
        Accelerator.update(self)
        self.rotate(self.direction)
        if random.randint(0, 12) == 0:
            self.direction += random.randint(-2, 2)
            if self.direction > 10:
                self.direction = 10
            elif self.direction < -10:
                self.direction = -10


class Shooter(RotateCellerator):
    numcoins = 25

    def update(self):
        RotateCellerator.update(self)
        if random.randint(0, 2) == 1:
            self.fire(False)


class Turtle(Enemy):
    numcoins = 30

    def __init__(self, *args, **kwargs):
        basic_shape.Shape.__init__(self, *args, **kwargs)
        self.lives = 9
        self.maxlives = 9

    def draw(self, surface, offset):
        basic_shape.Shape.draw(self, surface, offset)
        surface.fill((0, 255, 0),
                     (self.position[0] + offset[0] - 90, self.position[1] - 100 + offset[1], 10 * self.lives, 10))

    def hit(self):
        self.lives -= 1
        if self.lives <= 0:
            return True, True
        else:
            return False, True
