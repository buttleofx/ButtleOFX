import QtQuick 1.1

/*ParamDouble is an input field*/
Item {
    id: containerParamDouble
    implicitWidth: 300
    implicitHeight: 30


    /*Container of the textInput*/
    Row {
        id: paramDoubleInputContainer
        spacing: 10

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

        /*Input field accepting only float between 2^31-1 and 2^31*/
        Rectangle{
            height: 20
            width:40
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            TextInput{
                id: paramDoubleinput
                text: model.object.defaultValue
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 5
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                validator: DoubleValidator{
                    bottom: model.object.minimum
                    top:  model.object.maximum
                }
                onAccepted: model.object.setDefaultValue(parent.text)
            }
        }
    }


}

