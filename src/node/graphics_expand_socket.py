from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from config.colors import (COLOR_EXPAND_SOCKET, COLOR_SOCKET_BORDER,
                           COLOR_SOCKET_PLUS)
from config.constants import (SOCKET_RADIUS, SOCKET_OUTLINE_WIDTH)


class GraphicsExpandSocket(QtWidgets.QGraphicsItem):
    def __init__(self, socket):
        self.socket = socket
        super().__init__(socket.node.grNode)

        self.radius = (SOCKET_RADIUS*1.5)+1
        self.outline_width = SOCKET_OUTLINE_WIDTH
        self._color_background = QtGui.QColor(COLOR_EXPAND_SOCKET)
        self._color_outline = QtGui.QColor(COLOR_SOCKET_BORDER)
        self._color_plus = QtGui.QColor(COLOR_SOCKET_PLUS)

        self._pen = QtGui.QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QtGui.QBrush(self._color_background)
        self._pluspen = QtGui.QPen(self._color_plus)
        self._pluspen.setWidthF(self.outline_width)
        self._plusbrush = QtGui.QBrush(self._color_plus)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # painting circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius,
                            -self.radius, 2 * self.radius, 2 * self.radius)
        # painting plus sign
        painter.setBrush(self._plusbrush)
        painter.setPen(self._pluspen)
        rectangle1 = QtCore.QRectF(-self.radius/3/2, -self.radius/2,
                                   self.radius/3, self.radius)
        rectangle2 = QtCore.QRectF(-self.radius/2, -self.radius/3/2,
                                   self.radius, self.radius/3)
        painter.drawRect(rectangle1)
        painter.drawRect(rectangle2)

    def boundingRect(self):
        return QtCore.QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )