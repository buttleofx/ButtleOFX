import QtQuick 2.0
import "ColorFunctions.js" as ColorFunctions

// Group of inputs
Rectangle {
    id: colorFields
    implicitWidth: 80
    implicitHeight: 200
    color: "transparent"

    // Properties used to change the text in the boxes r, g, b with default values here
    property color currentColor: "white"
    property string alphaColorText: "#FFFFFFFF"

    property real redInput: 0
    property real greenInput: 0
    property real blueInput: 0
    property real alphaInput: 0

    // Used to inform colorPicker.qml that the value has changed
    property real newAlphaInput
    property real newRedInput
    property real newGreenInput
    property real newBlueInput

    property bool hasAlpha: true

    // Column containing the inputs colors
    Column {
        anchors.fill: parent
        anchors.leftMargin: 5
        anchors.rightMargin: 5
        anchors.topMargin: 5
        height: parent.height
        spacing: 6

        // Rectangle displaying the current selected color
        Rectangle {
            id: currentColorBox
            width: parent.width
            height: parent.height / 5 + 1

            SquaresGrid {
                cellSide: 3
                height: currentColorBox.height
                width: currentColorBox.width
            }

            Rectangle {
                width: parent.width
                height: parent.height
                border.width: 1
                border.color: "black"
                color: colorFields.currentColor
            }

            MouseArea {
                anchors.fill: parent
            }
        }

        // Rectangle displaying the current alpha color under the text form, for example #FF112233 (hexadecimal notation)
        Rectangle {
            id: alphaColorBox
            width: 70
            height: 15
            radius: 2
            border.width: 1
            border.color: "#FF525255"
            color: "#333"
            clip: true
            anchors.horizontalCenter: parent.horizontalCenter
            visible: colorFields.hasAlpha

            TextInput {
                id: alphaColorText
                anchors.fill: parent
                anchors.leftMargin: 4
                anchors.topMargin: 1
                color: "white"
                selectionColor: "grey"
                font.pixelSize: 11
                maximumLength: 9
                focus: true
                selectByMouse: true
                text: colorFields.alphaColorText
            }
        }

        // R, G, B color values boxes
        Column {
            width: parent.width
            spacing: 4

            // newRedInput, newGreenInput, newBlueInput, newAlphaInput defined as properties in this file, newValueInput defined in ColorInput.qml
            // We need to divide the values by 255 to send a value between 0 and 1
            ColorInput {
                id: rInput
                colorName: "R:"
                valueInput: redInput
                minValue: 0
                maxValue: 255

                onNewValueInputChanged: {
                    newRedInput = newValueInput/255
                }
            }

            ColorInput {
                id: gInput
                colorName: "G:"
                valueInput: greenInput
                minValue: 0
                maxValue: 255

                onNewValueInputChanged: {
                    newGreenInput = newValueInput/255
                }
            }

            ColorInput {
                id: bInput
                colorName: "B:"
                valueInput: blueInput
                minValue: 0
                maxValue: 255

                onNewValueInputChanged: {
                    newBlueInput = newValueInput/255
                }
            }

            ColorInput {
                id: aInput
                colorName: "A:"
                valueInput: alphaInput
                minValue: 0
                maxValue: 255

                onNewValueInputChanged: {
                    newAlphaInput = newValueInput/255
                }
                visible: colorFields.hasAlpha
            }
        }
    }
}
