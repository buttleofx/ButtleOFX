import QtQuick 2.0
import "../ColorPicker/qml"

Rectangle {
    id: root

    width: 50
    height: 30
    color: Qt.rgba(model.object.r, model.object.g,model.object.b)
    border.width: 1
    border.color: "#333"
    radius: 3

    property variant win // you can hold this as a reference..

    MouseArea {
        anchors.fill: parent
        onClicked: {
            var component = Qt.createComponent("WindowColorWheel.qml")
            win = component.createObject(root)
            win.show()
        }
    }
}
