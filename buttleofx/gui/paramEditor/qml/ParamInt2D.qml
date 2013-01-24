import QtQuick 1.1


Item {
    id: containerParamInt2D
    implicitWidth: 300
    implicitHeight: 30

    property variant paramObject: model.object

    /*Container of the textInput*/
    Row{
        id: paramInt2DInputContainer
        spacing: 10

        /*Title of the paramInt */
        Text {
            id: paramInt2DTitle
            text: paramObject.text + " : "
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
                text: paramObject.maximum
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 3
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                onAccepted: paramObject.value1 = paramInt2DInput1.text
                validator: IntValidator{
<<<<<<< HEAD
                    bottom: paramObject.minimum
                    top:  paramObject.maximum
=======
                    bottom: model.object.minimum1
                    top:  model.object.maximum1
>>>>>>> 389b39d7e3b3f39c0f0d3c6c50a9cba7fd04857a
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
                text: paramObject.maximum
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 3
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                onAccepted: paramObject.value2 = paramInt2DInput2.text
                validator: IntValidator{
<<<<<<< HEAD
                    bottom: paramObject.minimum
                    top:  paramObject.maximum
=======
                    bottom: model.object.minimum2
                    top:  model.object.maximum2
>>>>>>> 389b39d7e3b3f39c0f0d3c6c50a9cba7fd04857a
                }
            }
        }
    }

}
