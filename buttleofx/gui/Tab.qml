import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Item {
    id: tabBar
    implicitHeight: 15

    property color tabColor: "#141414"
    property string name: "New tab"
    signal closeClicked(bool clicked)

    Row{
        spacing: 1
        Rectangle {
            id:tab
            implicitWidth: 100
            implicitHeight: 25
            radius: 7
            color: tabBar.tabColor
            Text {
                id: tabLabel
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.margins: 3
                anchors.leftMargin: 8
                text: tabBar.name
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
        }//tab
    }//Row
}//tabBar
