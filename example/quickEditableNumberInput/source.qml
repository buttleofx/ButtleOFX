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
            anchors.fill: parent

            // Access to all properties of a classic qml textInput by textInput.<textIntproperty>
            textInput.text: root.linkedText
            textInput.color: "red"

            // Must use this signal to unbreak text link
            onQuickUpdate: root.linkedText = text
        }

    }

    // Example how tu add a new behaviour from external
    Rectangle {
        color: "red"
        width:parent.width
        height:50

        Text {
            anchors.centerIn: parent
            text: "Increment first number"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                numberInput.textInput.cursorPosition = 0
                numberInput.updateValue(1)
            }
        }
    }
}
