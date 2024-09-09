from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

from node.graphics_socket import GraphicsSocket
from node.edge import Edge
from node.graphics_edge import GraphicsEdge


MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10  # in pixels


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, grScene, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)

        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.zoomClamp = False
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def initUI(self):
        # Make any drawn items smoother with antialiasing
        self.setRenderHints(QtGui.QPainter.Antialiasing |
                            QtGui.QPainter.TextAntialiasing |
                            QtGui.QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        # Turn off scroll bars
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Apply transformation under mouse position
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    # ----------------
    # EVENT FUNCTIONS
    # ----------------

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == QtCore.Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == QtCore.Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == QtCore.Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == QtCore.Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        """Allow dragging view upon middle mouse press

        Args:
            event (_type_): _description_
        """
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        fakeEvent = QtGui.QMouseEvent(
            event.type(), event.localPos(), event.screenPos(),
            QtCore.Qt.LeftButton, event.buttons() | QtCore.Qt.LeftButton,
            event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        # get item which we clicked on
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # logic
        if type(item) is GraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res:
                return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        # logic
        if self.mode == MODE_EDGE_DRAG:
            self.mode = MODE_NOOP
            if self.isDistanceClickAndReleaseSignificant(event):
                res = self.edgeDragEnd(item)
                if res:
                    return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
        self.getItemAtClick(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.drag_edge.grEdge.setDestination(pos.x(), pos.y())
            self.drag_edge.grEdge.update()

    def wheelEvent(self, event):
        pos = event.position()
        oldPos = self.mapToScene(pos.x(), pos.y())

        # Calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = self.zoomOutFactor
            self.zoom -= self.zoomStep

        # Set scene scale
        self.scale(zoomFactor, zoomFactor)

        # Translate view
        pos = event.position()
        newPos = self.mapToScene(pos.x(), pos.y())
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

    def keyPressEvent(self, event):
        match event.key():
            case QtCore.Qt.Key_Backspace:
                selected_items = self.grScene.selectedItems()
                selected_edges = [item.edge for item in selected_items
                                  if isinstance(item, GraphicsEdge)]
                self.remove_edges(selected_edges)
            case QtCore.Qt.Key_Delete:
                selected_items = self.grScene.selectedItems()
                selected_edges = [item.edge for item in selected_items
                                  if isinstance(item, GraphicsEdge)]
                self.remove_edges(selected_edges)
    # ----------------
    # HELPER FUNCTIONS
    # ----------------

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        print('Start dragging edge')
        print('  assign Start Socket')
        self.previous_edge = item.socket.edge
        self.drag_edge = Edge(self.grScene.scene, item.socket, None)

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP
        print('End dragging edge')

        if type(item) is GraphicsSocket:
            print('  assign End Socket')
            if item.socket.hasEdge() and \
               item.socket.edge != self.previous_edge:
                item.socket.edge.remove()
            if self.previous_edge:
                self.previous_edge.remove()
            self.drag_edge.end_socket = item.socket
            print(self.drag_edge.end_socket)
            self.drag_edge.start_socket.setConnectedEdge(self.drag_edge)
            self.drag_edge.end_socket.setConnectedEdge(self.drag_edge)
            self.drag_edge.updatePositions()
            return True

        self.drag_edge.remove()
        self.drag_edge = None

        return False

    def isDistanceClickAndReleaseSignificant(self, event):
        """ measures if the distance between the first LMB click is far
            enough from the LMB release given a threshold.
        """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = \
            EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() +
                dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq
    
    def remove_edges(self, edges: list[Edge]):
        for edge in edges:
            edge.remove()
