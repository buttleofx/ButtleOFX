import QtQuick 1.1

/*ParamDouble3D containts two input field*/

Item {
    id: containerParamDouble3D
    width: parent.width
    height: parent.height

    // Title of the paramDouble
    Text {
        id: paramDouble3DTitle
        width: 80
        text: model.object.text + " : "
        color: "white"
       // font.pointSize: 8
        anchors.top: parent.top
        anchors.verticalCenter: parent.verticalCenter
    }  

    /*Container of the two input field*/
     Rectangle{
        id: paramDouble3DInputContainer
        color: "#212121"
        border.width: 1
        border.color: "#111111"
        radius: 4

        anchors.left: paramDouble3DTitle.right
        anchors.leftMargin: 5

        /* First input */
        TextInput{
            id: paramDouble3Dinput1
            text: model.object.defaultValue1
            anchors.left: parent.left
            anchors.leftMargin: 5
            maximumLength: 10
            color: focus ? "white" : "grey"
            validator: DoubleValidator{
                bottom: model.object.minimum
                top:  model.object.maximum
            }
        }
        MouseArea{
            anchors.fill: parent
            onPressed: input.focus = true
        }

        /* Second input */
        TextInput{
            id: paramDouble3Dinput2
            text: model.object.defaultValue2
            anchors.left: parent.left
            anchors.leftMargin: 30
            maximumLength: 10
            color: focus ? "white" : "grey"
            validator: DoubleValidator{
                bottom: model.object.minimum
                top:  model.object.maximum
            }
        }
        MouseArea{
            anchors.fill: parent
            onPressed: input.focus = true
        }

        /* Third input */
        TextInput{
            id: paramDouble3Dinput3
            text: model.object.defaultValue3
            anchors.left: parent.left
            anchors.leftMargin: 55
            maximumLength: 10
            color: focus ? "white" : "grey"
            validator: DoubleValidator{
                bottom: model.object.minimum
                top:  model.object.maximum
            }
        }
        MouseArea{
            anchors.fill: parent
            onPressed: input.focus = true
        }

    }


}