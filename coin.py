'''
Created on 10 aug. 2015

@author: Maurits
'''
import basic_shape
import pygame
class Coin(basic_shape.Shape):
    def __init__(self,position,image,*args,**kwargs):
        if "timeout" in kwargs.keys():
            self.timeout=kwargs["timeout"]
            del kwargs["timeout"]
        else:
            self.timeout=240
        if "value" in kwargs.keys():
            self.value=kwargs["value"]
            del kwargs["value"]
        else:
            self.value=1
        if "radius" not in kwargs.keys():
            kwargs["radius"]=32
        if "calcscore" in kwargs.keys():
            calcscore=kwargs["calcscore"]
            del kwargs["calcscore"]
        else:
            calcscore=False
        basic_shape.Shape.__init__(self,position,image,*args,**kwargs)
        self.age=0
        if self.timeout>0 and calcscore:
            self.GUI.score+=self.value
    def update(self):
        basic_shape.Shape.update(self)
        self.age+=1
          
        if self.timeout>0 and self.age>self.timeout:
            self.kill()
            #print self.timeout
    def draw(self, *args, **kwargs):
        if self.timeout<0 or self.age<(self.timeout//2) or self.age%8<=4:
            basic_shape.Shape.draw(self, *args, **kwargs)
        #pygame.draw.circle(args[0],(255,255,255),tuple(int(self.position[i]+args[1][i]) for i in xrange(2)),self.radius,1)