import pygame
from abc import ABC, abstractmethod



class BoundedShape(ABC):
    @abstractmethod
    def isMouseIn(self, mouse_position):
        pass




class InteractiveElement:
    def __init__(self, function_to_call : function, boundedshape : BoundedShape):
        self.func = function_to_call
        self.bounder = boundedshape
        self.toggle = False

    def check(self, mouse_position : tuple):
        if self.bounder.isMouseIn(mouse_position):
