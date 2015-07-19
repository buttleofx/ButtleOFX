import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0
import QtQuick.Dialogs 1.1

Rectangle {
    id: root
    color: "transparent"

    // defaults slots
    function onItemClickedSlot(pathImg){
        console.debug("handleGraphViewerClick")
        _buttleData.setActiveBrowserFile(pathImg)
        _buttleEvent.emitViewerChangedSignal()
    }

    function onItemDoubleClickedSlot(absolutePath){
        console.debug("handleGraphViewerDoubleClick")
        _buttleData.setActiveGraphId("graphEditor")
        _buttleManager.nodeManager.dropFile(absolutePath, 10, 10)
    }

    signal itemClicked(string absolutePath, string pathImg, bool isFolder, bool isSupported)
    signal itemDoubleClicked(string absolutePath, string pathImg, bool isFolder, bool isSupported)
    signal pushVisitedFolder(string path)

    Keys.onEscapePressed: root.model.unselectAllItems()
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

    Keys.onPressed: {
        //TODO: temporary shortcut menu: overload ambiguous
    }

    Menu{
        //TODO: REDO architecture
        id:actionsMenu
        property bool showActionOnItem: false

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
                var destination=""
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

            boundsBehavior: Flickable.StopAtBounds
            focus: true
        }
    }

    Component {
        id: component

        Rectangle {
            id: component_container

            width: grid.cellWidth - 20
            height: icon.height + fileName.height

            color: (model.object.isSelected) ? "#666666" : "transparent"
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
