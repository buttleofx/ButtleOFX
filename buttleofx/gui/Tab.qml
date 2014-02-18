import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Item {
    id: tabBar
    implicitHeight: 15
    width: parent.width
    implicitWidth: 100

    property color tabColor: "#141414"
    property string name: "New tab"
    signal closeClicked(bool clicked)
    signal fullscreenClicked(bool clicked)

    Row{
        spacing: 1
        width: parent.width

        Rectangle {
            id:tab
            width: parent.width
            implicitWidth: 100
            implicitHeight: 25
            color: tabBar.tabColor
            Text {
                id: tabLabel
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.leftMargin: 4
                text: tabBar.name
                color: "#cccccc"
                font.pointSize: 8
            }

            Button {
                width: 10
                height: 10
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.rightMargin: 4
                anchors.topMargin: 2

                iconSource:
                    if (hovered){
                        "img/icons/close_hover.png"
                    }else{
                        "img/icons/close.png"
                    }

                style:
                    ButtonStyle {
                        background: Rectangle {
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }

                onClicked: closeClicked(true)
            }

            Button {
                width: 10
                height: 10
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.rightMargin: 16
                anchors.topMargin: 2

                iconSource:
                    if (hovered){
                        "img/icons/fullscreen_hover.png"
                    }else{
                        "img/icons/fullscreen.png"
                    }

                style:
                    ButtonStyle {
                        background: Rectangle {
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }

                onClicked: fullscreenClicked(true)
            }
        }//tab
    }//Row
}//tabBar
