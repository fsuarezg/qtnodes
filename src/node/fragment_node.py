from node.node import Node

class FragmentNode(Node):
    def __init__(self, scene, title="Fragment", inputs=[], outputs=[]):
        super().__init__(scene, title, inputs, outputs)