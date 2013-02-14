import QtQuick 1.1
import "ColorFunctions.js" as ColorFunctions

// group of inputs
Rectangle {
    id: colorFields
    implicitWidth: 80
    implicitHeight: 200
    color: "black"

    // properties used to change the text int the boxes r, g, b and h, s, b
    property color currentColor: "white"
    property string alphaColorText: "#FFFFFFFF"
    property int redValue : 0
    property int greenValue : 0 
    property int blueValue : 0
    property real hValue: 0
    property real sValue: 0
    property real bValue: 0
    property int alphaValue: 0

    // column containing the inputs colors 
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
            Rectangle{
                width: parent.width
                height: parent.height
                border.width: 1
                border.color: "black"
                color: colorFields.currentColor
            }
            MouseArea{
                anchors.fill: parent
            } 
        }

        // rectangle displaying the current alphacolor under the text form #AA112233
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
                onTextChanged:{
                    paramObject.r = colorFields.redValue
                    paramObject.g = colorFields.greenValue
                    paramObject.b = colorFields.blueValue 
                    paramObject.a = colorFields.alphaValue
                }
            }
        }

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
            }
            ColorInput {
                id: gInput
                colorName: "G:"
                colorValueText: colorFields.greenValue
                minValue: 0
                maxValue: 255
            }
            ColorInput {
                id: bInput
                colorName: "B:"
                colorValueText: colorFields.blueValue 
                minValue: 0 
                maxValue: 255
            }
            // alpha value box
            ColorInput {
                id: aInput
                colorName: "A:";
                colorValueText: colorFields.alphaValue
                minValue: 0
                maxValue: 255
            }
        }
    }
}
