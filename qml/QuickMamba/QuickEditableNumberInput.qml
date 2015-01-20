import QtQuick 2.2
import QtQuick.Layouts 1.1

Rectangle {
    id: root

    property alias textInput: textInput

    property string upArrow: "assets/img/arrows/arrow2.png"
    property string upArrowHover: "assets/img/arrows/arrow2_hover.png"
    property string downArrow: "assets/img/arrows/arrow.png"
    property string downArrowHover: "assets/img/arrows/arrow_hover.png"

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

        var step = 1

        // No selection
        // Calcul step in function of cursor position, if cursor is before sign - step is just 1
        if (!(parseFloat(textInput.text) < 0 && oldCursorPos == 0)) {
            if (comaPosition == -1)
                step = Math.pow(10, text.length - oldCursorPos - 1)
            else if (oldCursorPos < comaPosition)
                step = Math.pow(10, comaPosition - oldCursorPos - 1)
            else if (oldCursorPos > comaPosition)
                step = Math.pow(10, comaPosition - oldCursorPos)
        }

        var newValue = parseFloat(textInput.text) + stepSign * step
        // Fix problem when changing sign, we must correct cursor position
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


    TextInput {
        id: textInput
        selectByMouse: true

        // Text Input is dynamically aligned with arrows
        anchors.left: parent.left
        anchors.right: arrows.left
        anchors.rightMargin: 2
        anchors.leftMargin: root.border.width
        anchors.verticalCenter: parent.verticalCenter
        horizontalAlignment: TextInput.AlignHCenter
        clip: true

        validator: DoubleValidator {
            locale: "en"
        }

        // Default style
        color: "white"
        cursorDelegate: BlinkCursor { }
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


    Item {
        id: arrows

        width:  upArrow.width > downArrow.width ? upArrow.width + 4 : downArrow.width + 4
        height: parent.height
        anchors.right: parent.right
        anchors.rightMargin: 2 + root.border.width

        Image {
            id: upArrow
            source: root.upArrow

            anchors.bottom: parent.verticalCenter
            anchors.bottomMargin: 6
            anchors.horizontalCenter: parent.horizontalCenter

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

            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.verticalCenter
            anchors.topMargin: 6

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
