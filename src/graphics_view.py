from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, grScene, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)

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
            self.rightMouseButtonPress(event)
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
        return super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        return super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

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
