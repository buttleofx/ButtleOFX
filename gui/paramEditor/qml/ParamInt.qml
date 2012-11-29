import QtQuick 1.1

/*ParamInt is an input field*/

/*Container of the textInput*/
Rectangle{
    id: paramInt
    width: 30
    height: 20
    color: "#212121"
    border.width: 1
    border.color: "#111111"
    radius: 4

    /*Input field accepting only number between 0 and 255*/
    TextInput{
        id: input
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 5
        maximumLength: 3
        color: focus ? "white" : "grey"
        validator: IntValidator{bottom: 0; top: 255}
    }
    MouseArea{
        anchors.fill: parent
        onPressed: input.focus = true
    }
}