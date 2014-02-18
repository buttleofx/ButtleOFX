import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.0
import ButtleFileModel 1.0
import QtQuick.Controls.Styles 1.0

Rectangle {
    id: winFile
    color: fileModel.exists ? "black" : "lightgrey"

    property string folder
    signal goToFolder(string newFolder)
    property string filterName
    signal changeFileFolder(string fileFolder)
    property string file
    signal changeFile(string file)
    signal changeFileType(string fileType)
    signal changeFileSize(real fileSize)
    property bool viewList: false
    signal changeSelectedList(variant selected)
    property int itemIndex: 0
    property string fileName

    function forceActiveFocusOnCreate() {
        fileModel.createFolder(fileModel.folder + "/New Directory")
    }

    function forceActiveFocusOnRename() {
        viewList ? listview.currentItem.forceActiveFocusInRow() : gridview.currentItem.forceActiveFocusInColumn()
    }

    function forceActiveFocusOnDelete() {
        fileModel.deleteItem(itemIndex)
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

        onFolderChanged: {
            fileModel.selectItem(0)
            winFile.changeFileFolder(fileModel.parentFolder)
        }
        onNameFilterChanged: {
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
                            Image{
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
                            Image{
                                id: arrow
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                                x:4
                                y:4
                            }
                        }
                    }

        GridView {
            id: gridview
            height : parent.height
            width : parent.width
            cellWidth: 150
            visible: viewList ? false : true

            model: fileModel.fileItems
            delegate:
                Component {
                    id: componentInColumn

                    Rectangle {
                        id: fileInColumn
                        color: model.object.isSelected ? "#00b2a1" : "transparent"
                        radius: 5
                        height: 80
                        width: 125
                        objectName: index

                        property variant selectedFiles
                        property variant filePath: model.object.filepath

                        function forceActiveFocusInColumn() {
                            textInColumn.forceActiveFocus()
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


                        Column {
                            id : file
                            anchors.horizontalCenter: parent.horizontalCenter

                            Image {
                                x: 25
                                source: model.object.fileType == "Folder" ? "../../img/buttons/browser/folder-icon.png" : "file:///" + model.object.filepath
                                sourceSize.width: 40
                                sourceSize.height: 40

                                anchors.horizontalCenter: parent.horizontalCenter
                            }

                            TextInput {
                                id: textInColumn
                                text: model.object.fileName
                                color: model.object.isSelected ? "black" : "white"
                                font.bold: model.object.isSelected
                                width: 120
                                horizontalAlignment: TextInput.AlignHCenter
                                selectByMouse: true
                                selectionColor: "#5a5e6b"

                                onFocusChanged:{
                                    textInColumn.focus ? selectAll() : deselect()
                                }

                                onAccepted: {
                                    textInColumn.selectAll()
                                    fileModel.changeFileName(textInColumn.getText(0, textInColumn.cursorPosition + 1), itemIndex)
                                    textInColumn.forceActiveFocus()
                                }
                            }
                        }// endColumn

                        Drag.active: dragMouseAreaColumn.drag.active
                        Drag.hotSpot.x: 20
                        Drag.hotSpot.y: 20
                        //Drag.dragType: Drag.Automatic
                        Drag.mimeData: {"urls": [fileInColumn.selectedFiles]}
                        //Drag.mimeData: {"text/plain": file.filePath, "text/uri-list": ""}
                        // Drag.keys: "text/uri-list"
                        Drag.keys: "internFileDrag"

                        StateGroup {
                          id: fileStateColumn
                          states: State {
                              name: "dragging"
                              when: dragMouseAreaColumn.pressed
                              PropertyChanges { target: fileInColumn; x: fileInColumn.x; y: fileInColumn.y }
                          }
                        }

                        MouseArea {
                            id: dragMouseAreaColumn
                            anchors.fill: parent
                            acceptedButtons: Qt.LeftButton | Qt.RightButton
                            onReleased: fileInColumn.Drag.drop()
                            drag.target: fileInColumn

                            onClicked: {
                                winFile.changeFileSize(0)
                                if (mouse.button == Qt.RightButton)
                                    options.popup()
                                    winFile.fileName = textInColumn.text
                                    winFile.itemIndex = index

                                //if shift:
                                if(mouse.modifiers & Qt.ShiftModifier)
                                    fileModel.selectItemsByShift(gridview.currentIndex, index)

                                gridview.currentIndex = index
                                winFile.changeFile(model.object.filepath)
                                winFile.changeFileType(model.object.fileType)
                                //if ctrl:
                                if(mouse.modifiers & Qt.ControlModifier)
                                    fileModel.selectItems(index)

                                else if(!(mouse.modifiers & Qt.ShiftModifier))
                                    fileModel.selectItem(index)
                                    winFile.changeFileSize(model.object.fileSize)

                                var sel = fileModel.getSelectedItems()
                                var selection = new Array()
                                for(var selIndex = 0; selIndex < sel.count; ++selIndex)
                                {
                                    selection[selIndex] = sel.get(selIndex).filepath
                                }
                                fileInColumn.selectedFiles = selection
                                winFile.changeSelectedList(sel)
                            }

                            onDoubleClicked: {
                                // if it's an image, we assign it to the viewer
                                 if (model.object.fileType != "Folder"){
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
                                 else{
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
                                    textInColumn.forceActiveFocus()
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

                    }
                }//endComponent
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
                            Image{
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
                            Image{
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
                    property variant filePath: model.object.filepath

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
                            source: model.object.fileType == "Folder" ? "../../img/buttons/browser/folder-icon.png" : "file:///" + model.object.filepath
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

                        onClicked: {
                            winFile.changeFileSize(0)
                            if (mouse.button == Qt.RightButton)
                                options.popup()
                                winFile.fileName = textInRow.text
                                winFile.itemIndex = index

                            //if shift:
                            if(mouse.modifiers & Qt.ShiftModifier)
                                fileModel.selectItemsByShift(listview.currentIndex, index)

                            listview.currentIndex = index
                            winFile.changeFile(model.object.filepath)
                            winFile.changeFileType(model.object.fileType)
                            //if ctrl:
                            if(mouse.modifiers & Qt.ControlModifier)
                                fileModel.selectItems(index)

                            else if(!(mouse.modifiers & Qt.ShiftModifier))
                                fileModel.selectItem(index)
                                winFile.changeFileSize(model.object.fileSize)

                            var sel = fileModel.getSelectedItems()
                            var selection = new Array()
                            for(var selIndex = 0; selIndex < sel.count; ++selIndex)
                            {
                                selection[selIndex] = sel.get(selIndex).filepath
                            }
                            fileInRow.selectedFiles = selection
                            winFile.changeSelectedList(sel)
                        }

                        onDoubleClicked: {
                            // if it's an image, we assign it to the viewer
                             if (model.object.fileType != "Folder"){
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
                             else{
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
