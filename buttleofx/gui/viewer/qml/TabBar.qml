import QtQuick 1.1

/* Tabs bar */

Rectangle {
    id: tabBar
    implicitWidth: 850
    implicitHeight: 20
    color: "transparent"

    property color tabColor: "#141414"

    Item {
        id: tab1
        implicitWidth: 100
        implicitHeight: 20
        height: parent.height
        clip: true
        Rectangle {
            anchors {
                fill: parent;
                bottomMargin: -radius
            }
            Text {
                id: tabLabel
                anchors.horizontalCenter: parent.horizontalCenter
                y:5
                text: "Viewer 1"
                font.pointSize: 10
                color: "white"
            }
            radius: 10
            color: tabColor
        }
    }

    Item {
        id: tab2
        implicitWidth: 30
        height: parent.height
        x: tab1.width + 1
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
