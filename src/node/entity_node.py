from node.node import Node
from node.graphics_entity_node import GraphicsEntityNode


class EntityNode(Node):
    def __init__(self, scene, title="Entity", inputs=[], outputs=[]):
        super().__init__(scene, title, inputs=inputs, outputs=outputs,
                         grNodeclass=GraphicsEntityNode)
        #self.grNode = GraphicsEntityNode(self.grNode)