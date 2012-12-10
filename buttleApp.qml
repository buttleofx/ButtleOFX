import QtQuick 1.1
import "gui/graph/qml"
import "gui/viewer"
import "gui/paramEditor/qml"

Rectangle
{
    id: buttleWindow

    anchors.fill: parent
    implicitWidth: 1280
    implicitHeight: 800

    color: "#252525"

    Column {
        spacing: 10
        Text
        {
            color: "#fff"
            text: "Menu of ButtleOFX"
        }
        Row {
            spacing: 100
            Column
            {
                spacing: 10
                Column
                {
                    x: 10; y: 10
                    spacing: 10
                    Player
                    {
                    }
                    GraphEditor
                    {
                    }
                }
            }
            ParamEditor
            {
            }
        }
    }
}
