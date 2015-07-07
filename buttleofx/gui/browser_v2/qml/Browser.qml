import QtQuick 2.2
import QtQuick.Layouts 1.1
import "../../../gui"

Rectangle {
    id: root

    width: 800
    height: 600
    color: "#353535"

    property int visitedFolderListIndex: 0
    signal buttonCloseClicked(bool clicked)
    signal buttonFullscreenClicked(bool clicked)

    function pushVisitedFolder(path){
        if (visitedFolderList.count === 0){
            // Save path of the current folder
            visitedFolderList.append({"url": _browser.currentPath})
        }
        visitedFolderList.append({"url": path})
        ++ visitedFolderListIndex
    }

    // Recently visited folder stack
    ListModel {
        id: visitedFolderList
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Tab {
            Layout.fillWidth: true
            id: tabBar
            name: "Browser"
            onCloseClicked: root.buttonCloseClicked(true)
            onFullscreenClicked: root.buttonFullscreenClicked(true)
        }

        NavBar {
            id: navBar
            Layout.fillWidth: true
            Layout.preferredHeight: childrenRect.height

            property var model: _browser
            property alias visitedFolderList: visitedFolderList
            property alias visitedFolderListIndex: root.visitedFolderListIndex
            onPushVisitedFolder: {
                root.pushVisitedFolder(path)
            }
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

             property var model: _browser
             property alias visitedFolderList: visitedFolderList
             property alias visitedFolderListIndex: root.visitedFolderListIndex

             onPushVisitedFolder: {
                 root.pushVisitedFolder(path)
             }
         }
    }
}
