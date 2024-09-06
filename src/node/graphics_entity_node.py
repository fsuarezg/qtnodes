from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from node.graphics_node import GraphicsNode
from config.colors import COLOR_ENTITY


class GraphicsEntityNode(GraphicsNode):

    def __init__(self, node, title='Node Graphics Item', parent=None,
                 nr_sockets=1):
        super().__init__(node, title=title, parent=parent,
                         nr_sockets=nr_sockets)
        self._brush_title = QtGui.QBrush(QtGui.QColor(COLOR_ENTITY))