import QtQuick 1.1

/*ParamInt is an input field*/


Item {
    id: containerParamInt
    width: parent.width
    height:parent.height

    /*Title of the paramInt */
    Text {
        id: paramIntTitle
        width: 80
        text: model.object.text + " : "
        color: "white"
       // font.pointSize: 8
        anchors.top: parent.top
        anchors.verticalCenter: parent.verticalCenter
    }


    /*Container of the textInput*/
    Rectangle{
        id: paramIntInputContainer
        color: "#212121"
        border.width: 1
        border.color: "#111111"
        radius: 4

        anchors.left: paramIntTitle.right
        anchors.leftMargin: 5


        /*Input field accepting only number between 0 and 255*/
        TextInput{
            id: paramIntInput
            text: model.object.defaultValue
            anchors.left: parent.left
            anchors.leftMargin: 5
            maximumLength: 3
            color: focus ? "white" : "grey"
            validator: IntValidator{
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
