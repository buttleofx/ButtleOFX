import QtQuick 1.1

/*ParamDouble is an input field*/

Item {
    id: containerParamDouble
    width: parent.width
    height: parent.height

    // Title of the paramDouble
    Text {
        id: paramDoubleTitle
        width: 80
        text: model.object.text + " : "
        color: "white"
       // font.pointSize: 8
        anchors.top: parent.top
        anchors.verticalCenter: parent.verticalCenter
    }

    /*Container of the textInput*/
    Rectangle{
        id: paramDoubleInputContainer
        color: "#212121"
        border.width: 1
        border.color: "#111111"
        radius: 4

        anchors.left: paramDoubleTitle.right
        anchors.leftMargin: 5

        /*Input field accepting only float between 2^31-1 and 2^31*/
        TextInput{
            id: paramDoubleinput
            text: model.object.defaultValue
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
    }


}

