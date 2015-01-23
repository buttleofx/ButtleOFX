import QtQuick 2.0
import QuickMamba 1.0

Item {
    id: containerParamInt2D
    implicitWidth: 300
    implicitHeight: 60
    y: 10

    property variant paramObject: model.object

    // Is this param secret?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    // Container of the textInput
    Row {
        id: paramInt2DInputContainer
        spacing: 10

        // First Input
        Rectangle {
            height: 35
            width: 60
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            QuickEditableNumberInput {
                id: paramInt2DInput1
                textInput.text: paramObject.value1
                textInput.font.bold: paramObject.value1HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                width: parent.width
                textInput.selectByMouse: true

                minValue: paramObject.minimum1
                maxValue: paramObject.maximum1
                decimals: 0

                onQuickUpdate: textInput.text = quickValue

                onEditingFinished: paramObject.value1 = parseInt(textInput.text)

                textInput.onAccepted: {
                    if (textInput.text <= maxValue && textInput.text >= minValue) {
                        paramObject.value1 = parseInt(paramInt2DInput1.textInput.text)
                    }
                }

                textInput.onActiveFocusChanged: {
                    if (textInput.text <= maxValue && textInput.text >= minValue) {
                        paramObject.value1 = paramInt2DInput1.textInput.text
                    }
                }

                textInput.validator: IntValidator {
                    bottom: model.object.minimum1
                    top:  model.object.maximum1
                }

                KeyNavigation.backtab: paramInt2DInput2
                KeyNavigation.tab: paramInt2DInput2
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

        // Second Input
        Rectangle {
            height: 35
            width: 60
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            QuickEditableNumberInput {
                id: paramInt2DInput2
                textInput.text: paramObject.value2
//                textInput.maximumLength: 3
                textInput.font.bold: paramObject.value2HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                width: parent.width
                textInput.selectByMouse: true

                minValue: paramObject.minimum2
                maxValue: paramObject.maximum2
                decimals: 0

                onQuickUpdate: textInput.text = quickValue

                onEditingFinished: paramObject.value2 = parseInt(textInput.text)

                textInput.onAccepted: {
                    if (textInput.text <= maxValue && textInput.text >= minValue) {
                        paramObject.value2 = parseInt(paramInt2DInput2.textInput.text)
                    }
                }

                textInput.onActiveFocusChanged: {
                    if (textInput.text <= maxValue && textInput.text >= minValue) {
                        paramObject.value2 = paramInt2DInput2.textInput.text
                    }
                }

                textInput.validator: IntValidator {
                    bottom: model.object.minimum2
                    top:  model.object.maximum2
                }

                KeyNavigation.backtab: paramInt2DInput1
                KeyNavigation.tab: paramInt2DInput1
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
    }
}
