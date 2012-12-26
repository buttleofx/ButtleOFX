import QtQuick 1.1

/* Tabs bar */

Rectangle {
    id: tabBar
    implicitWidth: 850
    width: parent.width
    height: 30
    color: "transparent"

    property color tabColor: "#141414"

    Item {
        id: tab1
        width: 75
        height: 30
        clip: true
        Rectangle {
            anchors {
                fill: parent;
                bottomMargin: -radius
            }
            Text {
                id: tabLabel
                anchors.centerIn: parent
                text: "Viewer 1"
                font.pointSize: 8
                color: "white"
            }
            radius: 10
            color: tabColor
        }
    }

    Item {
        id: tab2
        width: 30
        height: 30
        x: 76
        clip: true
        Rectangle {
            anchors {
                fill: parent;
                bottomMargin: -radius
            }
            Image {
                id: addButton
                source: "../img/plus.png"
                anchors.centerIn: parent
            }
            radius: 10
            color: tabColor
        }
    }
}
