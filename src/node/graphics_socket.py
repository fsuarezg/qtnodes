from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from config.colors import (COLOR_SOCKET, COLOR_SOCKET_BORDER)
from config.constants import (SOCKET_RADIUS, SOCKET_OUTLINE_WIDTH)


class GraphicsSocket(QtWidgets.QGraphicsItem):
    def __init__(self, socket, socket_type=1):
        self.socket = socket
        super().__init__(socket.node.grNode)

        self.radius = SOCKET_RADIUS
        self.outline_width = SOCKET_OUTLINE_WIDTH
        self._color_background = QtGui.QColor(COLOR_SOCKET)
        self._color_outline = QtGui.QColor(COLOR_SOCKET_BORDER)

        self._pen = QtGui.QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QtGui.QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # painting circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius,
                            -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self):
        return QtCore.QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )