import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod

def add_input_float(**kwargs):
    kwargs.setdefault("width", 100)
    return dpg.add_input_float(**kwargs)

class Field:
    def __init__(self, fieldLabel, state=False, range=None):
        self.label = fieldLabel

        # if true, wont show and will be written ABSOLUTELY in the code
        # absolute means refered to as a global variable and not a
        # node-dependant local one.

        # if not set to True, by default it will be set to False which is a node dependant local variable,
        # for a vlaid state that isnt true, it should have a string referall name that refers to another node.
        self.state = state
        self.range = range


ID_NODE_HASHMAP = {}

class Node(ABC):
    def __init__(self):
        # name of registered node class
        self.NodeLabelAbsolute = None

        # display name of the code
        self.NodeLabel = None

        # Labels for all input fields
        self.InputFields = []
        self.OutputFields = []
        

    @abstractmethod
    def __str__(self):
        return

    def draw(self):
        with dpg.node(label=self.NodeLabel):
            for i, InputField in enumerate(self.InputFields):
                if InputField.state == True:
                    pass
                else:
                    with dpg.node_attribute(label=InputField.label) as id:
                        ID_NODE_HASHMAP[id] = [i, self, "INPUT"]
                        if InputField.state == False:
                            if InputField.range is None:
                                add_input_float(label=InputField.label)
                            else:
                                dpg.add_slider_float(label=InputField.label, min_value=InputField.range[0], max_value=InputField.range[1])
                        elif isinstance(InputField.state, str):
                            dpg.add_text("binded")
                       
                        # masked do nothing
            
            for i, OutputField in enumerate(self.OutputFields):
                
                if OutputField.state == True:
                    pass
                elif OutputField.state == False:
                    with dpg.node_attribute(label=OutputField.label,attribute_type=dpg.mvNode_Attr_Output) as id:
                        ID_NODE_HASHMAP[id] = [i, self, "OUTPUT"]
                        dpg.add_text(OutputField.label)


class MPU6500_Accelerometer_Data_Node(Node):
    def __init__(self):
        super().__init__()

        self.NodeLabelAbsolute = "Accelerometer Data"

        self.InputFields = [
            Field("AccX", True),
            Field("AccY", True),
            Field("AccZ", True)
        ]

        self.OutputFields = [
            Field("Accelerometer X"),
            Field("Accelerometer Y"),
            Field("Accelerometer Z")
        ]

    def __str__(self):
        return ""

class ServoOutputNode(Node):
    def __init__(self):
        super().__init__()

        self.NodeLabelAbsolute = "Servo Output"

        self.InputFields = [
            Field("Servo Yaw"),
            Field("Servo Pitch"),
            Field("Servo Roll")
        ]

        self.OutputFields = [
            Field("servoYaw", True),
            Field("servoPitch", True),
            Field("servoRoll", True)
        ]

    def __str__(self):
        return ""

nodes = []
nodes_in_right_format = {}
node_label_counts = {}

def insertNode(node : Node):
    node_label_counts[node.NodeLabelAbsolute] = node_label_counts.get(node.NodeLabelAbsolute, -1) + 1
    node.NodeLabel = node.NodeLabelAbsolute + " " + str(node_label_counts[node.NodeLabelAbsolute])
    nodes.append(node)

for _ in range(2):
    insertNode(MPU6500_Accelerometer_Data_Node())
    insertNode(ServoOutputNode())

dpg.create_context()

dpg.configure_app(
    docking=True,
    docking_space=True,
    init_file="dac-studio-layout.ini",
    load_init_file=True,
)

def norm_nodes(ids):
    id0, id1=  ids 
    if ID_NODE_HASHMAP[id0][2] == "OUTPUT":
        return [id1] + ID_NODE_HASHMAP[id1][:2], [id0] + ID_NODE_HASHMAP[id0][:2]
    return [id0] + ID_NODE_HASHMAP[id0][:2], [id1] + ID_NODE_HASHMAP[id1][:2]

old_links = {}
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    ni,no = norm_nodes(app_data)
    iid, ifid, ifn = ni 
    oid, ofid, ofn = no 


    
    print(sender, app_data)

    if iid in old_links:
        dpg.delete_item(old_links[iid])

    old_links[iid]= dpg.add_node_link(iid, oid, parent=sender)
    


def delink_callback(sender, app_data):
    # app_data -> link_id
    dpg.delete_item(app_data)

with dpg.window(label="Tutorial", width=1200, height=900):

    with dpg.node_editor(callback=link_callback, delink_callback=delink_callback):
        for node in nodes:
            node.draw()

with dpg.window(label="Nodes"):
    dpg.add_text("Pick your nodes here.")

dpg.create_viewport(title='DAC Studio', width=1200, height=900)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

dpg.save_init_file("dac-studio-layout.ini")

dpg.destroy_context()
        
