import QtQuick 2.2
import QtQuick.Layouts 1.1
import BrowserModel 1.0


Rectangle {
    id: root

    width: 800
    height: 600

    color: "#353535"

    property int visitedFolderListIndex: 0

    // Recently visited folder stack
    ListModel {
        id: visitedFolderList
    }

    BrowserModel {
        id: browser
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        NavBar {
            id: navBar

            Layout.fillWidth: true
            Layout.preferredHeight: 50

            model: browser
            visitedFolderList: visitedFolderList
            visitedFolderListIndex: visitedFolderListIndex
        }

        Rectangle {
            id: separator

            Layout.fillWidth: true
            Layout.preferredHeight: 1

            color: "#00b2a1"
        }

        // Main window with files list
         FileWindow{
             id: fileWindow

             Layout.fillWidth: true
             Layout.fillHeight: true

             model: browser
             visitedFolderList: visitedFolderList
             visitedFolderListIndex: visitedFolderListIndex
         }
    }
}
