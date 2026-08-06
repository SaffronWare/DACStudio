import dearpygui.dearpygui as dpg
from abc import abstractmethod, ABC

OUTPUT_FIELD = 1
INPUT_FIELD = 0

class NodeField:
    def __init__(self, label, type, parent, vrange=None):
        self.drawn = False
        self.connection = None # not updated if its an output field
        self.label = label
        self.range = vrange
        self.parent = parent

    def update_draw(self):
        if not self.drawn:
            if self.connection is None:
                dpg.add_text(self.label, 
                             tag=self.parent.label + self.label + "CONNECTED")
            elif self.range is None:
                dpg.add_float_value(label=self.parent.label + self.label, 
                                    tag=self.parent.label + self.label + "FLOATVAL")
            else:
                dpg.add_slider_float(label=self.parent.label + self.label, 
                                     min_value=self.range[0], 
                                     max_value=self.range[1], 
                                     tag=self.parent.label + self.label + "FLOATRAN")

class Node(ABC):
    def __init__(self):
        self.label = None 
        self.nodes = {INPUT_FIELD: [], OUTPUT_FIELD: []}
