import QtQuick 2.2
import QtQuick.Layouts 1.0
import BrowserModel 1.0


Rectangle {
    id: root

    width: 800
    height: 600

    color: "#353535"


    // Recently visited folder stack
    ListModel {
        id: visitedFolderList
    }

    BrowserModel {
        id: browser
    }

    ColumnLayout {
        anchors.fill: parent

        NavBar {
            id: navBar

            Layout.fillWidth: true
            height : 30

            model: browser
            visitedFolderList: visitedFolderList

            anchors.top: parent.top
        }

        // Main window with files list
        // FilesWindow{
        // }
    }
}
