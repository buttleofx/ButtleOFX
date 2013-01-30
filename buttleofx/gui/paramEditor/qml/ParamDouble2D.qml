import QtQuick 1.1

/*ParamDouble2D containts two input field*/

Item {
    id: containerParamDouble2D
    implicitWidth: 300
    implicitHeight: 30

    property variant paramObject: model.object

    /*Container of the two input field*/
     Row{
        id: paramDouble2DInputContainer
        spacing : 10

        // Title of the paramDouble
        Text {
            id: paramDouble2DTitle
            text: paramObject.text + " : "
            color: "white"
        }

        /* First input */
        Rectangle{
            height: 20
            width:40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            TextInput{
                id: paramDouble2Dinput1
                text: paramObject.value1
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 5
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                onAccepted: paramObject.value1 = paramDouble2Dinput1.text
                onActiveFocusChanged: paramObject.value1 = paramDouble2Dinput1.text
                validator: DoubleValidator{
                    bottom: paramObject.minimum1
                    top:  paramObject.maximum1
                }
            }
        }

        /* Second input */
        Rectangle{
            height: 20
            width:40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            TextInput{
                id: paramDouble2Dinput2
                text: paramObject.value2
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 5
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                onAccepted: paramObject.value2 = paramDouble2Dinput2.text
                onActiveFocusChanged: paramObject.value2 = paramDouble2Dinput2.text
                validator: DoubleValidator{
                    bottom: paramObject.minimum2
                    top: paramObject.maximum2
                }
            }
        }
    }
}