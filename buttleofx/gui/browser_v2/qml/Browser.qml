import QtQuick 2.0
import QtQuick.Layouts 1.0

Rectangle {
    id: root

    width: 800
    height: 600
    color: "#353535"

    ColumnLayout {
        anchors.fill: parent

        NavBar {
            id: navBar

            height : 50
            anchors.top: parent.top
            Layout.fillWidth: true
        }

// Main window with files list
//        FilesWindow{
//        }
    }
}
