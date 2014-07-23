import QtQuick 2.0

// An input field with a title
Row {
    property alias colorName: colorName.text
    property alias minValue: numValidator.bottom
    property alias maxValue: numValidator.top
    property alias decimals: numValidator.decimals

    // Property used to take or give the value of Input from ColorInputsRGBA
    property real valueInput

    // Used for the update of the current color
    property real newValueInput

    width: 80
    height: 14
    spacing: 4

    // Title of the color (R, G or B for example)
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

    // Input of the color
    Rectangle {
        width: 30
        height: parent.height
        radius: 2
        border.width: 1
        border.color: "#FF525255"
        color: "#333"
        clip: true

        TextInput {
            id: input
            anchors.leftMargin: 4
            anchors.topMargin: 0
            anchors.fill: parent
            font.pixelSize: 11
            maximumLength: 3
            focus: true
            selectByMouse: true
            color: "white"
            text: valueInput

            validator: DoubleValidator {
                id: numValidator
                // Default values
                bottom: 0; top: 255; decimals: 2
                notation: DoubleValidator.StandardNotation
            }

            onAccepted: {
                // Every time the user confirms the entry we save the value in newValueInput and we recup it in colorInputsRGBA.qml
                newValueInput = parseInt(input.text)
            }
        }
    }
}
