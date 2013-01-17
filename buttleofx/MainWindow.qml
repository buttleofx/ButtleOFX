import QtQuick 1.1
import QtDesktop 0.1
import "gui/graph/qml"
import "gui/viewer/qml"
import "gui/paramEditor/qml"

Rectangle {
    width: 1280
    height: 800

    Keys.onPressed: {
        console.log("ApplicationWindow Keys.onPressed");
        if (event.key == Qt.Key_Delete) {
            console.log("destruction");
            _graphWrapper.destructionNode();
        }
        if (event.key == Qt.Key_U) {
                _cmdManager.undo();
            }
            if (event.key == Qt.Key_R) {
                console.log("R");
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
            handleWidth: 4

            /*There is a bug with splitter column, the draggable splitter doesn't moove as it should, this bug has been solved in qtcomponents for qt5, 
            but for the moment we are using qt 4*/
            SplitterColumn {
                width: 0.7*parent.width
                height: parent.height
                handleWidth: 4
                Splitter.minimumWidth : 5
                Splitter.expanding: true // obligatory to allow to have the minimumWidth

                Player {
                    Splitter.minimumHeight: 10
                    //Splitter.expanding: true
                    width: parent.width
                    height: 0.5*parent.height
                }

                GraphEditor {
                    Splitter.minimumHeight: 10
                    width: parent.width
                    height:0.5*parent.height
                }
            }

            ParamEditor {
                Splitter.minimumWidth: 5
                width: 0.3*parent.width
            }
        }
    }
}
