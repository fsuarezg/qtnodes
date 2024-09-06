from PySide6 import QtGui
from config.colors import COLOR_FRAGMENT

from node.node import Node
from node.graphics_fragment_node import GraphicsFragmentNode


class FragmentNode(Node):
    def __init__(self, scene, title="Fragment", inputs=[], outputs=[]):
        super().__init__(scene, title, inputs=inputs, outputs=outputs,
                         grNodeclass=GraphicsFragmentNode)