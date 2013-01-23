import QtQuick 1.1

// color slider
Rectangle {
    id: colorSlider
    implicitWidth: 16
    implicitHeight: 120

    //property used to compute the value of the alpha
    property real value: (1 - cursorColorSlider.y/colorSlider.height)

    //alpha intensity gradient background
    Rectangle {
        anchors.fill: parent
        border.color: "White"
        border.width: 1
        radius: 2

        gradient: Gradient {
            GradientStop { position: 1.0;  color: "#FF0000" }
            GradientStop { position: 0.85; color: "#FFFF00" }
            GradientStop { position: 0.76; color: "#00FF00" }
            GradientStop { position: 0.5;  color: "#00FFFF" }
            GradientStop { position: 0.33; color: "#0000FF" }
            GradientStop { position: 0.16; color: "#FF00FF" }
            GradientStop { position: 0.0;  color: "#FF0000" }
        }
    }
    Rectangle{
        id: cursorColorSlider
        width: colorSlider.width
        height: 5
        color: "transparent"
        border.color: "white"
        border.width: 2
        radius: 1
        MouseArea{
            anchors.fill: parent
            drag.target: parent
            drag.axis: Drag.YAxis
            drag.minimumY: 0//- cursorColorSlider.height/2
            drag.maximumY: colorSlider.height //- cursorColorSlider.height/2
            anchors.margins: -5// allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
        }
    }
}