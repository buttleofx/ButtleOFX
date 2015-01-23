import QtQuick 2.0
import QuickMamba 1.0

// ParamDouble2D containts two input field
Item {
    id: containerParamDouble2D
    implicitWidth: 300
    implicitHeight: 60
    y: 10

    property variant paramObject: model.object

    // Is this param secret?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    // Container of the two input field
    Row {
        id: paramDouble2DInputContainer
        spacing: 10

        // First input
        Rectangle {
            height: 35
            width: 60
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            QuickEditableNumberInput {
                id: paramDouble2Dinput1
                textInput.text: paramObject.value1
                width: parent.width
                textInput.font.bold: paramObject.value1HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                textInput.selectByMouse: true

                minValue: paramObject.minimum1
                maxValue: paramObject.maximum1
                decimals: 5

                onQuickUpdate: textInput.text = quickValue

                onEditingFinished: paramObject.value1 = parseFloat(textInput.text)

                textInput.onAccepted: {
                    if (textInput.text <= paramObject.maximum1 && textInput.text >= paramObject.minimum1) {
                        paramObject.value1 = parseFloat(paramDouble2Dinput1.textInput.text)
                    } else {
                        textInput.text = paramObject.value1
                    }
                }

                textInput.onActiveFocusChanged: {
                    if (textInput.text <= paramObject.maximum1 && textInput.text >= paramObject.minimum1) {
                        paramObject.value1 =  paramDouble2Dinput1.textInput.text
                    } else {
                        textInput.text = paramObject.value1
                    }
                }

                KeyNavigation.backtab: paramDouble2Dinput2
                KeyNavigation.tab: paramDouble2Dinput2
            }

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton

                onClicked: {
                    // Reinitialise value1 to its default value
                    paramObject.value1HasChanged = false
                    paramObject.value1 = paramObject.getDefaultValue1()
                }
            }
        }

        // Second input
        Rectangle {
            height: 35
            width: 60
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            QuickEditableNumberInput {
                id: paramDouble2Dinput2
                textInput.text: paramObject.value2
                width: parent.width
                color: activeFocus ? "white" : "grey"
                textInput.font.bold: paramObject.value2HasChanged ? true : false
                textInput.selectByMouse: true

                // validator provided by QuickEditableNumberInput
                minValue: paramObject.minimum2
                maxValue: paramObject.maximum2
                decimals: 5

                onQuickUpdate: textInput.text = quickValue

                onEditingFinished: paramObject.value2 = parseFloat(textInput.text)

                textInput.onAccepted: {
                    if (textInput.text <= paramObject.maximum2 && textInput.text >= paramObject.minimum2) {
                        paramObject.value2 = parseFloat(paramDouble2Dinput2.textInput.text)
                    } else {
                        textInput.text = paramObject.value2
                    }
                }

                textInput.onActiveFocusChanged: {
                    if (textInput.text <= paramObject.maximum2 && textInput.text >= paramObject.minimum2) {
                        paramObject.value1 = parseFloat(paramDouble2Dinput1.textInput.text)
                    } else {
                        textInput.text = paramObject.value2
                    }
                }


            }

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton

                onClicked: {
                    // Reinitialise the value of value2 to its default value
                    paramObject.value2HasChanged = false
                    paramObject.value2 = paramObject.getDefaultValue2()
                }
            }

            // TODO : fix change input not working
            KeyNavigation.backtab: paramDouble2Dinput1
            KeyNavigation.tab: paramDouble2Dinput1
        }
    }
}
