from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore 

class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, grScene, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.grScene = grScene
        self.initialize_ui()
        self.setScene(self.grScene)
    
    def initialize_ui(self):
        # Make any drawn items smoother with antialiasing
        self.setRenderHints(QtGui.QPainter.Antialiasing |
                            QtGui.QPainter.TextAntialiasing | 
                            QtGui.QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        # Turn off scroll bars
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

