from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from abc import abstractmethod
import math

from config.colors import (COLOR_EDGE, COLOR_EDGE_SELECTED)
from node.socket import (RIGHT_TOP, RIGHT_BOTTOM,
                         LEFT_TOP, LEFT_BOTTOM)

EDGE_CP_ROUNDNESS = 100

class GraphicsEdge(QtWidgets.QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        self._color = QtGui.QColor(COLOR_EDGE)
        self._color_selected = QtGui.QColor(COLOR_EDGE_SELECTED)
        self._pen = QtGui.QPen(self._color)
        self._pen_selected = QtGui.QPen(self._color_selected)
        self._pen_dragging = QtGui.QPen(self._color)
        self._pen_dragging.setStyle(QtCore.Qt.DashLine)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        if not self.edge.end_socket:
            painter.setPen(self._pen_dragging)
        elif self.isSelected():
            painter.setPen(self._pen_selected)
        else:
            painter.setPen(self._pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(self.path())

    @abstractmethod
    def updatePath(self):
        """ Will handle drawing QPainterPath from Point A to B """
        raise NotImplementedError(
            'This method has to be overriden in a child class')


class GraphicsEdgeDirect(GraphicsEdge):
    def updatePath(self):
        path = QtGui.QPainterPath(QtCore.QPointF(self.posSource[0],
                                                 self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)


class GraphicsEdgeBezier(GraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        cpx_s = +dist
        cpy_s = 0
        cpx_d = -dist
        cpy_d = 0

        # Case where start socket is on the right side of the destnation socket
        sspos = self.edge.start_socket.position
        if (s[0] > d[0] and sspos in (RIGHT_TOP, RIGHT_BOTTOM)
            or (s[0] < d[0] and sspos in (LEFT_BOTTOM, LEFT_TOP))):
            cpx_d *= -1
            cpx_s *= -1

            # More rounded bezier curves 
            div_value = (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.0000001
            cpy_d = ((s[1] - d[1]) / math.fabs(div_value)) * EDGE_CP_ROUNDNESS
            div_value = (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.0000001
            cpy_s = ((d[1] - s[1]) / math.fabs(div_value)) * EDGE_CP_ROUNDNESS

        path = QtGui.QPainterPath(QtCore.QPointF(self.posSource[0],
                                                 self.posSource[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s,
                     d[0] + cpx_d, d[1] + cpy_d,
                     self.posDestination[0], self.posDestination[1])
        self.setPath(path)
