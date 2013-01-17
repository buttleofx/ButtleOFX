import QtQuick 1.1

/*ParamString is an input field*/

Item {
    id: containerParamString
    width: parent.width
    height: parent.height


    /*Container of the textInput*/
    Row{
        id: paramStringInputContainer
        spacing: 10

        /*Title of the paramInt */
        Text {
            id: paramStringTitle
            width: 80
            text: model.object.stringType + " : "
            color: "white"
            //font.pointSize: 8
            anchors.top: parent.top
            anchors.verticalCenter: parent.verticalCenter
        }

        /*Input field limited to 50 characters*/
        Rectangle{
            height: 20
            width:200
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            TextInput{
                id: paramStringInput
                text: model.object.defaultValue
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 100
                activeFocusOnPress : true
                selectByMouse : true
                color: focus ? "white" : "grey"
                onAccepted: model.object.setDefaultValue(parent.text)
            }
        }
    }
}
