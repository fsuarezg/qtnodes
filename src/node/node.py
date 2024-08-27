from node.graphics_node import GraphicsNode


class Node():
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene

        self.title = title

        self.grNode = GraphicsNode(self, self.title)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs = []
        self.outputs = []
