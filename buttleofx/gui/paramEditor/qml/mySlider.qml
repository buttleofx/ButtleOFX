import QtQuick 1.1

Rectangle {
    implicitWidth : 300
    implicitHeight : 30
    color: "red"

    Rectangle {
        id: barSlider
        anchors.centerIn: parent
        color: white
        width: 200
        height: 2
    }
    Rectangle {
        anchors.verticalCenter: parent.verticalCenter
        radius: 1
        id: cursorSlider
        height: 10
        width: 10
        color: white
    }
}