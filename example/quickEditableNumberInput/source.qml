import QtQuick 2.0
import "../../qml/QuickMamba"
import QtQuick.Controls 1.1

Rectangle
{
    id: root
    color: "black"
    width: 500
    height: 500

    property string linkedText: "42.42"

    Rectangle {
        color: "white"
        width: 150
        height: 50
        anchors.centerIn: parent

        QuickEditableNumberInput {
            id: numberInput
            anchors.centerIn: parent

            text: root.linkedText

            onQuickUpdate: root.linkedText = text
        }

    }
}
