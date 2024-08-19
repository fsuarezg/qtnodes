from PySide6 import QtWidgets

class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)
        self.initialize()

    def initialize(self):
        self.setGeometry(200, 200, 800, 600)

        self.setWindowTitle("HELLO")
        self.show()