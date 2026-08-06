import dearpygui.dearpygui as dpg
from abc import abstractmethod, ABC

OUTPUT_FIELD = 1
INPUT_FIELD = 0

class NodeField:
    def __init__(self, label, type, parent, range=None):
        self.draw_id = None
        self.drawn = False
        self.connection = None
        self.type = INPUT_FIELD # OUT/IN:PUT_FIELD


    def update_draw(self):
        

class Node(ABC):
    
