import QtQuick 2.0

// ParamDouble2D containts two input field
Item {
    id: containerParamDouble2D
    implicitWidth: 300
    implicitHeight: 30
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
            height: 20
            width: 40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            TextInput {
                id: paramDouble2Dinput1
                text: paramObject.value1
                width: parent.width - 2
                anchors.left: parent.left
                anchors.leftMargin: 2
                anchors.rightMargin: 2
                anchors.verticalCenter: parent.verticalCenter
                font.bold: paramObject.value1HasChanged ? true : false
                color: activeFocus ? "white" : "grey"
                selectByMouse: true

                onAccepted: {
                    if (text <= paramObject.maximum1 && text >= paramObject.minimum1) {
                        paramObject.value1 = paramDouble2Dinput1.text
                    } else {
                        text = paramObject.value1
                    }
                }

                onActiveFocusChanged: {
                    if (text <= paramObject.maximum1 && text >= paramObject.minimum1) {
                        paramObject.value1 = paramDouble2Dinput1.text
                    } else {
                        text = paramObject.value1
                    }
                }

                /*
                validator: DoubleValidator {
                    bottom: paramObject.minimum1
                    top:  paramObject.maximum1
                }
                */

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
            height: 20
            width: 40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            clip: true

            TextInput {
                id: paramDouble2Dinput2
                text: paramObject.value2
                width: parent.width - 2
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                anchors.leftMargin: 2
                anchors.rightMargin: 2
                color: activeFocus ? "white" : "grey"
                font.bold: paramObject.value2HasChanged ? true : false
                selectByMouse: true

                onAccepted: {
                    if (text <= paramObject.maximum2 && text >= paramObject.minimum2) {
                        paramObject.value2 = paramDouble2Dinput2.text
                    } else {
                        text = paramObject.value2
                    }
                }

                onActiveFocusChanged: {
                    if (text <= paramObject.maximum2 && text >= paramObject.minimum2) {
                        paramObject.value1 = paramDouble2Dinput1.text
                    } else {
                        text = paramObject.value2
                    }
                }

                /*
                validator: DoubleValidator {
                    bottom: paramObject.minimum2
                    top: paramObject.maximum2
                }
                */

                KeyNavigation.backtab: paramDouble2Dinput1
                KeyNavigation.tab: paramDouble2Dinput1
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
        }
    }
}
