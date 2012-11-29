import QtQuick 1.1

/*ParamDouble is an input field*/

/*Container of the textInput*/
Rectangle{
	id: paramDouble
    width: 90
    height: 20
    color: "#212121"
    border.width: 1
    border.color: "#111111"
    radius: 4

    /*Input field accepting only float between 2^31-1 and 2^31*/
    TextInput{
        id: input
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 5
        maximumLength: 10
        color: focus ? "white" : "grey"
        validator: DoubleValidator{bottom: -2147483647; decimals: 20; top: 2147483648}
    }
    MouseArea{
        anchors.fill: parent
        onPressed: input.focus = true
    }
}