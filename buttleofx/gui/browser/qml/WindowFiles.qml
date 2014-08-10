import QtQuick 2.1
import QtQuick.Controls 1.0
import ButtleFileModel 1.0
import QtQuick.Dialogs 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0


Rectangle {
    id: winFile
    color: fileModel.exists ? "black" : "lightgrey"

    property string folder: fileModel.firstFolder()
    signal goToFolder(string newFolder)
    property string filterName
    signal changeFileFolder(string fileFolder)
    signal changeNbFilesInSeq(int nb)
    property bool viewList: false
    signal changeSelectedList(variant selected)
    property int itemIndex: 0
    property bool showSeq: false
    property int nbCell: viewList ? 1 : gridview.width/gridview.cellWidth

    function showEditFile(pos) {
        fileInfo.visible = true
        fileInfo.x = mainWindowQML.x + pos.x - 5
        fileInfo.y = mainWindowQML.y + pos.y - 5
    }

    function enterFolder() {
        var lastSelected = fileModel.getLastSelected()
        if (lastSelected.getFileType() == 'Folder') {
            winFile.goToFolder(lastSelected.getFilepath())
        }
    }

    function forceActiveFocusOnCreate() {
        fileModel.createFolder(fileModel.folder + "/New Directory")
    }

    function forceActiveFocusOnDelete() {
        fileModel.deleteItem(itemIndex)
        winFile.forceActiveFocusOnRefresh()
    }

    function selectItem(index) {
        fileModel.selectItem(index)
        var sel = fileModel.getSelectedItems()

        // If it's an image, we assign it to the viewer
        if (sel && !sel.isEmpty()) {
            if (sel.get(0).fileType != "Folder" && sel.get(0).getSupported()) {
                player.changeViewer(11) // We come to the temporary viewer
                // We save the last node wrapper of the last view
                player.lastNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(player.lastView)

                readerNode.nodeWrapper = _buttleData.nodeReaderWrapperForBrowser(sel.get(0).filepath)

                _buttleData.currentGraphIsGraphBrowser()
                _buttleData.currentGraphWrapper = _buttleData.graphBrowserWrapper

                _buttleData.currentViewerNodeWrapper = readerNode.nodeWrapper
                _buttleData.currentViewerFrame = 0
                // We assign the node to the viewer, at the frame 0
                _buttleData.assignNodeToViewerIndex(readerNode.nodeWrapper, 10)
                _buttleData.currentViewerIndex = 10 // We assign to the viewer the 10th view
                _buttleEvent.emitViewerChangedSignal()
            }
        }
    }

    function forceActiveFocusOnRefresh() {
        fileModel.updateFileItems(fileModel.folder)
        winFile.selectItem(itemIndex)
    }

    function forceActiveFocusOnChangeIndexOnRight() {
        if (itemIndex < fileModel.size) {
            winFile.selectItem(++itemIndex)
        }
    }

    function forceActiveFocusOnChangeIndexOnLeft() {
        if (itemIndex > 0) {
            winFile.selectItem(--itemIndex)
        }
    }

    function forceActiveFocusOnChangeIndexOnDown() {
        if (itemIndex + winFile.nbCell  < fileModel.size) {
            itemIndex += winFile.nbCell
            winFile.selectItem(itemIndex)
        } else {
            itemIndex = fileModel.size
            winFile.selectItem(itemIndex)
        }
    }

    function forceActiveFocusOnChangeIndexOnUp() {
        if (itemIndex - winFile.nbCell  >= 0) {
            itemIndex -= winFile.nbCell
            winFile.selectItem(itemIndex)
        } else {
            itemIndex = 0
            winFile.selectItem(itemIndex)
        }
    }

    MouseArea {
        anchors.fill: parent

        onClicked: {
            forceActiveFocus()
            // TODO: unselect
        }
    }

    Menu {
        id: creation

        MenuItem {
            text: "Create a Directory"

            onTriggered: {
                fileModel.createFolder(fileModel.folder + "/New Directory")
            }
        }
    }


    QtObject {
        id: readerNode
        property variant nodeWrapper
    }

    FileModelBrowser {
        id: fileModel
        folder: winFile.folder
        nameFilter: winFile.filterName
        showSeq: winFile.showSeq

        onFolderChanged: {
            winFile.changeFileFolder(fileModel.parentFolder)
            winFile.changeSelectedList(fileModel.getSelectedItems())
            winFile.selectItem(0)
            itemIndex = 0
        }
        onNameFilterChanged: {
            winFile.changeFileFolder(fileModel.parentFolder)
            winFile.changeSelectedList(fileModel.getSelectedItems())
            winFile.selectItem(0)
            itemIndex = 0
        }
        onShowSeqChanged: {
            winFile.changeFileFolder(fileModel.parentFolder)
            winFile.changeSelectedList(fileModel.getSelectedItems())
            winFile.selectItem(0)
            itemIndex = 0
        }
    }

    FileInfo {
        id: fileInfo
        visible: false

        onRefreshFolder: {
            winFile.forceActiveFocusOnRefresh()
        }
        onDeleteItem: {
            winFile.forceActiveFocusOnDelete()
        }
    }

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.RightButton

        onClicked: {
            if (mouse.button == Qt.RightButton)
                creation.popup()
        }
    }

    Text {
        id: hack_fontMetrics
        text: "A"
        visible: false
    }

    // Code for the (default) grid  layout
    ScrollView {
        anchors.fill: parent
        anchors.topMargin: 5
        anchors.bottomMargin: 5
        height: 120
        width: 110
        visible: viewList ? false : true

        style: ScrollViewStyle {
            scrollBarBackground: Rectangle {
                id: scrollBar
                width: 15
                color: "#212121"
                border.width: 1
                border.color: "#333"
            }

            decrementControl : Rectangle {
                id: scrollLower
                width: 15
                height: 15
                color: styleData.pressed ? "#212121" : "#343434"
                border.width: 1
                border.color: "#333"
                radius: 3

                Image {
                    id: arrow
                    source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                    x: 4
                    y: 4
                }
            }

            incrementControl : Rectangle {
                id: scrollHigher
                width: 15
                height: 15
                color: styleData.pressed ? "#212121" : "#343434"
                border.width: 1
                border.color: "#333"
                radius: 3

                Image {
                    id: arrow
                    source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                    x: 4
                    y: 4
                }
            }
        }

        GridView {
            id: gridview
            width: parent.width
            height: parent.height
            cellWidth: 120
            cellHeight: cellWidth
            property int gridMargin: 4
            visible: !viewList
            boundsBehavior: Flickable.StopAtBounds
            flickableDirection: Flickable.VerticalFlick
            interactive: false
            currentIndex: -1
            cacheBuffer: 10 * cellHeight  // Caches 10 lines below and above

            property int previousIndex: -1

            model: fileModel.fileItems

            delegate: Component {
                id: componentInColumn

                Rectangle {
                    id: rootFileItem
                    color: model.object.isSelected ? "#00b2a1" : "transparent"
                    width: gridview.cellWidth - gridview.gridMargin
                    height: gridview.cellHeight - gridview.gridMargin
                    radius: 5
                    objectName: index
                    property variant selectedFiles

                    /*DropArea {
                        id: moveItemInColumn
                        anchors.fill: parent
                        objectName: model.object.filepath
                        keys: ["internFileDrag"]

                        onDropped: {
                            console.debug("file: " + Drag.source.objectName)
                            console.debug("Index: " + drop.source.objectName)
                            //fileModel.moveItem(drop.source.objectName, )
                        }
                    }*/

                    Drag.active: rootFileItem_mouseArea.drag.active
                    Drag.hotSpot.x: 20
                    Drag.hotSpot.y: 20
                    // Drag.dragType: Drag.Automatic
                    // Drag.mimeData: {"urls": [rootFileItem.selectedFiles]}
                    // Drag.mimeData: {"text/plain": file.filePath, "text/uri-list": ""}
                    // Drag.keys: "text/uri-list"
                    Drag.keys: "internFileDrag"

                    StateGroup {
                        id: fileStateColumn

                        states:
                        State {
                            name: "dragging"
                            when: rootFileItem_mouseArea.pressed
                            PropertyChanges { target: rootFileItem; x: rootFileItem.x; y: rootFileItem.y }
                        }
                    }

                    MouseArea {
                        id: rootFileItem_mouseArea
                        anchors.fill: parent
                        acceptedButtons: Qt.LeftButton | Qt.RightButton
                        onReleased: rootFileItem.Drag.drop()
                        drag.target: rootFileItem

                        onPressed: {
                            rootFileItem.forceActiveFocus()
                            winFile.itemIndex = index

                            if (mouse.button == Qt.RightButton)
                                winFile.showEditFile(rootFileItem_mouseArea.mapToItem(null, mouse.x, mouse.y))
                            fileModel.selectItem(index)
                            fileInfo.currentFile = fileModel.getSelectedItems() ? fileModel.getSelectedItems().get(0) : undefined
                            // options.popup()


                            // If shift:
                            if (mouse.modifiers & Qt.ShiftModifier)
                                fileModel.selectItemsByShift(gridview.previousIndex, index)

                            gridview.previousIndex = index
                            // If ctrl:
                            if (mouse.modifiers & Qt.ControlModifier)
                                fileModel.selectItems(index)
                            else if (!(mouse.modifiers & Qt.ShiftModifier))
                                fileModel.selectItem(index)

                            var sel = fileModel.getSelectedItems()
                            var selection = new Array()

                            for (var selIndex = 0; selIndex < sel.count; ++selIndex) {
                                selection[selIndex] = sel.get(selIndex).filepath
                            }

                            rootFileItem.selectedFiles = selection
                            winFile.changeSelectedList(sel)

                            // If it's an image, we assign it to the viewer
                            if (model.object.fileType != "Folder" && model.object.getSupported()) {
                                player.changeViewer(11) // We come to the temporary viewer
                                // We save the last node wrapper of the last view
                                player.lastNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(player.lastView)
                                readerNode.nodeWrapper = _buttleData.nodeReaderWrapperForBrowser(model.object.filepath)

                                _buttleData.currentGraphIsGraphBrowser()
                                _buttleData.currentGraphWrapper = _buttleData.graphBrowserWrapper

                                _buttleData.currentViewerNodeWrapper = readerNode.nodeWrapper
                                _buttleData.currentViewerFrame = 0
                                // We assign the node to the viewer, at the frame 0
                                _buttleData.assignNodeToViewerIndex(readerNode.nodeWrapper, 10)
                                _buttleData.currentViewerIndex = 10 // We assign to the viewer the 10th view
                                _buttleEvent.emitViewerChangedSignal()
                            }
                        }

                        onDoubleClicked: {
                            // If it's an image, we create a node
                            if (model.object.fileType != "Folder" && model.object.getSupported()) {
                                _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                _buttleData.currentGraphIsGraph()

                                // If before the viewer was showing an image from the browser, we change the currentView
                                if (_buttleData.currentViewerIndex > 9) {
                                    _buttleData.currentViewerIndex = player.lastView

                                    if (player.lastNodeWrapper != undefined)
                                        _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                                    player.changeViewer(player.lastView)
                                }

                                _buttleManager.nodeManager.dropFile(model.object.filepath, 10, 10)
                            } else if (model.object.fileType == "Folder") {
                                winFile.goToFolder(model.object.filepath)
                            }
                        }
                    }

                    ColumnLayout {
                        id: file
                        spacing: 0
                        anchors.fill: parent

                        Item {
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            Rectangle {
                                anchors.fill: parent
                                anchors.margins: 4
                                property int minSize: Math.min(width, height)

                                color: if (thumbnail.status == Image.Error)
                                           "red"
                                       else if (thumbnail.status == Image.Null)
                                           "lightred"
                                       else if (thumbnail.status == Image.Loading)
                                           "#33FFFFFF"
                                       else
                                           "transparent"

                                Rectangle {
                                    // TODO replace with an image
                                    id: loading
                                    anchors.centerIn: parent
                                    width: 12
                                    height: width
                                    visible: !thumbnail.isFolder && thumbnail.status == Image.Loading
                                    // source: "images/loading.png"

                                    NumberAnimation on rotation {
                                        from: 0
                                        to: 360
                                        running: loading.visible == true
                                        loops: Animation.Infinite
                                        duration: 1000
                                    }

                                    color: "lightblue"
                                }

                                Image {
                                    id: thumbnail
                                    property bool isFolder: model.object.fileType == "Folder"
                                    source: model.object.fileImg
                                    asynchronous: true
                                    // cache: false

                                    sourceSize.width: isFolder ? parent.minSize : -1
                                    sourceSize.height: isFolder ? parent.minSize : -1
                                    anchors.fill: parent
                                    fillMode: Image.PreserveAspectFit
                                    smooth: true
                                    opacity: isFolder || status == Image.Ready ? 1 : 0

                                    Behavior on opacity { PropertyAnimation { duration: 300 } }
                                }
                            }
                        }

                        Item {
                            Layout.fillWidth: true
                            implicitHeight: hack_fontMetrics.height * 3 // 3 lines of text

                            Rectangle {
                                id: filename_background
                                width: filename_text.width
                                height: filename_text.paintedHeight

                                color: "white"
                                radius: 2

                                visible: filename_text.activeFocus
                            }

                            Text {
                                id: filename_text
                                horizontalAlignment: Text.AlignHCenter
                                anchors.fill: parent
                                text: model.object.fileName
                                color: model.object.isSelected ? "black" : "white"
                                font.bold: model.object.isSelected
                                textFormat: Text.PlainText
                                wrapMode: Text.Wrap

                                clip: !activeFocus
                                z: 9999  // TODO: need another solution to be truly on top.
                            }
                        }
                    }
                }
            }
        }
    }

    // Code for the list layout
    ScrollView {
        anchors.fill: parent
        anchors.topMargin: 5
        anchors.bottomMargin: 5
        height: 120
        width: 110
        visible: viewList

        style: ScrollViewStyle {
            scrollBarBackground: Rectangle {
                id: scrollBar2
                width: 15
                color: "#212121"
                border.width: 1
                border.color: "#333"
            }
            decrementControl : Rectangle {
                id: scrollLower2
                width: 15
                height: 15
                color: styleData.pressed ? "#212121" : "#343434"
                border.width: 1
                border.color: "#333"
                radius: 3

                Image {
                    id: arrowBis2
                    source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                    x: 4
                    y: 4
                }
            }
            incrementControl : Rectangle {
                id: scrollHigher2
                width: 15
                height: 15
                color: styleData.pressed ? "#212121" : "#343434"
                border.width: 1
                border.color: "#333"
                radius: 3

                Image {
                    id: arrow
                    source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                    x: 4
                    y: 4
                }
            }
        }

        ListView {
            id: listview
            height: parent.height
            width: parent.width
            visible: viewList
            boundsBehavior: Flickable.StopAtBounds
            flickableDirection: Flickable.VerticalFlick
            interactive: false
            currentIndex: -1

            property int previousIndex: -1

            model: fileModel.fileItems
            delegate: Component {

                Rectangle {
                    id: fileInRow
                    color: model.object.isSelected ? "#00b2a1" : "transparent"
                    radius: 5
                    height: hack_fontMetrics.height * 1.5 // 1.5 lines of text
                    width: listview.width

                    property variant selectedFiles
                    property variant currentFile: model.object
                    // property variant filePath: model.object.filepath

                    /*DropArea {
                        id: moveItemInRow
                        anchors.fill: parent
                        keys: ["internFileDrag"]

                        onDropped: {
                            console.debug("Drag: " + drag.source.filepath)
                            //fileModel.moveItem(itemIndex, drag.source.filepath)
                        }
                    }*/

                    RowLayout {
                        anchors.fill: parent
                        spacing: 10

                        Image {
                            source: model.object.fileImg
                            sourceSize.width: parent.height
                            sourceSize.height: parent.height
                            Layout.fillHeight: true
                            Layout.preferredWidth: parent.height
                            fillMode: Image.PreserveAspectFit
                        }

                        Text {
                            id: textInRow
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.minimumWidth: 40

                            text: model.object.fileName
                            color: model.object.isSelected ? "black" : "white"
                            font.bold: model.object.isSelected
                        }
                    }

                    Drag.active: dragMouseAreaRow.drag.active
                    Drag.hotSpot.x: 20
                    Drag.hotSpot.y: 20
                    // Drag.dragType: Drag.Automatic
                    // Drag.mimeData: {"urls": [fileInRow.selectedFiles]}
                    // Drag.mimeData: {"text/plain": file.filePath, "text/uri-list": ""}
                    // Drag.keys: "text/uri-list"
                    Drag.keys: "internFileDrag"

                    StateGroup {
                        id: fileStateRow

                        states: State {
                            name: "dragging"
                            when: dragMouseAreaRow.pressed
                            PropertyChanges { target: fileInRow; x: fileInRow.x; y: fileInRow.y }
                        }
                    }

                    MouseArea {
                        id: dragMouseAreaRow
                        anchors.fill: parent
                        acceptedButtons: Qt.LeftButton | Qt.RightButton
                        onReleased: fileInRow.Drag.drop()
                        drag.target: fileInRow

                        onPressed: {
                            winFile.itemIndex = index

                            if (mouse.button == Qt.RightButton)
                                winFile.showEditFile(dragMouseAreaRow.mapToItem(null, mouse.x, mouse.y))
                            fileModel.selectItem(index)
                            fileInfo.currentFile = fileModel.getSelectedItems() ? fileModel.getSelectedItems().get(0) : undefined

                            // If shift:
                            if (mouse.modifiers & Qt.ShiftModifier)
                                fileModel.selectItemsByShift(listview.previousIndex, index)

                            listview.previousIndex = index

                            // If ctrl:
                            if (mouse.modifiers & Qt.ControlModifier)
                                fileModel.selectItems(index)
                            else if (!(mouse.modifiers & Qt.ShiftModifier))
                                fileModel.selectItem(index)

                            var sel = fileModel.getSelectedItems()
                            var selection = new Array()
                            for (var selIndex = 0; selIndex < sel.count; ++selIndex) {
                                selection[selIndex] = sel.get(selIndex).filepath
                            }

                            fileInRow.selectedFiles = selection
                            winFile.changeSelectedList(sel)

                            // If it's an image, we assign it to the viewer
                            if (model.object.fileType != "Folder" && model.object.getSupported()) {
                                player.changeViewer(11) // We come to the temporary viewer
                                // We save the last node wrapper of the last view
                                player.lastNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(player.lastView)
                                readerNode.nodeWrapper = _buttleData.nodeReaderWrapperForBrowser(model.object.filepath)

                                _buttleData.currentGraphIsGraphBrowser()
                                _buttleData.currentGraphWrapper = _buttleData.graphBrowserWrapper

                                _buttleData.currentViewerNodeWrapper = readerNode.nodeWrapper
                                _buttleData.currentViewerFrame = 0
                                // We assign the node to the viewer, at the frame 0
                                _buttleData.assignNodeToViewerIndex(readerNode.nodeWrapper, 10)
                                _buttleData.currentViewerIndex = 10 // We assign to the viewer the 10th view
                                _buttleEvent.emitViewerChangedSignal()
                            }
                        }

                        onDoubleClicked: {
                            // If it's an image, we create a node
                            if (model.object.fileType != "Folder" && model.object.getSupported()) {
                                _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                _buttleData.currentGraphIsGraph()

                                // If before the viewer was showing an image from the browser, we change the currentView
                                if (_buttleData.currentViewerIndex > 9){
                                    _buttleData.currentViewerIndex = player.lastView

                                    if (player.lastNodeWrapper != undefined)
                                        _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                                    player.changeViewer(player.lastView)
                                }

                                _buttleManager.nodeManager.dropFile(model.object.filepath, 10, 10)
                            } else if (model.object.fileType == "Folder") {
                                winFile.goToFolder(model.object.filepath)
                            }
                        }
                    }
                }
            }
        }
    }
}
