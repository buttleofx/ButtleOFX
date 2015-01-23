import QtQuick 2.0
import QuickMamba 1.0

Item {
    id: paramInt
    implicitWidth: 300
    implicitHeight: 70
    y: 40

    property variant paramObject: model.object

    // Is this param secret?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    // To fix binding loops
    property bool mousePressed: false

    function updateXcursor() {
        return ((sliderInput.textInput.text - paramObject.minimum) * barSlider.width) / (paramObject.maximum - paramObject.minimum)
    }

    function updateTextValue() {
        return (cursorSlider.x * (paramObject.maximum - paramObject.minimum)) / barSlider.width + paramObject.minimum
    }

    Row {
        spacing: 10

        // The min value (at the beginning of the bar slider)
        Text {
            id: minValue
            text: paramObject.minimum
            font.pointSize: 8
            color: "white"
            y: 5
        }

        // The slider
        Item {
            width: 100
            height: parent.height

            // Current value
           QuickEditableNumberInput {
                id: sliderInput
                width: barSlider.width
                y: -30
                textInput.horizontalAlignment: TextInput.AlignHCenter
                textInput.text: paramObject.value
                textInput.font.family: "Helvetica"
                textInput.font.pointSize: 8
                textInput.font.bold: paramObject.hasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                // activeFocusOnPress: true
               textInput.selectByMouse: true

               // Validator include in QuickEditableNumberInput element
               minValue: paramObject.minimum
               maxValue: paramObject.maximum
               decimals: 0

               onQuickUpdate: {
                   textInput.text = quickValue
                   cursorSlider.x = updateXcursor()
                }

               onEditingFinished: {
                   //parse QtString to Int
                   paramObject.value = textInput.text
               }

               textInput.onAccepted: {
                   if (sliderInput.textInput.text <= paramObject.maximum && sliderInput.textInput.text >= paramObject.minimum) {
                    cursorSlider.x = updateXcursor()
                    paramObject.value = textInput.text
                    paramObject.pushValue(paramObject.value)

               }}

                Component.onCompleted: {
                    cursorSlider.x = updateXcursor()
                }

                textInput.onTextChanged: {
                    if (!mousePressed) {
                        if (sliderInput.textInput.text <= paramObject.maximum && sliderInput.textInput.text >= paramObject.minimum) {
                            cursorSlider.x = updateXcursor()
                        }
                }
                }

                textInput.onActiveFocusChanged: {
                    paramObject.value = updateTextValue()
                    paramObject.pushValue(paramObject.value)

                }

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.RightButton

                    onClicked: {
                        // Reinitialise the param to its default value
                        paramObject.hasChanged = false
                        paramObject.value = paramObject.getDefaultValue()
                        paramObject.pushValue(paramObject.value)
                    }
                }
            }

            // Bar slider: one grey, one white
            Rectangle {
                id: barSlider
                width: 100
                height: 2
                y: 8

                Rectangle {
                    id: whiteBar
                    x: 0
                    width: cursorSlider.x
                    height: parent.height
                    color: "#00b2a1"
                }

                Rectangle {
                    id: greyBar
                    x: cursorSlider.x
                    width: barSlider.width - whiteBar.width
                    height: parent.height
                    color: "grey"
                }
            }

            // Cursor slider (little white rectangle)
            Rectangle {
                id: cursorSlider
                y: 4
                height: 10
                width: 5
                radius: 1
                color: "white"

                MouseArea {
                    anchors.fill: parent
                    drag.target: parent
                    drag.axis: Drag.XAxis
                    drag.minimumX: 0 // cursorSlider.width / 2
                    drag.maximumX: barSlider.width // cursorSlider.width / 2
                    // Allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
                    anchors.margins: -10

                    onPressed: {
                        mousePressed = true
                        // Take the focus
                        paramInt.forceActiveFocus()
                    }

                    onReleased: {
                        paramObject.value = updateTextValue()
                        paramObject.pushValue(paramObject.value)
                        mousePressed = false
                    }
                }

                onXChanged: {
                    if (mousePressed) {
                        paramObject.value = updateTextValue()
                    }
                }
            }
        }

        // The max value (at the end of the bar slider)
        Text {
            id: maxValue
            text: paramObject.maximum
            font.pointSize: 8
            color: "white"
            y: 5
        }
    }
}
