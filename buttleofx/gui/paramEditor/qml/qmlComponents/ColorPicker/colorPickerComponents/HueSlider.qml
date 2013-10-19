import QtQuick 2.0

// hue slider
Rectangle {
    id: hueSlider
    implicitWidth: 16
    implicitHeight: 120

    // the current value of the color
    property real hue

    // property used to say that hue of color has changed and what its new value is in ColorPicker.qml
    property real newHue

    // value which changed everytime the hue cursor mooved
    property real editingHue: (1 - cursorHueSlider.y/hueSlider.height)
    
    //hue gradient 
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
        MouseArea {
            anchors.fill: parent
            onClicked: {
                cursorHueSlider.y = mouseY
                newHue = editingHue
            }
        }
    }
    Rectangle {
        id: cursorHueSlider
        width: hueSlider.width
        height: 5
        color: "transparent"
        border.color: "white"
        border.width: 2
        y: (1 - hue) * cursorHueSlider.height

        MouseArea {
            anchors.fill: parent
            drag.target: parent
            drag.axis: Drag.YAxis
            drag.minimumY: 0
            drag.maximumY: hueSlider.height 
            anchors.margins: -5// allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
            acceptedButtons: Qt.LeftButton
            onPressed: {
                stateMoving.state = "moving"
            }
            onReleased: {
                // order of the lines matters
                // editingHue and newHue defined on top of this file
                // newHue only sends when the mouse is released to avoid too much signals
                newHue = editingHue
                stateMoving.state = "normal"
            }
        }
    }

    StateGroup {
        // this state concerns the state of the cursor mooved with the mouse and used to choose the hue of the color
        id: stateMoving
        // state by default, cursor doesn't moved
        state: "normal"
        states: [
            State {
                // cursor is not moved by the user
                name: "normal"
                PropertyChanges { target: cursorHueSlider; y: (1 - hue)*hueSlider.height; }
            },
            State {
                // cursor is moved by the user
                name: "moving"
                PropertyChanges { target: cursorHueSlider; y: (1 - hue)*hueSlider.height; }
            }
        ]
    }
}