import dearpygui.dearpygui as dpg
from abc import abstractmethod, ABC

OUTPUT_FIELD = 1
INPUT_FIELD = 0
CURR_NODES = {}

class NodeField:
    def __init__(self, label, parent, vrange=None):
        self.drawn = False
        self.connection = None # not updated if its an output field
        self.label = label
        self.range = vrange
        self.parent = parent


    def update_draw(self):
        
            if not self.drawn:
                #if self.connection is not None:
                dpg.add_text(self.label, 
                            tag=self.parent.label + self.label + "CONNECTED")
                #elif self.range is None:
                dpg.add_float_value(label=self.parent.label + self.label, 
                                    tag=self.parent.label + self.label + "FLOATVAL")
                #else:
                dpg.add_slider_float(label=self.parent.label + self.label, 
                                    min_value=self.range[0], 
                                    max_value=self.range[1], 
                                    tag=self.parent.label + self.label + "FLOATRAN")
                self.drawn = True
                self.update_draw()
            elif self.drawn:
                dpg.hide_item(self.parent.label + self.label + "CONNECTED")
                dpg.hide_item(self.parent.label + self.label + "FLOATVAL")
                dpg.hide_item(self.parent.label + self.label + "FLOATRAN")

                if self.connection is not None:
                    dpg.show_item(self.parent.label + self.label + "CONNECTED")
                elif not self.range:
                    dpg.show_item(self.parent.label + self.label + "FLOATVAL")
                else:
                    dpg.show_item(self.parent.label + self.label + "FLOATRAN")

class Node(ABC):

    node_types_and_counts = {}

    def __init__(self):
        self.node_title = None
        self.label = None 
        self.nodes = {INPUT_FIELD: [], OUTPUT_FIELD: []}
        self.drawn = False

    def register(self, class_name, unique=False):
        if not unique:
            Node.node_types_and_counts[class_name] = Node.node_types_and_counts.get(class_name, 0) + 1
            return class_name + str(Node.node_types_and_counts[class_name] - 1)
        else:
            if class_name in Node.node_types_and_counts:
                return None
            else:
                Node.node_types_and_counts[class_name] = "UNIQUE"
                return class_name


    def draw(self):
        if not self.drawn:
            with dpg.node(label=self.label, tag=self.label):
                for node in self.nodes["INPUT_FIELD"]:
                    with dpg.node_attribute(label=node.label, tag=self.label + node.label):
                        node.update_draw()
                for node in self.nodes["OUTPUT_FIELD"]:
                    with dpg.node_attribute(label=node.label, tag=self.label + node.label, type=dpg.mvNode_Attr_Output):
                        node.update_draw()
        else:
            for node in self.nodes["INPUT_FIELD"] + self.nodes["OUTPUT_FIELD"]:
                node.update_draw()

class ACCNODE(Node):
    def __init__(self):
        super().__init__()
        self.node_title = "Accelerometer"
        self.nodes["OUTPUT_FIELD"] = [
            NodeField("Acceleration X", self),
            NodeField("Acceleration Y", self),
            NodeField("Acceleration Z", self)
        ]

        self.label = self.register(self.node_title)

class GYRONODE(Node):
    def __init__(self):
        super().__init__()
        self.node_title = "Gyroscope"
        self.nodes["OUTPUT_FIELD"] = [
            NodeField("Gyroscope X", self),
            NodeField("Gyroscope Y", self),
            NodeField("Gyroscope Z", self)
        ]

        self.label = self.register(self.node_title)

class SERVONODE(Node):
    def __init__(self):
        super().__init__()
        self.node_title = "Airplane Servos"
        self.nodes["INPUT_FIELD"] = [
            NodeField("Servo Yaw"),
            NodeField("Servo Row"),
            NodeField("Servo Pitch")
        ]
