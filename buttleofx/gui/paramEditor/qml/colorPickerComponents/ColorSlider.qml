import QtQuick 1.1

// color slider
Rectangle {
    id: colorSlider
    implicitWidth: 16
    implicitHeight: 120

    //property used to compute the value of the color
    property real value: (1 - cursorColorSlider.y/colorSlider.height)

    // test for enter colors values in inputs and adapt display
    //property real cursorColorPositionSlider: 0


    //alpha intensity gradient 
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 1.0;  color: "#FF0000" }
            GradientStop { position: 0.85; color: "#FFFF00" }
            GradientStop { position: 0.76; color: "#00FF00" }
            GradientStop { position: 0.5;  color: "#00FFFF" }
            GradientStop { position: 0.33; color: "#0000FF" }
            GradientStop { position: 0.16; color: "#FF00FF" }
            GradientStop { position: 0.0;  color: "#FF0000" }
        }
        MouseArea{
            anchors.fill: parent
            onClicked: {
                cursorColorSlider.y = mouseY
                paramObject.colorSlider = cursorColorSlider.y
            }
        }
    }
    Rectangle{
        id: cursorColorSlider
        width: colorSlider.width
        height: 5
        color: "transparent"
        border.color: "white"
        border.width: 2
        y: paramObject.colorSlider
        MouseArea{
            anchors.fill: parent
            drag.target: parent
            drag.axis: Drag.YAxis
            drag.minimumY: 0
            drag.maximumY: colorSlider.height 
            anchors.margins: -5// allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
        }
    }
}