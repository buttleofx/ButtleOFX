import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0
import QtQuick.Dialogs 1.1

Rectangle {
    id: root
    color: 'transparent'

    // defaults slots
    function onItemClickedSlot(pathImg){
        // handleGraphViewerClick
        // We come to the temporary viewer
        player.changeViewer(11)

        // We save the last node wrapper of the last view
        var nodeWrapper
        player.lastNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(player.lastView)
        nodeWrapper = _buttleData.nodeReaderWrapperForBrowser(pathImg)
        _buttleData.currentGraphIsGraphBrowser()
        _buttleData.currentGraphWrapper = _buttleData.graphBrowserWrapper
        _buttleData.currentViewerNodeWrapper = nodeWrapper
        _buttleData.currentViewerFrame = 0

        // We assign the node to the viewer, at the frame 0
        _buttleData.assignNodeToViewerIndex(nodeWrapper, 10)
        _buttleData.currentViewerIndex = 10 // We assign to the viewer the 10th view
        _buttleEvent.emitViewerChangedSignal()
    }

    function onItemDoubleClickedSlot(absolutePath){
        // handleGraphViewerDoubleClick
        _buttleData.currentGraphWrapper = _buttleData.graphWrapper
        _buttleData.currentGraphIsGraph()

        // If before the viewer was showing an image from the browser, we change the currentView
        if (_buttleData.currentViewerIndex > 9){
            _buttleData.currentViewerIndex = player.lastView

            if (player.lastNodeWrapper != undefined)
                _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
            player.changeViewer(player.lastView)
        }
          _buttleManager.nodeManager.dropFile(absolutePath, 10, 10)
    }

    signal itemClicked(string absolutePath, string pathImg, bool isFolder, bool isSupported)
    signal itemDoubleClicked(string absolutePath, string pathImg, bool isFolder, bool isSupported)
    signal pushVisitedFolder(string path)

    Keys.onEscapePressed: root.model.unselectAllItems()


    Keys.onPressed: {
        if(event.key === Qt.Key_F5){
            root.model.loadData('')
        }
    }

    // key navigation between browser items
    Keys.onReleased: {
        var k = event.key
        if(k === Qt.Key_Backspace && (event.modifiers & Qt.ShiftModifier)){
            popVisitedFolder()
        }

        else if(k === Qt.Key_Backspace){
            if(model.currentPath !== "/" && model.currentPath.trim() !== ""){
                pushVisitedFolder(model.parentFolder)
                root.model.currentPath = root.model.parentFolder
            }
        }

        var selectedItem = null

        // enter inside folder on enter: change model current path
        // use clicked signals: wanted behavior
        if(k === Qt.Key_Enter || k === Qt.Key_Return){
            var indexSelected = grid.currentIndex
            selectedItem = root.model.fileItems.get(indexSelected)

            if(selectedItem.isFolder()){
                root.model.currentPath = selectedItem.path
                return
            }

            root.model.selectItem(indexSelected)
            root.itemDoubleClicked(selectedItem.path, selectedItem.path, selectedItem.isFolder(), selectedItem.isSupported())
            root.itemClicked(selectedItem.path, selectedItem.path, selectedItem.isFolder(), selectedItem.isSupported())

            if(!selectedItem.isSupported())
                selectedItem.launchDefaultApplication()
        }

        if(k === Qt.Key_Up)
            grid.moveCurrentIndexUp()
        else if (k === Qt.Key_Down)
            grid.moveCurrentIndexDown()
        else if (k === Qt.Key_Left)
            grid.moveCurrentIndexLeft()
        else if (k === Qt.Key_Right)
            grid.moveCurrentIndexRight()
        else
            return

        if(event.modifiers & Qt.ShiftModifier)
            root.model.selectItemTo(grid.currentIndex)
        else
            root.model.selectItem(grid.currentIndex)


    }

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        onClicked:{
            root.forceActiveFocus()
            root.model.unselectAllItems()
            actionsMenu.showActionOnItem = false
            if(mouse.button == Qt.RightButton)
                actionsMenu.popup()
            if(mouse.button == Qt.LeftButton)
                root.model.unselectAllItems()
        }
    }

    MessageDialog {
        id: defaultApplicationFail
        title: "Error while opening file with system"
        text: ""
    }

    Menu{
        id:actionsMenu
        property bool showActionOnItem: false

        MenuItem{
            id: defaultApplication
            text:"Open system application"
            iconName: "document-open"
            shortcut: StandardKey.Open
            visible:actionsMenu.showActionOnItem

            onTriggered: {
                var itemsSelected = root.model.selectedItems
                var failedFiles = []

                for(var i=0; i<itemsSelected.count; ++i){
                    if(!itemsSelected.get(i).launchDefaultApplication())
                        failedFiles.push(itemsSelected.get(i).path)
                }

                if(failedFiles.length){
                    defaultApplicationFail.text = 'Problem occured while opening: \n ' + failedFiles.join() + ' file' + (failedFiles.length > 1 ? 's' : '') + '.'
                    defaultApplicationFail.visible = true
                }

            }
        }


        MenuItem{
            id: select
            text:"Select all"
            iconName: "edit-select-all"
            shortcut: StandardKey.SelectAll
            onTriggered: {
                root.model.selectAllItems()
            }
        }

        MenuItem{
            text:"Refresh"
            iconName: "reload"
            shortcut: StandardKey.Refresh
            onTriggered: {
                root.model.refresh()
            }
        }
        MenuSeparator{}
        MenuItem{
            text:"Find"
            iconName: "edit-find"
            shortcut: StandardKey.Find
            onTriggered: {
                navBar.searchLayout.show()
            }
        }
        MenuItem{
            text:"New folder"
            visible:!actionsMenu.showActionOnItem
            iconName: "folder-new"
            shortcut: StandardKey.New
            onTriggered: {
                root.bAction.handleNew("Folder")
                root.model.refresh()
            }
        }
        MenuItem{
            text:"New file"
            visible:!actionsMenu.showActionOnItem
            iconName: "document-new"
            shortcut: StandardKey.UnknownKey
            onTriggered: {
                root.bAction.handleNew("File")
                root.model.refresh()
            }
        }
        MenuSeparator{}
        MenuItem{
            text:"Copy"
            visible:actionsMenu.showActionOnItem
            shortcut: StandardKey.Copy
            iconName: "edit-copy"
            onTriggered: {
                root.bAction.handleCopy()
            }
        }
        MenuItem{
            text:"Cut"
            visible:actionsMenu.showActionOnItem
            iconName: "edit-cut"
            shortcut: StandardKey.Cut
            onTriggered: {
                root.bAction.handleMove()
            }
        }
        MenuItem{
            text:"Paste"
            iconName: "edit-paste"
            shortcut: StandardKey.Paste
            enabled: root.bAction.isCache
            onTriggered: {
                var destination = ""
                if(root.model.selectedItems.count == 1 && root.model.selectedItems.get(0).isFolder())
                    destination = root.model.selectedItems.get(0).path

                root.bAction.handlePaste(destination)
                root.model.refresh()

            }
        }
        MenuItem{
            text:"Delete"
            visible:actionsMenu.showActionOnItem
            iconName: "edit-delete"
            shortcut: StandardKey.Deletes
            onTriggered: {
                root.bAction.handleDelete()
                root.model.refresh()
            }
        }

        Menu{
            title:"Tuttle preset"
        }
    }

    ScrollView {
        anchors.fill: parent

        style: ScrollViewStyle {
            scrollBarBackground: Rectangle {
                id: scrollBar
                width: styleData.hovered ? 8 : 4
                color: "transparent"

                Behavior on width { PropertyAnimation { easing.type: Easing.InOutQuad ; duration: 200 } }
            }

            handle: Item {
                implicitWidth: 15
                Rectangle {
                    color: "#00b2a1"
                    anchors.fill: parent
                }
            }

            decrementControl : Rectangle {
                visible: false
            }

            incrementControl : Rectangle {
                visible: false
            }
        }

        GridView {
            id: grid

            anchors.fill: parent
            anchors.topMargin: 20

            cellWidth: 150
            cellHeight: 100

            model: root.model.fileItems
            delegate: component

            keyNavigationWraps: true
            boundsBehavior: Flickable.StopAtBounds

            // set the properly current selected when model ends loading
            Connections{
                target: root.model
                onLoadingChanged: {
                    if(!root.model.loading)
                        grid.currentIndex = -1
                }
            }
        }
    }

    Component {
        id: component

        Rectangle {
            id: component_container

            width: grid.cellWidth - 20
            height: icon.height + fileName.height

            color: model.object.isSelected ? "#666666" : "transparent"
            radius: 2

            Column {
                anchors.fill: parent

                Image {
                    id: loading

                    anchors.horizontalCenter: parent.horizontalCenter
                    height: 50
                    width: parent.width

                    source: "img/refresh_hover.png"
                    sourceSize.width: 20
                    sourceSize.height: 20
                    asynchronous: true

                    fillMode: Image.Pad

                    visible: !model.object.folder && model.object.thumbnailState === "loading"

                    NumberAnimation on rotation {
                        from: 0
                        to: 360
                        running: loading.visible
                        loops: Animation.Infinite
                        duration: 1000
                    }
                }

                Image {
                    id: icon

                    anchors.horizontalCenter: parent.horizontalCenter
                    height: 50
                    width: parent.width - 20

                    source: model.object.pathImg
                    sourceSize.width: 50
                    sourceSize.height: 50
                    asynchronous: true

                    fillMode: Image.PreserveAspectFit

                    opacity: ((icon_mouseArea.containsMouse || text_mouseArea.containsMouse) ^ model.object.isSelected) ? 1 : 0.7
                    visible: !loading.visible

                    MouseArea {
                        id: icon_mouseArea
                        anchors.fill: parent
                        acceptedButtons: Qt.LeftButton | Qt.RightButton
                        hoverEnabled: true
                    }
                }

                Text {
                    id: fileName

                    width: parent.width
                    height: paintedHeight

                    elide: (model.object.isSelected || text_mouseArea.containsMouse || icon_mouseArea.containsMouse) ? Text.ElideNone : Text.ElideRight
                    anchors.horizontalCenter: parent.horizontalCenter
                    horizontalAlignment: Text.AlignHCenter

                    text: model.object.name
                    color: ((icon_mouseArea.containsMouse || text_mouseArea.containsMouse) ^ model.object.isSelected) ? "white" : "#BBBBBB"
                    wrapMode: Text.WrapAnywhere

                    MouseArea {
                        id: text_mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                    }

                    onElideChanged: {
                        fileName.height = (elide == Text.ElideRight ? 20 : paintedHeight) //force good heigt after unselect
                    }
                }

                Component.onCompleted: {
                    fileName.width = fileName.contentWidth
                }
            }

            MouseArea{
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton

                onClicked: {
                    root.forceActiveFocus()

                    if(mouse.button == Qt.RightButton){
                        if(!root.model.selectedItems.count)
                            root.model.selectItem(index)
                        actionsMenu.showActionOnItem = true
                        actionsMenu.popup()
                    }

                    else if(mouse.button == Qt.LeftButton){
                        root.itemClicked(model.object.path, model.object.path, model.object.isFolder(), model.object.isSupported())
                        grid.currentIndex = index

                        if ((mouse.modifiers & Qt.ShiftModifier))
                            root.model.selectItemTo(index)
                        else if ((mouse.modifiers & Qt.ControlModifier))
                            model.object.isSelected = !model.object.isSelected
                        else
                            root.model.selectItem(index)
                    }
                }
                onDoubleClicked: {
                    root.itemDoubleClicked(model.object.path, model.object.path, model.object.isFolder(), model.object.isSupported())

                    // we ensure this behavior by default
                    if (model.object.isFolder()) {
                        pushVisitedFolder(model.object.path)
                        root.model.currentPath = model.object.path
                    }
                }
            }
        }
    }

//    ScrollView {
//        Layout.fillHeight: true
//        Layout.fillWidth: true

//        style: ScrollViewStyle {
//            scrollBarBackground: Rectangle {
//                id: scrollBar
//                width: 15
//                height: parent.height
//                anchors.right: parent.right
//                color: "transparent"
//            }

//            decrementControl : Rectangle {
//                id: scrollLower
//                width: 15
//                height: 15
//                color: "#343434"

//                Image {
//                    id: arrowDown
//                    source: styleData.pressed ? "img/arrow_up_hover.png" : "img/arrow_up.png"
//                    anchors.horizontalCenter: parent.horizontalCenter
//                    anchors.verticalCenter: parent.verticalCenter
//                }
//            }

//            incrementControl : Rectangle {
//                id: scrollHigher
//                width: 15
//                height: 15
//                color: "#343434"

//                Image {
//                    id: arrowUp
//                    source: styleData.pressed ? "img/arrow_down_hover.png" : "img/arrow_down.png"
//                    anchors.horizontalCenter: parent.horizontalCenter
//                    anchors.verticalCenter: parent.verticalCenter
//                }
//            }
//        }

//        TableView {

//            id: listView
//            height: parent.height
//            width: parent.width

//            style: TableViewStyle {
//                scrollBarBackground: Rectangle {
//                    id: scrollBar
//                    width: 15
//                    height: parent.height
//                    anchors.right: parent.right
//                    color: "transparent"
//                }

//                decrementControl : Rectangle {
//                    id: scrollLower
//                    width: 15
//                    height: 15
//                    color: "#343434"

//                    Image {
//                        id: arrowDown
//                        source: styleData.pressed ? "img/arrow_up_hover.png" : "img/arrow_up.png"
//                        anchors.horizontalCenter: parent.horizontalCenter
//                        anchors.verticalCenter: parent.verticalCenter
//                    }
//                }

//                incrementControl : Rectangle {
//                    id: scrollHigher
//                    width: 15
//                    height: 15
//                    color: "#343434"

//                    Image {
//                        id: arrowUp
//                        source: styleData.pressed ? "img/arrow_down_hover.png" : "img/arrow_down.png"
//                        anchors.horizontalCenter: parent.horizontalCenter
//                        anchors.verticalCenter: parent.verticalCenter
//                    }
//                }
//            }

////            TableViewColumn {
////                title: "Owner"
////                role: name
////                visible: true
////            }

////            TableViewColumn {
////                title: "Name"

////            }

//            itemDelegate: Item {
//                Text {
//                    text: model.object.name
//                    color: styleData.textColor
//                }
//            }

//            onClicked: {
//                console.log(model.get(row).name)
//            }

//            model: root.model.fileItems
//        }
//    }
}
