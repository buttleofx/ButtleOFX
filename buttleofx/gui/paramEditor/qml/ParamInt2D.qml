import QtQuick 2.0

Item {
    id: containerParamInt2D
    implicitWidth: 300
    implicitHeight: 30
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
            height: 20
            width: 40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            TextInput {
                id: paramInt2DInput1
                text: paramObject.value1
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 3
                font.bold: paramObject.value1HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse: true

                onAccepted: {
                    if (acceptableInput) {
                        paramObject.value1 = paramInt2DInput1.text
                    }
                }

                onActiveFocusChanged: {
                    if (acceptableInput) {
                        paramObject.value1 = paramInt2DInput1.text
                    }
                }

                validator: IntValidator {
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
            height: 20
            width: 40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            TextInput {
                id: paramInt2DInput2
                text: paramObject.value2
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 3
                font.bold: paramObject.value2HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse: true

                onAccepted: {
                    if (acceptableInput) {
                        paramObject.value2 = paramInt2DInput2.text
                    }
                }

                onActiveFocusChanged: {
                    if (acceptableInput) {
                        paramObject.value2 = paramInt2DInput2.text
                    }
                }

                validator: IntValidator {
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
