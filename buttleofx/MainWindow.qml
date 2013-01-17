import QtQuick 1.1
import QtDesktop 0.1
import "gui/graph/qml"
import "gui/viewer/qml"
import "gui/paramEditor/qml"

ApplicationWindow {
    id: buttleWindow
    title: "ButtleOFX"
    width: 1280
    height: 800
    minimumWidth: 100
    minimumHeight: 50

    Keys.onPressed: {
        console.log("ApplicationWindow Keys.onPressed");
        if (event.key == Qt.Key_Delete) {
            console.log("destruction");
            _buttleData.getGraphWrapper().destructionNode();
        }
        if (event.key == Qt.Key_U) {
                console.log("Undo");
                _cmdManager.undo();
            }
            if (event.key == Qt.Key_R) {
                console.log("Redo");
                _cmdManager.redo();
            }
    }

    Rectangle {
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

    //this rectangle represents the zone under the menu, it allows to define the anchors.fill and margins for the SplitterRow
    Rectangle {
        id: modulsContainer
        y: mainMenu.height
        width: parent.width
        height: parent.height - y
        color: "#353535"

        SplitterRow {
            anchors.fill: parent
            anchors.margins: 5
            //handleWidth changes the size of the separation between the row, column.
            //handleWidth: 3

            SplitterColumn {
                width: 0.7*parent.width
                height: parent.height
                //handleWidth: 3

                Player {
                    width: parent.width
                    height: 0.5*parent.height
                }

                GraphEditor {
                    width: parent.width
                    height:0.5*parent.height
                }
            }

            ParamEditor {
                width: 0.3*parent.width
            }
        }
    }
}
