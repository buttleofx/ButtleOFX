import QtQuick 2.0

// ParamDouble3D containts three input field
Item {
    id: containerParamDouble3D
    implicitWidth: 300
    implicitHeight: 30
    y: 10

    property variant paramObject: model.object

    // Is this param secret?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    //Container of the two input field
    Row {
        id: paramDouble3DInputContainer
        spacing: 10

        // Title of the paramDouble
        Text {
            id: paramDouble3DTitle
            text: paramObject.text + " : "
            color: "white"
            // If param has been modified, set the title font to bold
            font.bold: (paramObject.value1HasChanged || paramObject.value2HasChanged || paramObject.value3HasChanged) ? true : false

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton

                // Reinitialise the values of the params
                onClicked: {
                    paramObject.value1HasChanged = false
                    paramObject.value2HasChanged = false
                    paramObject.value3HasChanged = false
                    paramObject.value1 = paramObject.getDefaultValue1()
                    paramObject.value2 = paramObject.getDefaultValue2()
                    paramObject.value3 = paramObject.getDefaultValue3()
                }
            }
        }

        // First input
        Rectangle {
            height: 20
            width: 40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            TextInput {
                id: paramDouble3Dinput1
                text: paramObject.value1
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 5
                font.bold: paramObject.value1HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                width: 40
                activeFocusOnPress: true
                selectByMouse: true

                onAccepted: {
                    if (acceptableInput) {
                        paramObject.value1 = paramDouble3Dinput1.text
                    }
                }

                onActiveFocusChanged: {
                    if (acceptableInput) {
                        paramObject.value1 = paramDouble3Dinput1.text
                    }
                }

                validator: IntValidator {
                    bottom: paramObject.minimum1
                    top:  paramObject.maximum1
                }

                KeyNavigation.backtab: paramInt2DInput3
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

        // Second input
        Rectangle {
            height: 20
            width: 40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            TextInput {
                id: paramDouble3Dinput2
                text: paramObject.value2
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 5
                font.bold: paramObject.value2HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse: true

                onAccepted: {
                    if (acceptableInput) {
                        paramObject.value2 = paramDouble3Dinput2.text
                    }
                }

                onActiveFocusChanged: {
                    if (acceptableInput) {
                        paramObject.value2 = paramDouble3Dinput2.text
                    }
                }

                validator: IntValidator {
                    bottom: paramObject.minimum2
                    top: paramObject.maximum2
                }

                KeyNavigation.backtab: paramInt2DInput1
                KeyNavigation.tab: paramInt2DInput3
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
            height: 20
            width: 40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            TextInput {
                id: paramDouble3Dinput3
                text: paramObject.value3
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 5
                font.bold: paramObject.value3HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse: true

                onAccepted: {
                    if (acceptableInput) {
                        paramObject.value3 = paramDouble3Dinput3.text
                    }
                }

                onActiveFocusChanged: {
                    if (acceptableInput) {
                        paramObject.value3 = paramDouble3Dinput3.text
                    }
                }

                validator: IntValidator {
                    bottom: paramObject.minimum3
                    top: paramObject.maximum3
                }

                KeyNavigation.backtab: paramInt2DInput2
                KeyNavigation.tab: paramInt2DInput1
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
