import QtQuick 2.0
import "mathUtils.js" as MathUtils

Item {
    id: root
    property real value

    signal accepted
    // Signal call when the slider is moving, use it in spite of onValue to avoid binding loop
    signal updatedValue(var updatedValue)

    states :
        // When user is moving the slider
        State {
            name: "editing"
            PropertyChanges {
                target: root
                // Initialize with the value in the default state.
                // Allows to break the link in that state.
                value: root.value
            }
        }

    // Cursor
    Item {
        id: pickerCursor
        width: 8
        height: parent.height

        Rectangle {
            id: cursor
            x: MathUtils.clamp(root.width * root.value - parent.width / 2, 0, root.width)
            y: -4
            width: parent.width
            height: parent.height + -2*y
            border.color: "black"
            border.width: 1
            color: "transparent"

            Rectangle {
                anchors.fill: parent; anchors.margins: 1
                border.color: "white"; border.width: 1
                color: "transparent"
            }
        }
    }

    MouseArea {
        id: mouseAreaSlider
        anchors.fill: parent

        function sliderHandleMouse(mouse){
            root.state = 'editing'
            if (mouse.buttons & Qt.LeftButton) {
                root.value = MathUtils.clampAndProject(mouse.x, 0.0, root.width, 0, 1.0)
                root.updatedValue(root.value)
            }
        }
        onPositionChanged: sliderHandleMouse(mouse)
        onPressed: sliderHandleMouse(mouse)
        onReleased: {
            root.state = ''
            root.accepted()
        }
    }
}
