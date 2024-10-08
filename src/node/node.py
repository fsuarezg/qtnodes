from node.graphics_node import GraphicsNode
from node.socket import (Socket,
                         LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM,
                         LEFT_CENTER, RIGHT_CENTER)
from node.expand_socket import ExpandSocket

from config.constants import (NODE_SOCKET_SPACING)


class Node():
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[],
                 grNodeclass=GraphicsNode):
        self.scene = scene

        self.title = title

        nr_sockets = max(len(inputs), len(outputs))
        self.grNode = grNodeclass(self, self.title, nr_sockets=nr_sockets)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = NODE_SOCKET_SPACING

        # create expend sockets

        # self.socket_in = ExpandSocket(node=self, index=0,
        #                               position=LEFT_CENTER)
        # self.socket_out = ExpandSocket(node=self, index=0,
        #                                position=RIGHT_CENTER)

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP)
            counter += 1
            self.outputs.append(socket)

    @property
    def pos(self):
        return self.grNode.pos()        # QPointF

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def getSocketPosition(self, index, position):
        if position in (LEFT_TOP, LEFT_BOTTOM):
            x = 0
        else:
            x = self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_size \
                - self.grNode._padding - index * self.socket_spacing
        else:
            # start from top
            y = self.grNode.title_height + self.grNode._padding \
                + self.grNode.edge_size + index * self.socket_spacing

        return [x, y]
    
    def getExpandSocketPosition(self, index, position):
        if position == LEFT_CENTER:
            x = 0
        else:
            x = self.grNode.width

        y = (self.grNode.title_height + self.grNode._padding 
             + self.grNode.edge_size + index * self.socket_spacing)

        print(x, y)
        return [x, y]
    
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()


