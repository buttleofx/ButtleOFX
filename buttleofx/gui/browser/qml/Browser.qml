import QtQuick 2.2
import QtQuick.Layouts 1.1
import "../../../gui"

Rectangle {
    id: root

    width: 800
    height: 600
    color: "#353535"

    property alias fileWindow: fileWindow
    property alias navBar: navBar
    property bool showTab: true
    property variant bModel: _browser
    property variant bAction: _browserAction
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

    function popVisitedFolder(){
        if (visitedFolderList.count > 0 && visitedFolderListIndex > 0) {
            -- visitedFolderListIndex
            bModel.currentPath = visitedFolderList.get(visitedFolderListIndex).url
        }
    }

    // Recently visited folder stack
    ListModel {
        id: visitedFolderList
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Tab {
            id: tabBar
            Layout.fillWidth: true
            name: "Browser"
            visible: root.showTab
            onCloseClicked: root.buttonCloseClicked(true)
            onFullscreenClicked: root.buttonFullscreenClicked(true)
        }

        NavBar {
            id: navBar
            Layout.fillWidth: true
            Layout.preferredHeight: childrenRect.height

            property var model: root.bModel
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

             property var model: root.bModel
             property var bAction: root.bAction
             property alias visitedFolderList: visitedFolderList
             property alias visitedFolderListIndex: root.visitedFolderListIndex

             onPushVisitedFolder: {
                 root.pushVisitedFolder(path)
             }
         }
    }

    Keys.onReleased: {
        if ((event.modifiers & Qt.ControlModifier) && (event.key == Qt.Key_L)){
            navBar.toggleUrlEdit()
        }
    }
}
