import QtQuick 1.1

//square where we can choose the intensity of the color
Item{
    id: colorPicker
    implicitWidth: 120
    implicitHeight: 120

    property color currentColor : "blue"
    property real saturation : cursorPicker.x/colorPicker.width
    property real brightness : 1 - cursorPicker.y/colorPicker.height
    clip: true
    Rectangle{
        anchors.fill: parent;
        rotation: -90
        gradient: Gradient {
            GradientStop { position: 0.0;  color: "#FFFFFFFF" }
            GradientStop { position: 1.0; color: colorPicker.currentColor }
        }
    }
    Rectangle{
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 1.0; color: "#FF000000" }
            GradientStop { position: 0.0; color: "#00000000" }
        }
    }

    Rectangle{
        id: cursorPicker
        width: 5
        height: 5
        radius: 2
        color: "white"
        border.color: "black"
        MouseArea{
            anchors.fill: parent
            drag.target: parent
            drag.axis: Drag.XandYAxis
            drag.minimumX: 0 //- cursorPicker.width/2
            drag.maximumX: colorPicker.width - cursorPicker.width
            drag.minimumY: 0 //- cursorPicker.width/2
            drag.maximumY: colorPicker.height - cursorPicker.height
            anchors.margins: -5 // allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
        }    
    }   
}