import QtQuick 2.0
import QuickMamba 1.0
import QtQuick.Controls 1.1

Rectangle
{
    id: root
    color: "black"
    width: 300
    height: 250

    Rectangle {
        color:screenPicker.currentColor
        width: 50
        height: 50

        MouseArea {
            anchors.fill: parent
            onPressed: screenPicker.grabbing = true
        }
    }

    ScreenPicker {
        id:screenPicker
    }
}
