import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod

class Field:
    def __init__(self, fieldLabel, masked=False):
        self.fieldLabel = fieldLabel

        # if true, wont show and will be written ABSOLUTELY in the code
        # absolute means refered to as a global variable and not a
        # node-dependant local one.

        # if not set to True, by default it will be set to False which is a node dependant local variable,
        # for a vlaid state that isnt true, it should have a string referall name that refers to another node.
        self.masked = masked

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

class MPU6500_Accelerometer_Data_Node(Node):
    def __init__(self):
        super().__init__()
        self.InputFields = [
            Field("AccX"),
            Field("AccY"),
            Field("AccZ")
        ] 

dpg.create_context()

dpg.configure_app(
    docking=True,
    docking_space=True,
    init_file="dac-studio-layout.ini",
    load_init_file=True,
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

dpg.save_init_file("dac-studio-layout.ini")

dpg.destroy_context()
        
