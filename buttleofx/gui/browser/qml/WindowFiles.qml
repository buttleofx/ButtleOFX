import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.0
import ButtleFileModel 1.0

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
    property bool viewGrid: true
    signal changeSelectedList(variant selected)
    property int itemIndex: 0
    property string fileName

    Menu {
        id: creation

        MenuItem {
            text: "Create a Directory"
            onTriggered: {
                fileModel.createFolder(fileModel.folder + "/New Directory")
                //Update the folder to see the new directory
                fileModel.updateFileItems(winFile.folder)
            }
        }
    }

    Menu {
        id: options

        MenuItem {
            text: "Rename"
            onTriggered: {
                //Open a TextEdit
                //renameMessage.open()

                fileModel.changeFileName("New Name", itemIndex)
                //Update the folder
                fileModel.updateFileItems(winFile.folder)
            }
        }
        MenuItem {
            text: "Delete"
            onTriggered: {
                deleteMessage.open()
                fileModel.updateFileItems(winFile.folder)
            }
        }
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
        visible: viewGrid ? false : true

        GridView {
            id: gridview
            height : parent.height
            width : parent.width
            cellWidth: 150
            visible: viewGrid ? false : true

            model: fileModel.fileItems
            delegate:
                Component {

                    Rectangle {
                        id: fileInColumn
                        color: model.object.isSelected ? "#00b2a1" : "transparent"
                        radius: 5
                        height: 80
                        width: 125

                        property variant selectedFiles

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

                            Text {
                                id: textInColumn
                                text: model.object.fileName
                                color: model.object.isSelected ? "black" : "white"
                                font.bold: model.object.isSelected
                                width: 120
                                elide: Text.ElideRight
                                horizontalAlignment: Text.AlignHCenter
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
                                if (mouse.button == Qt.RightButton)
                                    options.popup()
                                    winFile.fileName = textInColumn.text

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
                                model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
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
        visible: viewGrid

        ListView {
            id: listview
            height : parent.height
            width : parent.width
            visible: viewGrid

            model: fileModel.fileItems
            delegate: Component {
                Rectangle {
                    id: fileInRow
                    color: model.object.isSelected ? "#00b2a1" : "transparent"
                    radius: 5
                    height: 25
                    width: listview.width

                    property variant selectedFiles


                    Row {
                        width: parent.width
                        spacing: 10
                        Image {
                            x: 25
                            source: model.object.fileType == "Folder" ? "../../img/buttons/browser/folder-icon.png" : "file:///" + model.object.filepath
                            sourceSize.width: 20
                            sourceSize.height: 20
                        }

                        Text {
                            id: textInRow
                            text: model.object.fileName
                            color: model.object.isSelected ? "black" : "white"
                            font.bold: model.object.isSelected
                            width: parent.width
                            elide: Text.ElideRight

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
                            if (mouse.button == Qt.RightButton)
                                options.popup()
                                winFile.fileName = textInRow.text

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
                            model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
                        }
                    }
                }// end Rectangle
            }//endComponent
        }
    }

    MessageDialog {
        id: deleteMessage
        title: "Delete?"
        icon: StandardIcon.Warning
        text: "Do you really want to delete " + winFile.fileName + "?"
        standardButtons: StandardButton.Yes | StandardButton.No
        onYes: {
            fileModel.deleteItem(itemIndex)
            //fileModel.updateFileItems(winFile.folder)
            console.log("deleted")
            deleteMessage.close()
        }
        onNo: {
            console.log("didn't delete")
            deleteMessage.close()
        }
    }

    MessageDialog {
        id: renameMessage
        title: "Rename"
        icon: StandardIcon.Question
        text: "Please enter the new name of " + winFile.fileName + ":"

        /*TextInput {
            id: newName
            text: model.object.fileName
            color: "white"
            width: parent.width
            selectByMouse: true
            selectionColor: "#00b2a1"
            onFocusChanged:{
                texteditPath.focus ? selectAll() : deselect()
            }
        }*/

        standardButtons: StandardButton.Ok | StandardButton.Cancel
        onAccepted: {
            fileModel.changeFileName(newName.text, itemIndex)
            console.log("Renamed")
            renameMessage.close()
        }
        onRejected: {
            console.log("didn't Rename")
            renameMessage.close()
        }
    }

}
