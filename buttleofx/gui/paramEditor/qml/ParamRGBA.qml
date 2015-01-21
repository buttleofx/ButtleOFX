import QtQuick 2.0

Rectangle {
    id: root

    width: 160
    height: 60

    property variant win // you can hold this as a reference..

    Text {
        text: "Click here to open new window!"
        anchors.centerIn: parent
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            var component = Qt.createComponent("WindowColorWheel.qml")
            win = component.createObject(root)
            win.show()
        }
    }
}
