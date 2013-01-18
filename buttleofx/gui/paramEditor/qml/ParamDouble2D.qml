import QtQuick 1.1

/*ParamDouble2D containts two input field*/

Item {
    id: containerParamDouble2D
    implicitWidth: 300
    implicitHeight: 30

    /*Container of the two input field*/
     Row{
        id: paramDouble2DInputContainer
        spacing : 10

        // Title of the paramDouble
        Text {
            id: paramDouble2DTitle
            width: 80
            text: model.object.text + " : "
            color: "white"
            anchors.top: parent.top
            anchors.verticalCenter: parent.verticalCenter
        }

        /* First input */
        Rectangle{
            height: 20
            width:40
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            TextInput{
                id: paramDouble2Dinput1
                text: model.object.value1
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 5
                color: activeFocus ? "white" : "grey"
                width: 40
                activeFocusOnPress : true
                selectByMouse : true
                onAccepted: model.object.value1 = paramDouble2Dinput1.text
                validator: DoubleValidator{
                    bottom: model.object.minimum
                    top:  model.object.maximum
                }
            }
        }

        /* Second input */
        Rectangle{
            height: 20
            width:40
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            TextInput{
                id: paramDouble2Dinput2
                text: model.object.value2
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 5
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                onAccepted: model.object.value2 = paramDouble2Dinput2.text
                validator: DoubleValidator{
                    bottom: model.object.minimum
                    top:  model.object.maximum
                }
            }
        }
    }
}