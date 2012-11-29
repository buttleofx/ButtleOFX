import QtQuick 1.1

/*ParamString is an input field*/

/*Container of the textInput*/
Rectangle{
    id: param
    width: 200
    height: 20
    color: "#212121"
    border.width: 1
    border.color: "#111111"
    radius: 4

    /*Input field limited to 50 characters*/
    TextInput{
        id: input
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