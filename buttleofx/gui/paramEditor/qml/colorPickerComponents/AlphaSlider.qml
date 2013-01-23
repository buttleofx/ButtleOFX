import QtQuick 1.1

/* alpha (transparency) slider */
Rectangle {
    id: alphaSlider
    implicitWidth: 16
    implicitHeight: 120
    color:"white"

    // property used to compute the value of the color
    property real value: (1 - cursorAlphaSlider.y/height)
    
    SquaresGrid { cellSize: 2 }

    Rectangle {
        anchors.fill: parent
        border.color: "white"
        border.width: 1
        radius: 2
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#FF000000" }
            GradientStop { position: 1.0; color: "#00000000" }
        }
    }
    Rectangle{
        id: cursorAlphaSlider
        width: alphaSlider.width
        height: 5
        color: "transparent"
        border.color: "white"
        border.width: 2
        radius: 1
        MouseArea{
            anchors.fill: parent
            drag.target: parent
            drag.axis: Drag.YAxis
            drag.minimumY: 0//- cursorAlphaSlider.height/2
            drag.maximumY: alphaSlider.height //- cursorAlphaSlider.height/2
            anchors.margins: -5 // allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
        }
    }
}