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
        //width of the column (contains vertical elements Text and Row ) is the same as the window
        width: parent.width
        height: parent.height
        spacing: 0
        Text
        {
            /*height of text is 2% of window's height*/
            width: parent.width
            height: 2/100 * parent.height
            color: "#fff"
            text: "Menu of ButtleOFX"
            font.pointSize: 2/100 * parent.height;
        }
        Row {
            //width of the row is the same as the window (i.e the column here)
            width: parent.width
            //height of the row is 98% of the window (10% for the menu)
            height: 98/100 * parent.height
            spacing: 0

            Column
            {
                //width of the column is 70% of the window (other 30% for the paramEditor)
                width: 70/100 * parent.width
                height: parent.height
                x: 10; y: 10
                spacing: 0
                Player
                {
                    //parent of the player is the column which is already at 70% of window's width so it has the same width
                    width: parent.width;
                    //player's height is 50% of the column's height
                    height: 50/100 * parent.height;
                    //y of the toolBar of the bottom is 5% of the player
                    toolHeight: 5/100 + parent.height
                }
                GraphEditor
                {
                    //same width as the column
                    width: parent.width;
                    //graphEditor's height is 50% of the column's height
                    height: 50/100 * parent.height
                }
            }

            ParamEditor
            {
                    //width is 30% of the row
                    width: 30/100 * parent.width
                    //height is the same as the window
                    height: parent.height
            }
        }
    }
}
