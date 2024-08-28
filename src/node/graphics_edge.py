from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from abc import abstractmethod


class QDMGraphicsEdge(QtWidgets.QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        self._color = QtGui.QColor("#001000")
        self._color_selected = QtGui.QColor("#00ff00")
        self._pen = QtGui.QPen(self._color)
        self._pen_selected = QtGui.QPen(self._color_selected)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        if not self.isSelected():
            painter.setPen(self._pen)
        else:
            painter.setPen(self._pen_selected)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(self.path())

    @abstractmethod
    def updatePath(self):
        """ Will handle drawing QPainterPath from Point A to B """
        raise NotImplementedError(
            'This method has to be overriden in a child class')


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def updatePath(self):
        path = QtGui.QPainterPath(QtCore.QPointF(self.posSource[0],
                                                 self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]:
            dist *= -1

        path = QtGui.QPainterPath(QtCore.QPointF(self.posSource[0],
                                                 self.posSource[1]))
        path.cubicTo(s[0] + dist, s[1], d[0] - dist, d[1],
                     self.posDestination[0], self.posDestination[1])
        self.setPath(path)
