import QtQuick 2.0
import QuickMamba 1.0
import QtQuick.Controls 1.1

Rectangle
{
    id: root
    color: "black"
    width: 300
    height: 250

    ScreenPicker {
        id:screenPicker
        anchors.fill: parent
    }
}
