import sys
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from pathlib import Path

from treemodel import TreeModel


class Backend(QObject):
    def __init__(self):
        super().__init__()

        headers = ["Title", "Description"]
        file = Path(__file__).parent / "default.txt"

        self.model = TreeModel(headers, file.read_text())

    @Slot(result="QVariant")
    def getModel(self):
        return self.model


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    engine.load("tree.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())