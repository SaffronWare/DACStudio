import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod

NODE_TYPES = {
    "OUTPUT": 1,
    "INPUT": 0,
    "INTER": 0.5,
}


REGISTERED_NODES = {}

class Field:
    def __init__(self, fieldLabel, masked=False):
        self.fieldLabel = fieldLabel

        # if true, wont show and will be written ABSOLUTELY in the code
        # absolute means refered to as a global variable and not a
        # node-dependant local one.
        self.masked = masked

class Node:
    def __init__(self):
        # name of registered node class
        self.NodeLabelAbsolute = None

        # display name of the code
        self.NodeLabel = None

        # Labels for all input fields
        self.InputFields = []
        self.OutputFields = []

        # if false or missing, 
        self.InputMasks = []
        self.OutputMasks = []

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
        
