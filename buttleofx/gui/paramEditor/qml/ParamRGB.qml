import QtQuick 2.0
import QtQuick.Layouts 1.1
import "../ColorPicker/qml"

RowLayout {

    property variant win // you can hold this as a reference..

    Rectangle {
        id: root
        width: parent.width / 2
        height: 30
        color: Qt.rgba(model.object.r, model.object.g,model.object.b, 255)
        border.width: 1
        border.color: "#333"
        radius: 3
    }
    MouseArea {
        anchors.fill: parent
        onClicked: {
            var component = Qt.createComponent("WindowColorWheelRGB.qml")
            win = component.createObject(root)
            win.show()
        }
    }
}


