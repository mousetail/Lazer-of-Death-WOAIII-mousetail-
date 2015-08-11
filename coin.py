'''
Created on 10 aug. 2015

@author: Maurits
'''
import basic_shape

class Coin(basic_shape.Shape):
    def __init__(self,position,image,value,*args,**kwargs):
        basic_shape.Shape.__init__(self,position,image,*args,**kwargs)
        self.value=value