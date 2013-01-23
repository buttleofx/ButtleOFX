import QtQuick 1.1


Item {
    id: containerParamInt2D
    implicitWidth: 300
    implicitHeight: 30

    /*Container of the textInput*/
    Row{
        id: paramInt2DInputContainer
        spacing: 10

        /*Title of the paramInt */
        Text {
            id: paramInt2DTitle
            text: model.object.text + " : "
            color: "white"
        }

        /* First Input */
        Rectangle{
            height: 20
            width:40
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            TextInput{
                id: paramInt2DInput1
                text: model.object.value1
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 3
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                onAccepted: model.object.value1 = paramInt2DInput1.text
                validator: IntValidator{
                    bottom: model.object.minimum
                    top:  model.object.maximum
                }
            }
        }

        /* Second Input */
        Rectangle{
            height: 20
            width:40
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            TextInput{
                id: paramInt2DInput2
                text: model.object.value2
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 3
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                onAccepted: model.object.value2 = paramInt2DInput2.text
                validator: IntValidator{
                    bottom: model.object.minimum
                    top:  model.object.maximum
                }
            }
        }
    }

}
