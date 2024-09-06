from PySide6 import QtWidgets
# from PySide6 import QtGui

from scene import Scene
from graphics_view import GraphicsView
from node.node import Node
from node.fragment_node import FragmentNode
from node.entity_node import EntityNode
from node.edge import Edge


class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # create graphics scene
        self.scene = Scene()

        self.addDebugData()

        self.view = GraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()

    def addDebugData(self):
        fragmentnode1 = FragmentNode(
                            self.scene,
                            inputs=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            outputs=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        entitynode1 = EntityNode(self.scene, inputs=[1, 2, 3], outputs=[1])
        fragmentnode2 = FragmentNode(self.scene, inputs=[1], outputs=[1])
        fragmentnode3 = FragmentNode(self.scene, inputs=[], outputs=[])
        fragmentnode1.setPos(-350, 0)
        entitynode1.setPos(-75, 0)
        fragmentnode2.setPos(200, 0)
        fragmentnode3.setPos(475, 0)

        edge1 = Edge(self.scene, fragmentnode1.outputs[0],
                     entitynode1.inputs[0])
        edge2 = Edge(self.scene, entitynode1.outputs[0],
                     fragmentnode2.inputs[0])


        # greenBrush = QtGui.QBrush(QtGui.Qt.green)
        # outlinePen = QtGui.QPen(QtGui.Qt.black)
        # outlinePen.setWidth(2)
        # rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        # rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)