import QtQuick 1.1

/*ParamBoolean is a radio button*/

/*Container of the radio button*/

Item{
    width: 30
    height: 20
    property alias title: paramTitle.text

    /*Title of the param*/
    Text {
        id: paramTitle
        text: "undefined"
        color: "white"
        font.pointSize: 8
    }

    /*Black circle where we can click*/
    Rectangle {
        anchors.left: paramTitle.right
        anchors.leftMargin: 5
        id: circle
        width: 15
        height: width
        radius : width * 0.5
        color: "#999999"

        /*Little white circle which appears in white inside the circle when we click*/
        Rectangle{
            id: interiorCircle
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            width: circle.width - circle.width/2
            height: width
            radius: width * 0.5
            color : focus ? "white" : "black"
            focus: true
        }

        MouseArea{
            onPressed: interiorCircle.focus = true
            anchors.fill: parent
        }
    }
}
