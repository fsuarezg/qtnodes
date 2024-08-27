from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui


class GraphicsNode(QtWidgets.QGraphicsItem):
    def __init__(self, node, title='Node Graphics Item', parent=None):
        super().__init__(parent)

        self._title_color = QtCore.Qt.white
        self._title_font = QtGui.QFont("Ubuntu", 10)

        self.width = 180
        self.height = 240
        self.edge_size = 10.0
        self.title_height = 24.0
        self._padding = 4.0

        self._pen_default = QtGui.QPen(QtGui.QColor("#7F000000"))
        self._pen_selected = QtGui.QPen(QtGui.QColor("#FFFFA637"))

        self._brush_title = QtGui.QBrush(QtGui.QColor("#FF313131"))
        self._brush_background = QtGui.QBrush(QtGui.QColor("#E3212121"))

        self.initTitle()
        self.title = title

        self.initUI()

    def boundingRect(self):
        return QtCore.QRectF(
            0,
            0,
            2 * self.edge_size + self.width,
            2 * self.edge_size + self.height
        ).normalized()

    def initUI(self):
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)

    def initTitle(self):
        self.title_item = QtWidgets.QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width
            - 2 * self._padding
        )

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QtGui.QPainterPath()
        path_title.setFillRule(QtCore.Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height,
                                  self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size,
                           self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size,
                           self.title_height - self.edge_size,
                           self.edge_size, self.edge_size)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QtGui.QPainterPath()
        path_content.setFillRule(QtCore.Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height,
                                    self.width,
                                    self.height - self.title_height,
                                    self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height,
                             self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height,
                             self.edge_size, self.edge_size)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QtGui.QPainterPath()
        path_outline.addRoundedRect(0, 0,
                                    self.width, self.height,
                                    self.edge_size, self.edge_size)
        painter.setPen(
            self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
