import QtQuick 1.1

/*ParamDouble2D containts two input field*/

Item {
    id: containerParamDouble2D
    width: parent.width
    height: parent.height

    // Title of the paramDouble
    Text {
        id: paramDouble2DTitle
        width: 80
        text: model.object.text + " : "
        color: "white"
       // font.pointSize: 8
        anchors.top: parent.top
        anchors.verticalCenter: parent.verticalCenter
    }  

    /*Container of the two input field*/
     Rectangle{
        id: paramDouble2DInputContainer
        color: "#212121"
        border.width: 1
        border.color: "#111111"
        radius: 4

        anchors.left: paramDouble2DTitle.right
        anchors.leftMargin: 5

        /* First input */
        TextInput{
            id: paramDouble2Dinput1
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
            id: paramDouble2Dinput2
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

    }


}