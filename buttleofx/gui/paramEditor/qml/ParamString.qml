import QtQuick 1.1

/*ParamString is an input field*/

Item {
    id: containerParamString
    implicitWidth: 300
    implicitHeight: 30

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
            implicitWidth: 200
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
                selectByMouse : true
                color: activeFocus ? "white" : "grey"
                onAccepted: model.object.setDefaultValue(parent.text)
            }
        }
    }
}
