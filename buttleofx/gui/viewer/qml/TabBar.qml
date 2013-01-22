import QtQuick 1.1


Rectangle {
    id: tabBar
    implicitWidth: 950
    implicitHeight: 25
    color: "#353535"
    property color tabColor: "#141414"

    Item {
        id: tab1
        implicitWidth: 100
        implicitHeight: 20
        height: parent.height
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
                color: "white"
                font.pointSize: 10
            }
            radius: 10
            color: tabBar.tabColor
        }
    }

    Item {
        id: tab2
        implicitWidth: 30
        height: parent.height
        x: tab1.width + 1
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
            color: tabBar.tabColor
        }
    }
}