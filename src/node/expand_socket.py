from node.graphics_expand_socket import GraphicsExpandSocket
from node.socket import (LEFT_CENTER)


class ExpandSocket():
    def __init__(self, node, index=0, position=LEFT_CENTER):

        self.node = node
        self.index = index
        self.position = position

        self.grSocket = GraphicsExpandSocket(self)
        self.grSocket.setPos(*self.node.getExpandSocketPosition(index,
                                                                position))

        self.edge = None

    def getExpandSocketPosition(self):
        res = self.node.getExpandSocketPosition(self.index, self.position)
        return res

    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        if self.edge:
            return True
        else:
            return False
