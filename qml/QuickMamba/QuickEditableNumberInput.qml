import QtQuick 2.2
import QtQuick.Layouts 1.1

Rectangle {
    id: root

    property alias textInput: textInput

    property string upArrow: "assets/img/arrows/arrow2.png"
    property string upArrowHover: "assets/img/arrows/arrow2_hover.png"
    property string downArrow: "assets/img/arrows/arrow.png"
    property string downArrowHover: "assets/img/arrows/arrow_hover.png"
    property color cursorColor : "#00B2A1"

    // Default style
    color: "#212121"
    border.width: 2
    border.color: "#333"
    radius: 3

    signal quickUpdate(var text)

    QtObject {
        id: m
        property real step: 1
    }

    // stepSign is the factor of step (eg: 1 will increment, -1 will decrement)
    function updateValue(stepSign) {
        stepSign = typeof stepSign !== 'undefined' ? stepSign : 1

        // Remember cursor position to stay in same place after text update (because we lose it when property text changes)
        var oldCursorPos = textInput.cursorPosition

        var text = textInput.text
        var comaPosition = text.indexOf(".")

        var increment = 1

        /* Calcul the increment value in function of the right digit to the cursor
         * e.g. 12.2|32 : increment is then 0.01
         * If cursor is left to coma or negative sign, increment is just default value (1)
        */
        if (!(parseFloat(textInput.text) < 0 && oldCursorPos == 0)) {
            if (comaPosition == -1)
                increment = Math.pow(10, text.length - oldCursorPos - 1)
            else if (oldCursorPos < comaPosition)
                increment = Math.pow(10, comaPosition - oldCursorPos - 1)
            else if (oldCursorPos > comaPosition)
                increment = Math.pow(10, comaPosition - oldCursorPos)
        }

        var newValue = parseFloat(textInput.text) + stepSign * increment

        // Adjust cursor position when the old number is negative and the new one is positive
        if (newValue >= 0 && parseFloat(textInput.text) < 0)
            oldCursorPos--

        root.quickUpdate(newValue)
        textInput.cursorPosition = oldCursorPos
    }

    MouseArea {
        anchors.fill: parent

        onWheel: {
            if (wheel.angleDelta.y >= 0)
                root.updateValue(1)
            else
                root.updateValue(-1)
        }
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: root.border.width + 4
        TextInput {
            id: textInput
            selectByMouse: true

            Layout.fillWidth: true

            // Text Input is dynamically aligned with arrows
            horizontalAlignment: TextInput.AlignHCenter
            clip: true

            validator: DoubleValidator {
                locale: "en"
            }

            // Default style
            color: "white"
            cursorDelegate: BlinkCursor {
                color: root.cursorColor
                visible: textInput.focus
            }
            selectionColor: Qt.rgba(1, 1, 1, 0.2)

            Keys.onPressed: {
                switch (event.key) {
                case Qt.Key_Up:
                    root.updateValue(1)
                    event.accepted = true
                    break
                case Qt.Key_Down:
                    root.updateValue(-1)
                    event.accepted = true
                    break
                }
            }
        }

        ColumnLayout {
            id: arrows

            // Width of column must be equal to the biggest image width
            Layout.preferredWidth: upArrow.width > downArrow.width ? upArrow.width : downArrow.width
            Layout.fillHeight: true
            spacing: 10

            Image {
                id: upArrow
                source: root.upArrow

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true

                    onEntered: upArrow.source = root.upArrowHover
                    onExited: upArrow.source = root.upArrow

                    onClicked: root.updateValue(1)
                }
            }

            Image {
                id: downArrow
                source: root.downArrow

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true

                    onEntered: downArrow.source = root.downArrowHover
                    onExited: downArrow.source = root.downArrow

                    onClicked: root.updateValue(-1)
                }
            }
        }
    }
}
