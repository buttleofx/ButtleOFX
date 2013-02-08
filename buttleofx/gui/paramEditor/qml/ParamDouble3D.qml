import QtQuick 1.1

/*ParamDouble3D containts two input field*/

Item {
    id: containerParamDouble3D
    implicitWidth: 300
    implicitHeight: 30

    property variant paramObject: model.object

    /*Container of the two input field*/
     Row {
        id: paramDouble3DInputContainer
        spacing: 10

        // Title of the paramDouble
        Text {
            id: paramDouble3DTitle
            text: paramObject.text + " : "
            color: "white"
        }  

        /* First input */
        Rectangle {
            height: 20
            width:40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            TextInput {
                id: paramDouble3Dinput1
                text: paramObject.value1
                width: parent.width - 2
                anchors.left: parent.left
                anchors.leftMargin: 2
                anchors.rightMargin: 2
                anchors.verticalCenter: parent.verticalCenter
                color: activeFocus ? "white" : "grey"
                selectByMouse : true
                onAccepted: {
                    if(acceptableInput){
                        paramObject.value1 = paramDouble3Dinput1.text
                    }
                }
                onActiveFocusChanged: {
                    if(acceptableInput){
                        paramObject.value1 = paramDouble3Dinput1.text
                    }
                }
                validator: DoubleValidator{
                    bottom: paramObject.minimum1
                    top:  paramObject.maximum1
                }

                KeyNavigation.backtab: paramDouble3Dinput3
                KeyNavigation.tab: paramDouble3Dinput2
            }
        }

        /* Second input */
        Rectangle {
            height: 20
            width:40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            TextInput {
                id: paramDouble3Dinput2
                text: paramObject.value2
                width: parent.width - 2
                anchors.left: parent.left
                anchors.leftMargin: 2
                anchors.rightMargin: 2
                anchors.verticalCenter: parent.verticalCenter
                color: activeFocus ? "white" : "grey"
                activeFocusOnPress : true
                selectByMouse : true
                onAccepted: {
                    if(acceptableInput) {
                        paramObject.value2 = paramDouble3Dinput2.text
                    }
                }
                onActiveFocusChanged: {
                    if(acceptableInput) {
                        paramObject.value2 = paramDouble3Dinput2.text
                    }
                }
                validator: DoubleValidator{
                    bottom: paramObject.minimum2
                    top: paramObject.maximum2
                }

                KeyNavigation.backtab: paramDouble3Dinput1
                KeyNavigation.tab: paramDouble3Dinput3
            }
        }

        /* Third input */
        Rectangle {
            height: 20
            width:40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            TextInput{
                id: paramDouble3Dinput3
                text: paramObject.value3
                width: parent.width - 2
                anchors.left: parent.left
                anchors.leftMargin: 2
                anchors.rightMargin: 2
                anchors.verticalCenter: parent.verticalCenter
                color: activeFocus ? "white" : "grey"
                activeFocusOnPress : true
                selectByMouse : true
                onAccepted: {
                    if(acceptableInput) {
                        paramObject.value3 = paramDouble3Dinput3.text
                    }
                }
                onActiveFocusChanged: {
                    if(acceptableInput) {
                        paramObject.value3 = paramDouble3Dinput3.text
                    }
                }
                validator: DoubleValidator{
                    bottom: paramObject.minimum3
                    top: paramObject.maximum3
                }

                KeyNavigation.backtab: paramDouble3Dinput2
                KeyNavigation.tab: paramDouble3Dinput1
            }
        }
    }
}
