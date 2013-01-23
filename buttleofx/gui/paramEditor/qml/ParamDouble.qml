import QtQuick 1.1

/*ParamDouble is an input field*/
Item {
    id: containerParamDouble
    implicitWidth: 300
    implicitHeight: 30

    property variant paramObject: model.object

    /*Container of the textInput*/
    Row {
        id: paramDoubleInputContainer
        spacing: 10

        // Title of the paramDouble
        Text {

            id: paramDoubleTitle
            text: paramObject.text + " : "
            color: "white"
        }

        /* Input field */
        Rectangle{
            height: 20
            width:40

            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            TextInput{
                id: paramDoubleInput
                text: paramObject.value
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 5
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                validator: DoubleValidator{
                    bottom: paramObject.minimum
                    top:  paramObject.maximum
                }
                onAccepted: paramObject.value = paramDoubleInput.text
            }
        }
    }


}

