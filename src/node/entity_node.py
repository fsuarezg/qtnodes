from node.node import Node

class EntityNode(Node):
    def __init__(self, scene, title="Entity", inputs=[], outputs=[]):
        super().__init__(scene, title, inputs, outputs)