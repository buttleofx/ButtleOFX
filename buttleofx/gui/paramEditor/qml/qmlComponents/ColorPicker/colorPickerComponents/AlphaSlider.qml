import QtQuick 1.1

/* alpha (transparency) slider */
Rectangle {
    id: alphaSlider
    implicitWidth: 16
    implicitHeight: 120
    color:"white"

    // the current alpha value for the user
    property real alphaValue

    // property used to say that value of alpha has changed and what its new value is in ColorPicker.qml
    property real newAlphaValue

    // value which changed everytime the alpha cursor mooved (between 0 and 1 here)
    property real editingAlphaValue: (1 - cursorAlphaSlider.y/alphaSlider.height) 

    SquaresGrid { 
        height: parent.height
        width: parent.width
        cellSide: 5 
    }

    Rectangle {
        anchors.fill: parent
        border.color: "black"
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#FF000000" }
            GradientStop { position: 1.0; color: "#00000000" }
        }
        MouseArea{
            anchors.fill: parent
            onClicked: {
                newAlphaValue = editingAlphaValue
                cursorAlphaSlider.y = mouseY
            }
        }
    }
    Rectangle {
        id: cursorAlphaSlider
        width: alphaSlider.width
        height: 5
        color: "transparent"
        border.color: "white"
        border.width: 2
        y: (1 - alphaValue)*alphaSlider.height

        MouseArea {
            anchors.fill: parent
            drag.target: parent
            drag.axis: Drag.YAxis
            drag.minimumY: 0//- cursorAlphaSlider.height/2
            drag.maximumY: alphaSlider.height //- cursorAlphaSlider.height/2
            anchors.margins: -5 // allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
            acceptedButtons: Qt.LeftButton
            onPressed: {
                stateMoving.state = "moving"
            }
            onReleased: {
                // order of the lines matters
                // editingAlphaValue defined on top of this file
                // newAlphaValue only sends when the mouse is released to avoid too much signals
                newAlphaValue = editingAlphaValue
                stateMoving.state = "normal"
            }
        }

        StateGroup {
            // this state concerns the state of the cursor mooved with the mouse and used to choose the value of alpha
            id: stateMoving
            // state by default, cursor doesn't moved
            state: "normal"
            states: [
                State {
                    // cursor is not moved by the user
                    name: "normal"
                    PropertyChanges { target: cursorAlphaSlider; y: (1 - alphaValue)*alphaSlider.height; }
                },
                State {
                    // cursor is moved by the user
                    name: "moving"
                    PropertyChanges { target: cursorAlphaSlider; y: (1 - alphaValue)*alphaSlider.height; }
                }
            ]
        }

    }
}