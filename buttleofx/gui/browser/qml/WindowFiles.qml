import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0

import ButtleFileModel 1.0


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
    property string fileName
    property bool showSeq: false
    property int nbCell: viewList ? 1 : gridview.width/gridview.cellWidth

    function forceActiveFocusOnCreate() {
        fileModel.createFolder(fileModel.folder + "/New Directory")
    }

    function forceActiveFocusOnRename() {
        viewList ? listview.currentItem.forceActiveFocusInRow() : gridview.currentItem.forceActiveFocusInColumn()
    }

    function forceActiveFocusOnDelete() {
        fileModel.deleteItem(itemIndex)
    }

    function forceActiveFocusOnRefresh() {
        fileModel.updateFileItems(fileModel.folder)
        fileModel.selectItem(0)
    }
    function forceActiveFocusOnChangeIndexOnRight() {
        if(itemIndex < fileModel.size) {
            fileModel.selectItem(itemIndex + 1)
            itemIndex ++
        }
    }
    function forceActiveFocusOnChangeIndexOnLeft() {
        if(itemIndex > 0) {
            fileModel.selectItem(itemIndex - 1)
            itemIndex --
        }
    }

    function forceActiveFocusOnChangeIndexOnDown() {
        if(itemIndex + winFile.nbCell  < fileModel.size) {
            itemIndex += winFile.nbCell
            fileModel.selectItem(itemIndex)
        }else {
            itemIndex = fileModel.size
            fileModel.selectItem(itemIndex)
        }
    }
    function forceActiveFocusOnChangeIndexOnUp() {
        if(itemIndex - winFile.nbCell  >= 0) {
            itemIndex -= winFile.nbCell
            fileModel.selectItem(itemIndex)
        }else {
            itemIndex = 0
            fileModel.selectItem(itemIndex)
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
            fileModel.selectItem(0)
        }
        onNameFilterChanged: {
            winFile.changeFileFolder(fileModel.parentFolder)
            winFile.changeSelectedList(fileModel.getSelectedItems())
            fileModel.selectItem(0)
        }
        onShowSeqChanged: {
            winFile.changeFileFolder(fileModel.parentFolder)
            winFile.changeSelectedList(fileModel.getSelectedItems())
            fileModel.selectItem(0)
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
                            width:15
                            color: "#212121"
                            border.width: 1
                            border.color: "#333"
                        }
                        decrementControl : Rectangle {
                            id: scrollLower
                            width:15
                            height:15
                            color: styleData.pressed? "#212121" : "#343434"
                            border.width: 1
                            border.color: "#333"
                            radius: 3

                            Image {
                                id: arrow
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                                x:4
                                y:4
                            }
                        }
                        incrementControl : Rectangle {
                            id: scrollHigher
                            width:15
                            height:15
                            color: styleData.pressed? "#212121" : "#343434"
                            border.width: 1
                            border.color: "#333"
                            radius: 3
                            Image {
                                id: arrow
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                                x:4
                                y:4
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
            visible: ! viewList
            boundsBehavior: Flickable.StopAtBounds
            flickableDirection: Flickable.VerticalFlick
            interactive: false
            currentIndex: -1
            cacheBuffer: 10 * cellHeight  // caches 10 lines below and above

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
                    //property variant filePath: model.object.filepath

                    function forceActiveFocusInColumn() {
                        filename_textEdit.forceActiveFocus()
                    }

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
                    //Drag.dragType: Drag.Automatic
                    Drag.mimeData: {"urls": [rootFileItem.selectedFiles]}
                    //Drag.mimeData: {"text/plain": file.filePath, "text/uri-list": ""}
                    // Drag.keys: "text/uri-list"
                    Drag.keys: "internFileDrag"

                    StateGroup {
                        id: fileStateColumn
                        states: State {
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
                                options.popup()
                                winFile.fileName = filename_textEdit.text

                            //if shift:
                            if(mouse.modifiers & Qt.ShiftModifier)
                                fileModel.selectItemsByShift(gridview.previousIndex, index)

                            gridview.previousIndex = index
                            //if ctrl:
                            if(mouse.modifiers & Qt.ControlModifier)
                                fileModel.selectItems(index)

                            else if(!(mouse.modifiers & Qt.ShiftModifier))
                                fileModel.selectItem(index)

                            var sel = fileModel.getSelectedItems()
                            var selection = new Array()
                            for(var selIndex = 0; selIndex < sel.count; ++selIndex)
                            {
                                selection[selIndex] = sel.get(selIndex).filepath
                            }
                            rootFileItem.selectedFiles = selection
                            winFile.changeSelectedList(sel)

                            // if it's an image, we assign it to the viewer
                             if (model.object.fileType != "Folder") {
                                 player.changeViewer(11) // we come to the temporary viewer
                                 // we save the last node wrapper of the last view
                                 player.lastNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(player.lastView)

                                 readerNode.nodeWrapper = _buttleData.nodeReaderWrapperForBrowser(model.object.filepath)

                                 _buttleData.currentGraphIsGraphBrowser()
                                 _buttleData.currentGraphWrapper = _buttleData.graphBrowserWrapper

                                 _buttleData.currentViewerNodeWrapper = readerNode.nodeWrapper
                                 _buttleData.currentViewerFrame = 0
                                 // we assign the node to the viewer, at the frame 0
                                 _buttleData.assignNodeToViewerIndex(readerNode.nodeWrapper, 10)
                                 _buttleData.currentViewerIndex = 10 // we assign to the viewer the 10th view
                                 _buttleEvent.emitViewerChangedSignal()
                             }
                        }

                        onDoubleClicked: {
                            // if it's an image, we create a node
                             if (model.object.fileType != "Folder") {
                                 _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                 _buttleData.currentGraphIsGraph()
                                 // if before the viewer was showing an image from the browser, we change the currentView
                                 if (_buttleData.currentViewerIndex > 9){
                                     _buttleData.currentViewerIndex = player.lastView
                                     if (player.lastNodeWrapper != undefined)
                                         _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                                     player.changeViewer(player.lastView)
                                 }

                                 _buttleManager.nodeManager.dropFile(model.object.filepath, 10, 10)
                             } else {
                                 winFile.goToFolder(model.object.filepath)
                             }
                        }
                    }

                    Menu {
                        id: options

                        MenuItem {
                            text: "Rename"
                            onTriggered: {
                                //Open a TextEdit
                                filename_textEdit.forceActiveFocus()
                            }
                        }
                        MenuItem {
                            text: "Delete"
                            onTriggered: {
                                fileModel.deleteItem(itemIndex)
                                //deleteMessage.open()
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
                            Item {
                                anchors.fill: parent
                                anchors.margins: 4
                                property int minSize: Math.min(width, height)

                                Image {
                                    property bool isFolder: model.object.fileType == "Folder"
                                    source: isFolder ? model.object.fileImg : 'image://buttleofx/'+ model.object.filepath
                                    // Without tuttle // source: isFolder ? model.object.fileImg : "file:///" + model.object.fileImg

                                    asynchronous: true

                                    sourceSize.width: isFolder ? parent.minSize : -1
                                    sourceSize.height: isFolder ? parent.minSize : -1
                                    anchors.fill: parent
                                    fillMode: Image.PreserveAspectFit
                                    smooth: true
                                }

                            }
                        }

                        Item {
                            Layout.fillWidth: true
                            implicitHeight: hack_fontMetrics.height * 3 // 3 lines of text
                            Text {
                                id: hack_fontMetrics
                                text: "A"
                                visible: false
                            }
                            Rectangle {
                                id: filename_background
                                width: filename_textEdit.width
                                height: filename_textEdit.paintedHeight

                                color: "white"
                                radius: 2

                                visible: filename_textEdit.activeFocus
                            }
                            TextEdit {
                                id: filename_textEdit

                                horizontalAlignment: TextInput.AlignHCenter
                                anchors.fill: parent

                                text: model.object.fileName
                                property string origText: ""

                                color: model.object.isSelected ? "black" : "white"
                                font.bold: model.object.isSelected
                                textFormat: TextEdit.PlainText
                                wrapMode: TextEdit.Wrap

                                selectByMouse: activeFocus
                                selectionColor: "#5a5e6b"
                                clip: ! activeFocus
                                z: 9999  // TODO: need another solution to be truly on top.

                                onTextChanged: {
                                    // Hack to get the "Keys.onEnterPressed" event
                                    var hasEndline = (text.lastIndexOf("\n") != -1)
                                    if( hasEndline )
                                    {
                                        var newText = text.replace("\n", "")
                                        textAccepted(newText)
                                    }
                                }

                                onActiveFocusChanged: {
                                    if( filename_textEdit.activeFocus )
                                    {
                                        selectAll()
                                        origText = text
                                    }
                                    else
                                    {
                                        deselect()
                                        textAccepted(text)
                                    }
                                }
                                function textAccepted(newText) {
                                    if( origText != newText )
                                    {
                                        fileModel.changeFileName(newText, itemIndex)
                                    }
                                    origText = ""
                                }
                                MouseArea {
                                    id: filename_mouseArea
                                    width: filename_textEdit.width
                                    height: Math.max(filename_textEdit.width, filename_textEdit.paintedHeight)
                                    acceptedButtons: Qt.LeftButton
                                    enabled: ! filename_textEdit.activeFocus
                                    onPressed: {
                                        // forward to the rootFileItem
                                        rootFileItem_mouseArea.onPressed(mouse)
                                    }
                                    onDoubleClicked: {
                                        mouse.accepted = true
                                        filename_textEdit.forceActiveFocus()
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

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
                            width:15
                            color: "#212121"
                            border.width: 1
                            border.color: "#333"
                        }
                        decrementControl : Rectangle {
                            id: scrollLower2
                            width:15
                            height:15
                            color: styleData.pressed? "#212121" : "#343434"
                            border.width: 1
                            border.color: "#333"
                            radius: 3
                            Image{
                                id: arrowBis2
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                                x:4
                                y:4
                            }
                        }
                        incrementControl : Rectangle {
                            id: scrollHigher2
                            width:15
                            height:15
                            color: styleData.pressed? "#212121" : "#343434"
                            border.width: 1
                            border.color: "#333"
                            radius: 3

                            Image {
                                id: arrow
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                                x:4
                                y:4
                            }
                        }
                    }

        ListView {
            id: listview
            height : parent.height
            width : parent.width
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
                    height: 25
                    width: listview.width

                    function forceActiveFocusInRow() {
                        textInRow.forceActiveFocus()
                    }

                    property variant selectedFiles
                    property variant currentFile: model.object
                    //property variant filePath: model.object.filepath

                    /*DropArea {
                        id: moveItemInRow
                        anchors.fill: parent
                        keys: ["internFileDrag"]

                        onDropped: {
                            console.debug("Drag: " + drag.source.filepath)
                            //fileModel.moveItem(itemIndex, drag.source.filepath)
                        }
                    }*/

                    Row {
                        width: parent.width
                        spacing: 10
                        Image {
                            x: 25
                            //source: model.object.fileType == "Folder" ? model.object.fileImg : 'image://buttleofx'+ model.object.filepath
                            source: model.object.fileType == "Folder" ? model.object.fileImg : "file:///" + model.object.fileImg
                            sourceSize.width: 20
                            sourceSize.height: 20
                        }

                        TextInput {
                            id: textInRow
                            x: 10

                            text: model.object.fileName
                            color: model.object.isSelected ? "black" : "white"
                            font.bold: model.object.isSelected
                            width: parent.width

                            selectByMouse: true
                            selectionColor: "#5a5e6b"

                            onFocusChanged:{
                                textInRow.focus ? selectAll() : deselect()
                            }

                            onAccepted: {
                                textInRow.selectAll()
                                fileModel.changeFileName(textInRow.getText(0, textInRow.cursorPosition + 1), itemIndex)
                                textInRow.forceActiveFocus()
                            }
                        }
                    }// endRow

                    Drag.active: dragMouseAreaRow.drag.active
                    Drag.hotSpot.x: 20
                    Drag.hotSpot.y: 20
                    //Drag.dragType: Drag.Automatic
                    Drag.mimeData: {"urls": [fileInRow.selectedFiles]}
                    //Drag.mimeData: {"text/plain": file.filePath, "text/uri-list": ""}
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
                                options.popup()
                                winFile.fileName = textInRow.text

                            //if shift:
                            if(mouse.modifiers & Qt.ShiftModifier)
                                fileModel.selectItemsByShift(listview.previousIndex, index)

                            listview.previousIndex = index
                            //if ctrl:
                            if(mouse.modifiers & Qt.ControlModifier)
                                fileModel.selectItems(index)

                            else if(!(mouse.modifiers & Qt.ShiftModifier))
                                fileModel.selectItem(index)

                            var sel = fileModel.getSelectedItems()
                            var selection = new Array()
                            for(var selIndex = 0; selIndex < sel.count; ++selIndex)
                            {
                                selection[selIndex] = sel.get(selIndex).filepath
                            }
                            fileInRow.selectedFiles = selection
                            winFile.changeSelectedList(sel)

                            // if it's an image, we assign it to the viewer
                             if (model.object.fileType != "Folder") {
                                 player.changeViewer(11) // we come to the temporary viewer
                                 // we save the last node wrapper of the last view
                                 player.lastNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(player.lastView)

                                 readerNode.nodeWrapper = _buttleData.nodeReaderWrapperForBrowser(model.object.filepath)

                                 _buttleData.currentGraphIsGraphBrowser()
                                 _buttleData.currentGraphWrapper = _buttleData.graphBrowserWrapper

                                 _buttleData.currentViewerNodeWrapper = readerNode.nodeWrapper
                                 _buttleData.currentViewerFrame = 0
                                 // we assign the node to the viewer, at the frame 0
                                 _buttleData.assignNodeToViewerIndex(readerNode.nodeWrapper, 10)
                                 _buttleData.currentViewerIndex = 10 // we assign to the viewer the 10th view
                                 _buttleEvent.emitViewerChangedSignal()
                             }
                        }

                        onDoubleClicked: {
                            // if it's an image, we create a node
                             if (model.object.fileType != "Folder") {
                                 _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                 _buttleData.currentGraphIsGraph()
                                 // if before the viewer was showing an image from the browser, we change the currentView
                                 if (_buttleData.currentViewerIndex > 9){
                                     _buttleData.currentViewerIndex = player.lastView
                                     if (player.lastNodeWrapper != undefined)
                                         _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                                     player.changeViewer(player.lastView)
                                 }

                                 _buttleManager.nodeManager.dropFile(model.object.filepath, 10, 10)
                             } else {
                                 winFile.goToFolder(model.object.filepath)
                             }
                        }
                    }
                    Menu {
                        id: options

                        MenuItem {
                            text: "Rename"
                            onTriggered: {
                                //Open a TextEdit
                                textInRow.forceActiveFocus()
                            }
                        }
                        MenuItem {
                            text: "Delete"
                            onTriggered: {
                                fileModel.deleteItem(itemIndex)
                                //deleteMessage.open()
                            }
                        }
                    }
                }// end Rectangle
            }//endComponent
        }
    }

    /*MessageDialog {
        id: deleteMessage
        title: "Delete?"
        icon: StandardIcon.Warning
        text: "Do you really want to delete " + winFile.fileName + "?"
        standardButtons: StandardButton.No | StandardButton.Yes
        onYes: {
            //fileModel.deleteItem(itemIndex)
            console.log("deleted")
        }
        onNo: {
            console.log("didn't delete")
        }
    }*/
}
