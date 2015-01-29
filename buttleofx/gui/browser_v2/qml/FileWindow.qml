import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0


Rectangle {
    id: root

    color: "transparent"

    function pushVisitedFolder(path){
        if (visitedFolderList.count === 0){
            // Save path of the current folder
            visitedFolderList.append({"url": root.model.currentPath})
        }

        visitedFolderList.append({"url": path})
        ++ visitedFolderListIndex
    }

    function handleGraphViewerClick(pathImg){
        player.changeViewer(11) // We come to the temporary viewer
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

    function handleGraphViewerDoubleClick(pathImg){
        _buttleData.currentGraphWrapper = _buttleData.graphWrapper
        _buttleData.currentGraphIsGraph()

        // If before the viewer was showing an image from the browser, we change the currentView
        if (_buttleData.currentViewerIndex > 9){
            _buttleData.currentViewerIndex = player.lastView

            if (player.lastNodeWrapper != undefined)
                _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
            player.changeViewer(player.lastView)
        }
        _buttleManager.nodeManager.dropFile(pathImg, 10, 10)
    }

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        onClicked:{
            if(mouse.button == Qt.RightButton)
                actionsMenu.popup()
            if(mouse.button == Qt.LeftButton)
                root.model.unselectAllItems()
        }
    }

    Menu{
        //TODO: REDO architecture
        id:actionsMenu

        MenuItem{
            text:"Copy"
            onTriggered: {
                _browserAction.handleCopy()
            }
        }
        MenuItem{
            text:"Cut"
            onTriggered: {
                _browserAction.handleMove()
            }
        }

        MenuItem{
            text:"Paste"
            onTriggered: {
                _browserAction.handlePaste()
            }
        }
        MenuItem{
            text:"Delete"
            onTriggered: {
                _browserAction.handleDelete()
            }
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

            cellWidth: 150
            cellHeight: 100

            // displayMarginBeginning: 20 // Available in QtQuick 2.3
            // displayMarginEnd: 20 // Available in QtQuick 2.3

            clip: true
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

                    visible: !(model.object.type === 1) && icon.status === Image.Loading

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

                        onClicked: {
                            if(mouse.button == Qt.RightButton){
                                actionsMenu.popup()
                                return
                            }

                            if(!model.object.isFolder()){
                                if (model.object.isSupported())
                                    handleGraphViewerClick(model.object.path)
                            }
                            if ((mouse.modifiers & Qt.ShiftModifier))
                                root.model.selectItemTo(index)
                            else if ((mouse.modifiers & Qt.ControlModifier))
                                model.object.isSelected = !model.object.isSelected
                            else
                                root.model.selectItem(index)
                        }

                        onDoubleClicked: {
                            if (model.object.isFolder()) {
                                root.pushVisitedFolder(model.object.path)
                                root.model.currentPath = model.object.path
                            }

                            // If it's an image, we create a node
                            else if (model.object.isSupported())
                                handleGraphViewerDoubleClick(model.object.path)
                        }
                    }
                }

                Text {
                    id: fileName

                    width: parent.width
                    height: paintedHeight

                    elide: (model.object.isSelected) ? Text.ElideNone : Text.ElideRight
                    anchors.horizontalCenter: parent.horizontalCenter
                    horizontalAlignment: Text.AlignHCenter

                    text: model.object.name
                    color: ((icon_mouseArea.containsMouse || text_mouseArea.containsMouse) ^ model.object.isSelected) ? "white" : "#BBBBBB"

                    wrapMode: Text.WrapAnywhere

                    MouseArea {
                        id: text_mouseArea
                        anchors.fill: parent

                        hoverEnabled: true

                        onClicked: {
                            if(!model.object.isFolder()){
                                if (model.object.isSupported())
                                    handleGraphViewerClick(model.object.path)
                            }

                            if ((mouse.modifiers & Qt.ShiftModifier))
                                root.model.selectItemTo(index)
                            else if ((mouse.modifiers & Qt.ControlModifier))
                                model.object.isSelected = !model.object.isSelected
                            else
                                root.model.selectItem(index)
                        }

                        onDoubleClicked: {
                            if (model.object.type === 1) { // Folder
                                root.pushVisitedFolder(model.object.path)
                                root.model.currentPath = model.object.path
                            }
                            else if (model.object.isSupported())
                                handleGraphViewerDoubleClick(model.object.path)
                        }
                    }
                }

                Component.onCompleted: {
                    fileName.width = fileName.contentWidth
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

