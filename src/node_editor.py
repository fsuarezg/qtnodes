from PySide6 import QtWidgets
# from PySide6 import QtGui

from scene_manager import SceneManager
from graphics_view import GraphicsView
from node.node import Node
from node.edge import Edge


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

        self.addDebugData()
        # node = Node(self.scene, "My Awesome Node", 
        #             inputs=[1, 2, 3], outputs=[1])

        self.view = GraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()

    def addDebugData(self):
        node1 = Node(self.scene, "My Awesome Node 1", 
                     inputs=[1, 2, 3], outputs=[1])
        node2 = Node(self.scene, "My Awesome Node 2",
                     inputs=[1, 2, 3], outputs=[1])
        node3 = Node(self.scene, "My Awesome Node 3",
                     inputs=[1, 2, 3], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0])
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[0])


        # greenBrush = QtGui.QBrush(QtGui.Qt.green)
        # outlinePen = QtGui.QPen(QtGui.Qt.black)
        # outlinePen.setWidth(2)
        # rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        # rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)