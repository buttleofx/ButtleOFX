import QtQuick 2.0
import "../ColorPicker/qml"
import "../../../gui"
import QtQuick.Layouts 1.1

RowLayout {
    id: root

    // you can hold this as a reference
    property variant win

    Rectangle {

        width: 50
        height: 30
        color: Qt.rgba(model.object.r, model.object.g, model.object.b, 255)
        border.width: 1
        border.color: "#333"
        radius: 3
    }

    Rectangle {

        width: 50
        height: 30
        color: Qt.rgba(0, 0, 0, model.object.a)
        border.width: 1
        border.color: "#333"
        radius: 0

        Image {
            z: -1
            width: parent.width - 1
            height: parent.height - 1
            source:_buttleData.buttlePath + "/gui/img/background/checkerboard.jpg"
            fillMode: Image.Tile
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
