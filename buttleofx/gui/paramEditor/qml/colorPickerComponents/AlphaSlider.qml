import QtQuick 1.1

/* alpha (transparency) slider */
Rectangle {
    id: alphaSlider
    implicitWidth: 16
    implicitHeight: 120
    color:"white"

    // property used to compute the value of the color
    property real value: (1 - cursorAlphaSlider.y/height)

    property real cursorAlphaPositionSlider: 0
    
    SquaresGrid { 
        height: parent.height
        width: parent.width
        cellSide: 5 
    }

    Rectangle {
        anchors.fill: parent
        border.color: "black"
        /*border.width: 1
        radius: 2*/
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#FF000000" }
            GradientStop { position: 1.0; color: "#00000000" }
        }
        MouseArea{
            anchors.fill: parent
            onClicked: {
                cursorAlphaSlider.y = mouseY
                paramObject.alphaSlider = cursorAlphaSlider.y
            }
        }
    }
    Rectangle{
        id: cursorAlphaSlider
        width: alphaSlider.width
        height: 5
        color: "transparent"
        border.color: "white"
        border.width: 2
        y: paramObject.alphaSlider
        //radius: 1
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