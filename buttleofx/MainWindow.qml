import QtQuick 1.1
import QtDesktop 0.1
import "gui/graph/qml"
import "gui/viewer/qml"
import "gui/paramEditor/qml"

Rectangle
{
    id: buttleWindow

    anchors.fill: parent
    width: 1280
    height: 800
    color: "#252525"

    Rectangle{
        id:mainMenu
        width: parent.width
        height: 30
        color: "#141414"

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: "#00b2a1"
            text: "ButtleOFX"
            font.pointSize: 14
        }
    }

    Column {

        width: parent.width
        height: parent.height
        x: 10
        y: 45

        SplitterRow {

            anchors.fill: parent

            SplitterColumn {

                width: 0.8*parent.width
                height: parent.height
                Splitter.expanding: true

                Player {
                    width: parent.width
                    height: 0.5*parent.height
                    y: 30
                }

                GraphEditor {
                    width: parent.width
                    height:0.5*parent.height
                }
            }

            ParamEditor {
                    Splitter.expanding: true
            }
        }
    }
}
