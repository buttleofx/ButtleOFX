import QtQuick 1.1

// an input field with a title
Row {
    property alias  colorName: colorName.text
    property alias  colorValueText: colorValue.text
    property alias  minValue: numValidator.bottom
    property alias  maxValue: numValidator.top
    property alias  decimals: numValidator.decimals
    // test for enter colors values in inputs and adapt display
    property real cursorPositionInput: 255

    width: 80
    height: 14
    spacing: 4
    // title of the color (R, G or B for example)
    Text {
        id: colorName
        width: 18
        height: parent.height
        color: "white"
        font.pixelSize: 11
        font.bold: true
        horizontalAlignment: Text.AlignRight
        verticalAlignment: Text.AlignBottom
        anchors.bottomMargin: 3
        text: "R"
    }
    //input of the color
    Rectangle {
        width: 30
        height: parent.height
        radius: 2
        border.width: 1
        border.color: "#FF525255"
        color: "transparent"
        clip: true
        TextInput {
            id: colorValue
            anchors.leftMargin: 4
            anchors.topMargin: 0 
            anchors.fill: parent
            font.pixelSize: 11            
            maximumLength: 3
            focus: true
            selectByMouse: true
            color: "white"
            validator: DoubleValidator {
                id: numValidator
                //default values
                bottom: 0; top: 255; decimals: 2
                notation: DoubleValidator.StandardNotation
            }
            onAccepted: {
                cursorPositionInput = colorValue.text
                console.log(cursorPositionInput)
            }
        }
    }
}

