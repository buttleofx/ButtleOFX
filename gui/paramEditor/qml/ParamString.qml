import QtQuick 1.1

/*ParamString is an input field*/

Item {
    id: containerParamString
    width: parent.width
    height: 20

    /*Title of the paramInt */
    Text {
        id: paramStringTitle
        width: 60
        text: model.object.stringType
        color: "white"
        //font.pointSize: 8
        anchors.top: parent.top
        anchors.verticalCenter: parent.verticalCenter
    }

    /*Container of the textInput*/
    Rectangle{
        id: paramStringInputContainer
        width: 100
        color: "#212121"
        border.width: 1
        border.color: "#111111"
        radius: 4

        anchors.left: paramStringTitle.right
        anchors.leftMargin: 5

        /*Input field limited to 50 characters*/
        TextInput{
            id: paramStringInput
            text: model.object.defaultValue
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 5
            maximumLength: 50
            color: focus ? "white" : "grey"
        }
        MouseArea{
            anchors.fill: parent
            onPressed: input.focus = true
        }
    }

}
