from PySide6 import QtWidgets
# from PySide6 import QtGui

from scene_manager import SceneManager
from graphics_view import GraphicsView
from node.node import Node


class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.scene = SceneManager()
        # self.grScene = self.scene.grScene

        node = Node(self.scene, "My Awesome Node", 
                    inputs=[1, 2, 3], outputs=[1])

        self.view = GraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()

        # greenBrush = QtGui.QBrush(QtGui.Qt.green)
        # outlinePen = QtGui.QPen(QtGui.Qt.black)
        # outlinePen.setWidth(2)
        # rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        # rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)