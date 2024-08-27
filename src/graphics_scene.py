from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore
import math


class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None, scene_width=64000, scene_height=64000):
        super(GraphicsScene, self).__init__(parent)
        self.scene_width = scene_width
        self.scene_height = scene_height
        self.initUI()

    @property
    def _color_background(self):
        return QtGui.QColor('#393939')

    @property
    def _color_light(self):
        return QtGui.QColor('#2f2f2f')

    @property
    def _color_dark(self):
        return QtGui.QColor('#292929')

    @property
    def _grid_size(self):
        return 20

    @property
    def _grid_squares(self):
        return 5

    def initUI(self):
        self._pen_light = QtGui.QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QtGui.QPen(self._color_dark)
        self._pen_dark.setWidth(2)
        self.setBackgroundBrush(self._color_background)

        self.setSceneSize(self.scene_width, self.scene_width)

    def setSceneSize(self, width, height):
        self.scene_width = width
        self.scene_height = height
        self.setSceneRect(-width//2, -height//2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # create grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self._grid_size)
        first_top = top - (top % self._grid_size)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self._grid_size):
            if (x % (self._grid_size*self._grid_squares) != 0):
                lines_light.append(QtCore.QLine(x, top, x, bottom))
            else:
                lines_dark.append(QtCore.QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self._grid_size):
            if (y % (self._grid_size*self._grid_squares) != 0):
                lines_light.append(QtCore.QLine(left, y, right, y))
            else:
                lines_dark.append(QtCore.QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)

