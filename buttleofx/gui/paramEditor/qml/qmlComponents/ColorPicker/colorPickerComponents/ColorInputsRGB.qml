import QtQuick 2.0

// Group of inputs
Rectangle {
    id: colorFields
    implicitWidth: 80
    implicitHeight: 200
    color: "black"

    // Properties used to change the text in the boxes r, g, b and h, s, b
    property color currentColor: "white"
    property int redValue: 0
    property int greenValue: 0
    property int blueValue: 0
    property real hValue: 0
    property real sValue: 0
    property real bValue: 0

    // Test for enter colors values in inputs and adapt display
    // property real cursorColorPositionInputs: rInput.cursorPositionInput + gInput.cursorPositionInput + bInput.cursorPositionInput


    // Column containing the inputs colors
    Column {
        anchors.fill: parent
        anchors.leftMargin: 5
        anchors.rightMargin: 5
        anchors.topMargin: 5
        height: parent.height
        spacing: 6

        // Rectangle displaying the current color
        Rectangle {
            id: currentColorBox
            width: parent.width
            height: parent.height / 5

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

        // Rectangle displaying the current alpha color under the text form #AA112233
        /*
        Rectangle {
            id: alphaColorBox
            width: 70
            height: 15
            radius: 2
            border.width: 1
            border.color: "#FF525255"
            color: "transparent"
            clip: true
            anchors.horizontalCenter: parent.horizontalCenter
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

                onTextChanged: {
                    paramObject ? paramObject.r = rInput.colorValueText : 255
                    paramObject ? paramObject.g = gInput.colorValueText : 255
                    paramObject ? paramObject.b = bInput.colorValueText : 255
                }
            }
        }
        */

        // H, S, B color values boxes
        /*
        Column {
            width: parent.width
            spacing: 4
            ColorInput {
                id: "hInput"
                anchors.horizontalCenter: parent.horizontalCenter
                colorName: "H:"
                colorValue: colorFields.hValue
            }
            ColorInput {
                id: "sInput"
                anchors.horizontalCenter: parent.horizontalCenter
                colorName: "S:"
                colorValue: colorFields.sValue
            }
            ColorInput {
                id: "bInput"
                anchors.horizontalCenter: parent.horizontalCenter
                colorName: "B:"
                colorValue: colorFields.bValue
            }
        }

        // Just for little space between HSB and RGBA boxes
        Rectangle {
            width: parent.width
            height: 2
            color: "transparent"
        }
        */

        // R, G, B color values boxes
        Column {
            width: parent.width
            spacing: 4

            ColorInput {
                id: rInput
                colorName: "R:"
                colorValueText: colorFields.redValue
                minValue: 0
                maxValue: 255

                onColorValueTextChanged: {
                    paramObject ? paramObject.r = colorValueText : 255
                    // Test to adapt display of colorSlider in function of values enter in inputs
                    // cursorColorPosition = 120 * (rInput.colorValueText + gInput.colorValueText + bInput.colorValueText )/(3*255)
                }
            }

            ColorInput {
                id: gInput
                colorName: "G:"
                colorValueText: colorFields.greenValue
                minValue: 0
                maxValue: 255

                onColorValueTextChanged: {
                    paramObject ? paramObject.g = colorValueText : 255
                    // Test to adapt display of colorSlider in function of values enter in inputs
                    // cursorColorPosition = 120 * (rInput.colorValueText + gInput.colorValueText + bInput.colorValueText )/(3*255)
                }
            }

            ColorInput {
                id: bInput
                colorName: "B:"
                colorValueText: colorFields.blueValue
                minValue: 0
                maxValue: 255

                onColorValueTextChanged: {
                    paramObject ? paramObject.b = colorValueText : 255
                    // test to adapt display of colorSlider in function of values enter in inputs
                    // cursorColorPosition = 120 * (rInput.colorValueText + gInput.colorValueText + bInput.colorValueText )/(3*255)
                }
            }
        }
    }
}
