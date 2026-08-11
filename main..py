import dearpygui.dearpygui as dpg
from abc import abstractmethod, ABC

OUTPUT_FIELD = 1
INPUT_FIELD = 0
CURR_NODES = {}

CONSTANTS = {
    "X_MAPS_TO": 0,
    "Y_MAPS_TO": 0,
    "Z_MAPS_TO": 0,

    "SERVO_YAW_PIN": 0,
    "SERVO_PITCH_PIN": 0,
    "SERVO_ROLL_PIN": 0,

    "DELAY_BEFORE_START_RECORDING_IN_SECONDS": 0,
    "SHOULD_RECORD_DATA": 1,
}

VARIABLES = {}


def jjoin(*args):
    return "::".join(list(args))

def njoin(*args):
    return "_".join(list(args))

def ssplit(string):
    return string.split("::")


class NodeField:
    def __init__(self, label, parent, vrange=None):
        self.drawn = False
        self.connection = None # not updated if its an output field
        self.label = label
        self.range = vrange
        self.parent = parent

    def fullpath(self):
        return jjoin(self.parent.label, self.label)

    def __str__(self):
        return "var_" + "".join(self.parent.label.split()) + "_" + "".join(self.label.split())
    
    def update_draw(self):
            
            if not self.drawn:
                #if self.connection is not None:
                dpg.add_text(self.label, 
                            tag=jjoin(self.parent.label, self.label, "CONNECTED"))
               
                #elif self.range is None:
                dpg.add_input_float(label=self.label, 
                                    tag=jjoin(self.parent.label, self.label, "FLOATVAL"), width=100)
        
           
                dpg.add_slider_float(label=self.label, 
                                    min_value=0, 
                                    max_value=1, 
                                    tag=jjoin(self.parent.label, self.label, "FLOATRAN"), width=100)
          
                self.drawn = True
                self.update_draw()
            elif self.drawn:
                dpg.hide_item(jjoin(self.parent.label, self.label, "CONNECTED"))
                dpg.hide_item(jjoin(self.parent.label, self.label, "FLOATVAL"))
                dpg.hide_item(jjoin(self.parent.label, self.label, "FLOATRAN"))

                if self.connection is not None:
                    dpg.show_item(jjoin(self.parent.label, self.label, "CONNECTED"))
                elif not self.range:
                    dpg.show_item(jjoin(self.parent.label, self.label, "FLOATVAL"))
                else:
                    dpg.show_item(jjoin(self.parent.label, self.label, "FLOATRAN"))
                    dpg.configure_item(jjoin(self.parent.label, self.label, "FLOATRAN"), min_value=self.range[0], max_value=self.range[1])

class Node(ABC):

    node_types_and_counts = {}
    registered_nodes = {}

    def __str__(self, srcstr):
        i = 0
        out = ""
        while i < len(srcstr):
            char = srcstr[i]
            if char  == "~":
                i += 1
                var_output_index = int(srcstr[i])
                out += self.nodes[OUTPUT_FIELD][var_output_index]
                i += 1
            elif char == "$":
                i += 1
                var_input_index = int(srcstr[i])
                out += self.nodes[INPUT_FIELD][var_input_index].connection
                i += 1
            else:
                out += char
            i += 1
        return out
        

    def __init__(self):
        self.node_title = None
        self.label = None 
        self.nodes = {INPUT_FIELD: [], OUTPUT_FIELD: []}
        self.hashed_nodes = {}
        self.drawn = False

    def hash_nodes(self):
        for node in self.nodes[INPUT_FIELD]:
            self.hashed_nodes[node.label] = [node, INPUT_FIELD]
        
        for node in self.nodes[OUTPUT_FIELD]:
            self.hashed_nodes[node.label] = [node, OUTPUT_FIELD]

    def register(self, obj, unique=False):
        self.hash_nodes()
        class_name = obj.node_title
        if not unique:
            
        
            Node.node_types_and_counts[class_name] = Node.node_types_and_counts.get(class_name, 0) + 1
            Node.registered_nodes[class_name + str(Node.node_types_and_counts[class_name] - 1)] = obj
            return class_name + str(Node.node_types_and_counts[class_name] - 1)
        else:
            if class_name in Node.node_types_and_counts:
                return None
            else:
                Node.registered_nodes[class_name] = obj
                Node.node_types_and_counts[class_name] = "UNIQUE"
                return class_name


    def draw(self, pparent=None):
        if not self.drawn:
            with dpg.node(label=self.label, tag=self.label) if pparent is None else dpg.node(label=self.label, tag=self.label, parent=pparent):
                for node in self.nodes[INPUT_FIELD]:
                    with dpg.node_attribute(label=node.label, tag=jjoin(self.label, node.label)):
                        node.update_draw()
                for node in self.nodes[OUTPUT_FIELD]:
                    with dpg.node_attribute(label=node.label, tag=jjoin(self.label, node.label), attribute_type=dpg.mvNode_Attr_Output):
                        node.update_draw()
        else:
            for node in self.nodes[INPUT_FIELD] + self.nodes[OUTPUT_FIELD]:
                node.update_draw()

class ACCNODE(Node):

    source_reference = """
    ~1~ = s_AccX;
    ~2~ = s_AccY;
    ~3~ = s_AccZ;
"""

    def __init__(self):
        super().__init__()
        self.node_title = "Accelerometer"
        self.nodes[OUTPUT_FIELD] = [
            NodeField("Acceleration X", self),
            NodeField("Acceleration Y", self),
            NodeField("Acceleration Z", self)
        ]

        self.label = self.register(self)

    

"""
class VARNODE(Node):
    

    def __init__(self, varname):
        super().__init__()
        self.node_title = "set " + varname
        self.nodes[INPUT_FIELD] = [
            NodeField(varname, self)
        ]
        

        self.label = self.register(self, True)
        """


class GYRONODE(Node):
    source_reference = """
    ~1~ = s_GyroX;
    ~2~ = s_GyroY;
    ~3~ = s_GyroZ;
"""

    def __init__(self):
        super().__init__()
        self.node_title = "Gyroscope"
        self.nodes[OUTPUT_FIELD] = [
            NodeField("Gyroscope X", self),
            NodeField("Gyroscope Y", self),
            NodeField("Gyroscope Z", self)
        ]

        self.label = self.register(self)

class SERVONODE(Node):
    source_reference = """
    s_ServoYaw = $1$;
    s_ServoRoll = $2$;
    s_ServoPitch = $3$;
"""
    def __init__(self):
        super().__init__()
        self.node_title = "Airplane Servos"
        self.nodes[INPUT_FIELD] = [
            NodeField("Servo Yaw", self),
            NodeField("Servo Roll", self),
            NodeField("Servo Pitch", self)
        ]

        self.label = self.register(self, True)



def link_callback(sender, app_data):

    n1 ,f1 = ssplit(app_data[0])
    n2,f2 = ssplit(app_data[1])

    ninfo1 = Node.registered_nodes[n1].hashed_nodes[f1][1]
    ninfo2 = Node.registered_nodes[n2].hashed_nodes[f2][1]

    inNode = None
    ouNode = None
    if ninfo1 == INPUT_FIELD:
        pass 
    else:
        n1,n2 = n2, n1
        f1, f2 = f2, f1

    inNode = Node.registered_nodes[n1].hashed_nodes[f1][0]
    ouNode = Node.registered_nodes[n2].hashed_nodes[f2][0]



    if inNode.connection is not None:
        print(f"deleting connection: {jjoin(inNode.fullpath(), inNode.connection.fullpath())}")
        dpg.delete_item(jjoin(inNode.fullpath(), inNode.connection.fullpath()))

    inNode.connection = ouNode
    Node.registered_nodes[n1].hashed_nodes[f1][0] = inNode
        
    
    print(n1,f1,n2,f2)
    print(f"creating {jjoin(inNode.fullpath(), ouNode.fullpath())}")
    dpg.add_node_link(app_data[0], app_data[1], parent=sender, tag=jjoin(inNode.fullpath(), ouNode.fullpath()))
    
def delink_callback(sender, app_data):
    dpg.delete_item(app_data)

def add_node_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


    match sender:
            case "acc_node":
                return ACCNODE().draw("main")
            case "gyro_node":
                return GYRONODE().draw("main")
            case "servo_node":
                return SERVONODE().draw("main")

    


def add_node_menu():
    dpg.add_text("Pick your nodes here")
    dpg.add_button(label="Add accelerometer node", callback=add_node_callback, tag="acc_node")
    dpg.add_button(label="Add gyroscope node", callback=add_node_callback, tag="gyro_node")
    dpg.add_button(label="Add servo output node",callback=add_node_callback, tag="servo_node")

def add_constant():
    name = dpg.get_value("ADD_CONSTANT")
    if name not in CONSTANTS:
        CONSTANTS[name] = 0
        dpg.add_text(name, before="VARIABLES_TEXT")
        dpg.add_input_float(label="", default_value=0, tag="c::" + name, parent="config-page", before="VARIABLES_TEXT")

        #print(name)

def add_variable():
    name =dpg.get_value("ADD_VARIABLE")
    if name not in VARIABLES:
        CONSTANTS[name] = 0
        dpg.add_text(name, parent='config-page')
    
def configuration_menu():
    dpg.add_text("CONSTANTS")

    with dpg.group(horizontal=True):
           dpg.add_input_text(tag="ADD_CONSTANT")
           dpg.add_button(label="ADD", callback=add_constant)

    for name, value in CONSTANTS.items():
        dpg.add_text(name)
        dpg.add_input_float(label="", default_value=value, tag="c::" + name)

    dpg.add_text("VARIABLES", tag="VARIABLES_TEXT")

    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="ADD_VARIABLE")
        dpg.add_button(label="ADD", callback=add_variable)
    
    for name,value in VARIABLES.items():
        dpg.add_text(name)
        dpg.add_text(label="",  tag="v::"+name)


def main():
    dpg.create_context()

    dpg.configure_app(
        docking=True,
        docking_space=True,
        init_file="dac-studio-layout.ini",
        load_init_file=True,
    )

    
    dpg.create_viewport(title='DAC Studio', width=1200, height=900)
    

    with dpg.window(label="Tutorial", width=1200, height=900):
        
            with dpg.node_editor(callback=link_callback, delink_callback=delink_callback, tag="main"):
                    for node in Node.registered_nodes:
                        node.draw()
        
            
            with dpg.window(label="Nodes"):
                add_node_menu()
        
            with dpg.window(label="Configuration", tag="config-page"):
                configuration_menu()
        
            print("this will run every frame")

    

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

    dpg.save_init_file("dac-studio-layout.ini")

    dpg.destroy_context()

if __name__ == '__main__':
    main()