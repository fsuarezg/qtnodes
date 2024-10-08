from node.graphics_edge import (GraphicsEdgeDirect, GraphicsEdgeBezier)


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2


class Edge:
    def __init__(self, scene, start_socket, end_socket,
                 edge_type=EDGE_TYPE_BEZIER):

        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.setConnectedEdge(edge=self)
        if self.end_socket is not None:
            self.end_socket.setConnectedEdge(edge=self)

        if edge_type == EDGE_TYPE_DIRECT:
            self.grEdge = GraphicsEdgeDirect(self)
        else:
            self.grEdge = GraphicsEdgeBezier(self)

        self.scene.grScene.addItem(self.grEdge)
        self.scene.addEdge(self)
        self.updatePositions()

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)
        self.grEdge.update()

    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)
