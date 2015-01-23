import QtQuick 2.0
import QuickMamba 1.0

// ParamDouble3D containts two input field
Item {
    id: containerParamDouble3D
    implicitWidth: 300
    implicitHeight: 60
    y: 10

    property variant paramObject: model.object

    // Is this param secret?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    // Container of the two input field
    Row {
        id: paramDouble3DInputContainer
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
                id: paramDouble3Dinput1
                textInput.text: paramObject.value1
                width: parent.width
                textInput.font.bold: paramObject.value1HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                textInput.selectByMouse: true

                minValue: paramObject.minimum1
                maxValue: paramObject.maximum1
                decimals: 5

                textInput.onAccepted: {
                    if (textInput.text <= paramObject.maximum1 && textInput.text >= paramObject.minimum1) {
                        paramObject.value1 = parseFloat(paramDouble3Dinput1.textInput.text)
                    } else {
                        textInput.text = paramObject.value1
                    }
                }

                textInput.onActiveFocusChanged: {
                    if (textInput.text <= paramObject.maximum1 && textInput.text >= paramObject.minimum1) {
                        paramObject.value1 = paramDouble3Dinput1.textInput.text
                    } else {
                        textInput.text = paramObject.value1
                    }
                }

                KeyNavigation.backtab: paramDouble3Dinput3
                KeyNavigation.tab: paramDouble3Dinput2
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
                id: paramDouble3Dinput2
                textInput.text: paramObject.value2
                width: parent.width
                textInput.font.bold: paramObject.value2HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                textInput.activeFocusOnPress: true
                textInput.selectByMouse: true

                minValue: paramObject.minimum2
                maxValue: paramObject.maximum2
                decimals: 5

                onQuickUpdate: textInput.text = quickValue

                onEditingFinished: paramObject.value2 = parseFloat(textInput.text)

                onAccepted: {
                    if (textInput.text <= paramObject.maximum2 && textInput.text >= paramObject.minimum2) {
                        paramObject.value2 = parseFloat(paramDouble3Dinput2.textInput.text)
                    } else {
                        textInput.text = paramObject.value2
                    }
                }

                onActiveFocusChanged: {
                    if (textInput.text <= paramObject.maximum2 && textInput.text >= paramObject.minimum2) {
                        paramObject.value2 = paramDouble3Dinput2.textInput.text
                    } else {
                        textInput.text = paramObject.value2
                    }
                }

                KeyNavigation.backtab: paramDouble3Dinput1
                KeyNavigation.tab: paramDouble3Dinput3
            }

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton

                onClicked: {
                    // Reinitialise value2 to its default value
                    paramObject.value2HasChanged = false
                    paramObject.value2 = paramObject.getDefaultValue2()
                }
            }
        }

        // Third input
        Rectangle {
            height: 35
            width: 60
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            QuickEditableNumberInput {
                id: paramDouble3Dinput3
                textInput.text: paramObject.value3
                width: parent.width
                textInput.font.bold: paramObject.value3HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                textInput.activeFocusOnPress: true
                textInput.selectByMouse: true

                minValue: paramObject.minimum3
                maxValue: paramObject.maximum3
                decimals: 5

                onQuickUpdate: textInput.text = quickValue

                onEditingFinished: paramObject.value3 = parseFloat(textInput.text)

                textInput.onAccepted: {
                    if (textInput.text <= paramObject.maximum3 && textInput.text >= paramObject.minimum3) {
                        paramObject.value3 = parseFloat(paramDouble3Dinput3.textInput.text)
                    } else {
                        textInput.text = paramObject.value3
                    }
                }

                textInput.onActiveFocusChanged: {
                    if (textInput.text <= paramObject.maximum3 && textInput.text >= paramObject.minimum3) {
                        paramObject.value3 = paramDouble3Dinput3.textInput.text
                    } else {
                        textInput.text = paramObject.value3
                    }
                }

                KeyNavigation.backtab: paramDouble3Dinput2
                KeyNavigation.tab: paramDouble3Dinput1
            }

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton

                onClicked: {
                    // Reinitialise value3 to its default value
                    paramObject.value3HasChanged = false
                    paramObject.value3 = paramObject.getDefaultValue3()
                }
            }
        }
    }
}
