import QtQuick 1.1

Rectangle {
    id: graphEditor
    width: 850
    height: 350
    z: 0
    property variant graphX: 0
    property variant graphY: 0
    clip: true

    Graph {
        y: 30
        width : parent.width
        height: parent.height
    }

    Tools {
        width : parent.width
        height: 30
    }
}
