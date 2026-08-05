import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod

NODE_TYPES = {
    "OUTPUT": 1,
    "INPUT": 0,
    "INTER": 0.5,
}


REGISTERED_NODES = {}

def RegisterNode(label, cls):
    if label in REGISTERED_NODES:
        REGISTERED_NODES[label]["count"] += 1
        return label + " " + str(REGISTERED_NODES[label]["count"])
    else:
        REGISTERED_NODES[label] = {"id_or_class":cls, "count":0}
        return label + " 0"


class Field(ABC):
    def __init__(self):
        self.label = None
        self.value = None
        self.datatype = None

    @abstractmethod
    def imGuiInputDisplayer(self):
        pass

    @abstractmethod
    def imGuiOutputDisplayer(self):
        pass

# dict of fields that will be set at beginning of file, each will
GLOBALS = {}


class GenericFloatField(Field):
    def __init__(self, label="genfloat", default_or_start=0):
        self.value = default_or_start
        self.label = label

    def imGuiInputDisplayer(self):
        if (self.value is not None):
            dpg.add_input_float(label=self.label, default_value=self.value)

    def imGuiOutputDisplayer(self):
        if (self.value is not None):
            dpg.add_text(f"{self.label}: {self.value}")


class Node:
    def __init__(self):
        self.label = ""
        self.type = None

        # dict keys are internal labels. for now.
        self.input_fields = {}
        self.output_fields = {}

    def display(self):
        with dpg.node(label=self.label):
            for input_field in self.input_fields.values():
                with dpg.node_attribute(label=input_field.label):
                    input_field.imGuiInputDisplayer()
            for output_field in self.output_fields.values():
                with dpg.node_attribute(label=output_field.label, attribute_type=dpg.mvNode_Attr_Output):
                    output_field.imGuiOutputDisplayer()

class AccDataNode(Node):
    def __init__(self):
        self.label = "Accelerometer Data"
        self.type = NODE_TYPES["INPUT"]
        self.input_fields = {
            
        }
        self.output_fields = {
            "accx": GenericFloatField("AccX", 0),
            "accy": GenericFloatField("AccY", 0),
            "accz": GenericFloatField("AccZ", 0)
        }

        self.label = RegisterNode(self.label, AccDataNode)


    def display(self):
        return super().display()


NODES = [AccDataNode(), AccDataNode()]


dpg.create_context()

dpg.configure_app(
    docking=True,
    docking_space=True,
)

# callback runs when user attempts to connect attributes
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    print(sender, app_data)
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)

# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    # app_data -> link_id
    dpg.delete_item(app_data)

with dpg.window(label="Tutorial", width=400, height=400):

    with dpg.node_editor(callback=link_callback, delink_callback=delink_callback):
        for node in NODES:
            node.display()

with dpg.window(label="Nodes"):
    dpg.add_text("Pick your nodes here.")

dpg.create_viewport(title='DAC Studio', width=600, height=300)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
        
