import QtQuick 1.1

// Tabs' bar
Rectangle {
    id: tabBar
    implicitWidth: 850
    implicitHeight: 20
    width: parent.width
    //height of the tab bar is 5% of the Player's height
    height: 5/100 * parent.height;
    anchors.top: parent.top
    color: toolbarColor

    Rectangle {
        id: tabBack
        width: 80
        height: parent.height - tabBack.y
        y: 7
        color: backColor
    }
    Rectangle {
        id: tab
        width: 80
        height: parent.height
        anchors.top:  parent.top
        color: backColor
        radius: 7

        Text {
            id: tabFigure
            anchors.centerIn: parent
            text: "Viewer 1"
            font.pointSize: 8
            color: textColor
        }
    }
    Rectangle {
        id: addBack
        width: 30
        height: parent.height -addBack.y
        y: 7
        x: tab.width + 2
        color: backColor
    }
    Rectangle {
        id: add
        width: 30
        height: parent.height
        x: tab.width + 2
        anchors.top:  parent.top
        color: backColor
        radius: 7

        Image {
            id: addButton
            source: "img/plus.png"
            anchors.centerIn: parent
        }
    }
}
