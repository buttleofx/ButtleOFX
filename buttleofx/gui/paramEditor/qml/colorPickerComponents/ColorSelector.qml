import QtQuick 1.1

//square where we can choose the intensity of the color
Item{
    id: colorPicker
    implicitWidth: 120
    implicitHeight: 120
    clip: true

    property color currentColor : "blue"
    property real saturation : cursorPicker.x/colorPicker.width
    property real brightness : 1 - cursorPicker.y/colorPicker.height

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

    Item {
        id: cursorPicker
        property int r : 5
        Rectangle {
            x: alreadyPassed ? - parent.r : -parent.r + paramObject.colorSelectorX
            y: alreadyPassed ? -parent.r : -parent.r + paramObject.colorSelectorY
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
                paramObject.colorSelectorX = Math.max(0, Math.min(width,  mouse.x));
                cursorPicker.x =  Math.max(0, Math.min(width,  mouse.x));
                paramObject.colorSelectorY = Math.max(0, Math.min(height, mouse.y));
                cursorPicker.y = Math.max(0, Math.min(height, mouse.y));
            }
        }
        onPositionChanged: {
            handleMouse(mouse)
        }
        onPressed: {
            handleMouse(mouse)
        }
    }
}