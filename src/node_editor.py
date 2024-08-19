from PySide6 import QtWidgets

from node_graphics_scene import GraphicsScene
from node_graphics_view import GraphicsView

class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)
        self.initialize_ui()

    def initialize_ui(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.grScene = GraphicsScene()

        self.view = GraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()