'''
Created on 10 aug. 2015

@author: Maurits
'''
import basic_shape

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
        
        basic_shape.Shape.__init__(self,position,image,*args,**kwargs)
        self.age=0
        
        self.GUI.score+=self.value
    def update(self):
        basic_shape.Shape.update(self)
        self.age+=1
          
        if self.age>self.timeout:
            self.kill()
    def draw(self, *args, **kwargs):
        if self.age<(self.timeout//2) or self.age%8<=4:
            basic_shape.Shape.draw(self, *args, **kwargs)