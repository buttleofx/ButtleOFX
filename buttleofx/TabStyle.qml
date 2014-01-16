import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

TabViewStyle {

    signal buttonCloseClicked(bool clicked)

    frameOverlap: 1
    tab: Rectangle {
        color: "#141414"
        implicitWidth: 100
        implicitHeight: 25
        radius: 7

        Text {
            id: tabLabel
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: 3
            anchors.leftMargin: 8
            text: styleData.title
            color: "white"
            font.pointSize: 8
        }

        Button {
            width: 12
            height: 12
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: 4

            iconSource:
                if (pressed){
                    "gui/img/icons/close_hover.png"
                }else{
                    "gui/img/icons/close.png"
                }

            style:
                ButtonStyle {
                    background: Rectangle {
                        anchors.fill: parent
                        color: "transparent"
                    }
                }

            onClicked: buttonCloseClicked(true)
        }
    }
    frame: Rectangle { color: "#353535" }
}

