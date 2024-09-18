import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("File System TreeView")

    TreeView {
        id: treeView
        anchors.fill: parent
        model: backend.getModel()

        delegate: Item {
            id: treeDelegate
            implicitWidth: treeView.width/2
            implicitHeight: 20

            Row {
                spacing: 5
                Text {
                    text: model.display
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }
    }
}