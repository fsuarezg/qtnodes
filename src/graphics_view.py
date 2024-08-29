from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

from node.graphics_socket import GraphicsSocket
from node.edge import Edge


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

    def wheelEvent(self, event):
        # Store scene position
        # BUG: Pyside 6.7 has a bug where mapToScene needs to have exact
        # (int, int) type passed. Normally I should be able to pass on the
        # event.position() directly
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
        # BUG: see above
        pos = event.position()
        newPos = self.mapToScene(pos.x(), pos.y())
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        print('Start dragging edge')
        print('  assign Start Socket')
        self.dragEdge = Edge(self.grScene.scene, item.socket, None)

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP
        print('End dragging edge')

        if type(item) is GraphicsSocket:
            print('  assign End Socket')
            return True

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

