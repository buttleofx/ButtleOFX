import QtQuick 2.0
import "../ColorPicker/qml"
import "../../../gui"
import QtQuick.Layouts 1.1

RowLayout {
    id: root

    // you can hold this as a reference
    property variant win

    Rectangle {
        width: parent.width / 2
        height: 30
        color: Qt.rgba(model.object.r, model.object.g, model.object.b, 255)
        border.width: 1
        border.color: "#333"
    }

    Rectangle {
        width: parent.width / 3
        height: 30

        Image {
            anchors.fill: parent
            source:_buttleData.buttlePath + "/gui/img/background/checkerboard.jpg"
            fillMode: Image.Tile
        }

        Rectangle {
            anchors.fill: parent
            color: "black"
            opacity : model.object.a
            border.width: 1
            border.color: "#333"
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            var component = Qt.createComponent("WindowColorWheelRGBA.qml")
            win = component.createObject(root)
            win.show()
        }
    }
}
