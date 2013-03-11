import QtQuick 1.1

// square where we can choose the saturation and the brightness of the color
Item{
    id: bsPicker // bs for brightness and saturation
    implicitWidth: 120
    implicitHeight: 120
    clip: true

    // properties used to manage the update of saturation in colorPicker
    property real saturation
    property real newSaturation
    property real editingSaturation : cursorPicker.x/bsPicker.width

    // properties used to manage the update of brightness in colorPicker
    property real brightness
    property real newBrightness
    property real editingBrightness : 1 - cursorPicker.y/bsPicker.height

    // currentColor is the color displayed in the little rectangle (black by default)
    property color currentColor : "black"

    // used to place the cursor at the good position the first time
    property bool alreadyPassed: false

    SquaresGrid { 
        height: parent.height
        width: parent.width
        cellSide: 3 
    } 

    Rectangle{
        anchors.fill: parent;
        rotation: -90
        gradient: Gradient {
            GradientStop { position: 0.0;  color: "#FFFFFFFF" }
            GradientStop { position: 1.0; color: bsPicker.currentColor }
        }
    }
    Rectangle{
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 1.0; color: "#FF000000" }
            GradientStop { position: 0.0; color: "#00000000" }
        }
    }

    Item {
        id: cursorPicker
        property int r : 5
        Rectangle {
            // - parent.r is used to match center of the circle and position
            x: alreadyPassed ? - parent.r : -parent.r + saturation * bsPicker.width 
            y: alreadyPassed ? -parent.r : -parent.r + (1 - brightness) * bsPicker.height 
            width: parent.r*2
            height: parent.r*2
            radius: parent.r
            border.color: "black"
            border.width: 1
            color: "transparent"
            Rectangle {
                anchors.fill: parent; anchors.margins: 1;
                border.color: "white"
                border.width: 1
                radius: width/2
                color: "transparent"
            }
        }
    }
    MouseArea {
        anchors.fill: parent
        //handleMouse used to manage the displacement of the little circle cursor in the square
        function handleMouse(mouse) {
            if (mouse.buttons & Qt.LeftButton) {
                alreadyPassed = true
                cursorPicker.x =  Math.max(0, Math.min(width,  mouse.x));
                cursorPicker.y = Math.max(0, Math.min(height, mouse.y));
            }
        }
        onPositionChanged: {
            handleMouse(mouse)
        }
        onPressed: {
            stateMoving.state = "moving"
            handleMouse(mouse)
        }
        onReleased: {
            // warning : order of the lines matters
            // editingSaturation and editingBrightness defined on top of this file
            // newSaturation and newBrightness only send when the mouse is released to avoid too much signals
            newSaturation = editingSaturation
            newBrightness = editingBrightness
            stateMoving.state = "normal"
        }
    }

    StateGroup {
        // this state concerns the state of the cursor mooved with the mouse and used to choose the value of brightness and saturation
        id: stateMoving
        // state by default, cursor doesn't moved
        state: "normal"
        states: [
            State {
                // cursor is immobile
                name: "normal"
                PropertyChanges { target: cursorPicker; y: (1 - brightness)*bsPicker.height; x: saturation*bsPicker.width; }
            },
            State {
                // cursor is moved by the user
                name: "moving"
                PropertyChanges { target: cursorPicker; y: (1 - brightness)*bsPicker.height; x: saturation*bsPicker.width; }
            }
        ]
    }
}