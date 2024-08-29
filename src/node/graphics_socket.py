from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from config.colors import (COLOR_SOCKET, COLOR__SOCKET_BORDER)


class GraphicsSocket(QtWidgets.QGraphicsItem):
    def __init__(self, socket, socket_type=1):
        self.socket = socket
        super().__init__(socket.node.grNode)

        self.radius = 6.0
        self.outline_width = 1.0
        self._color_background = QtGui.QColor(COLOR_SOCKET)
        self._color_outline = QtGui.QColor(COLOR__SOCKET_BORDER)

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