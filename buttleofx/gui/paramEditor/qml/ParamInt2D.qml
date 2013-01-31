import QtQuick 1.1


Item {
    id: containerParamInt2D
    implicitWidth: 300
    implicitHeight: 30

    property variant paramObject: model.object

    /*Container of the textInput*/
    Row {
        id: paramInt2DInputContainer
        spacing: 10

        /*Title of the paramInt */
        Text {
            id: paramInt2DTitle
            text: paramObject.text + " : "
            color: "white"
        }

        /* First Input */
        Rectangle {
            height: 20
            width:40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            TextInput {
                id: paramInt2DInput1
                text: paramObject.value1
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 3
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                onAccepted: {
                    if(acceptableInput) {
                        paramObject.value1 = paramInt2DInput1.text
                    }
                }
                onActiveFocusChanged: {
                    if(acceptableInput) {
                        paramObject.value1 = paramInt2DInput1.text
                    }
                }
                validator: IntValidator {
                    bottom: model.object.minimum1
                    top:  model.object.maximum1
                }

                KeyNavigation.backtab: paramInt2DInput2
                KeyNavigation.tab: paramInt2DInput2
            }
        }

        /* Second Input */
        Rectangle {
            height: 20
            width:40
            color: "#343434"
            border.width: 1
            border.color: "#444"
            radius: 3
            TextInput{
                id: paramInt2DInput2
                text: paramObject.value2
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 3
                color: activeFocus ? "white" : "grey"
                width: 40
                selectByMouse : true
                onAccepted: {
                    if(acceptableInput) {
                        paramObject.value2 = paramInt2DInput2.text
                    }
                }
                onActiveFocusChanged: {
                    if(acceptableInput) {
                        paramObject.value2 = paramInt2DInput2.text
                    }
                }
                validator: IntValidator {
                    bottom: model.object.minimum2
                    top:  model.object.maximum2
                }

                KeyNavigation.backtab: paramInt2DInput1
                KeyNavigation.tab: paramInt2DInput1
            }
        }
    }

}
