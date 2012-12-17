import QtQuick 1.1

Rectangle {
    id: connection
    implicitWidth: 100
    implicitHeight: 2
    property variant nodeIn: nodeIn
    property variant nodeOut: nodeOut

    MouseArea {
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
    }
}
