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
                        id: background
                        color: model.object.isSelected ? "#00b2a1" : "transparent"
                        radius: 5
                        height: 80
                        width: 100

                        MouseArea {
                            id: mouseRegionImage
                            anchors.fill : parent
                            acceptedButtons: Qt.LeftButton | Qt.RightButton
                            onClicked: {
                                if (mouse.button == Qt.RightButton)
                                    options.popup()
                                    winFile.fileName = textElement.text

                                //if shift:
                                if(mouse.modifiers & Qt.ShiftModifier)
                                    fileModel.selectItemsByShift(gridview.currentIndex, index)

                                itemIndex = index
                                gridview.currentIndex = index
                                winFile.changeFile(model.object.filepath)
                                winFile.changeFileType(model.object.fileType)
                                //if ctrl:
                                if(mouse.modifiers & Qt.ControlModifier)
                                    fileModel.selectItems(index)

                                else if(!(mouse.modifiers & Qt.ShiftModifier))
                                    fileModel.selectItem(index)

                                var sel = fileModel.getSelectedItems()
                                console.debug("sel.count: " + sel.count)
                                for(var selIndex = 0; selIndex < sel.count; ++selIndex)
                                {
                                    console.debug("sel: " + selIndex + " -> " + sel.get(selIndex).fileName)
                                }
                                winFile.changeSelectedList(sel)
                            }

                            onDoubleClicked: {
                                model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
                            }

                            //hoverEnabled: true
                            onReleased: file.Drag.drop()
                            drag.target: file
                        }

                        Column {
                            id : file

                            property string filePath : model.object.filepath

                            Drag.active: mouseRegionImage.drag.active
                            Drag.hotSpot.x: 20
                            Drag.hotSpot.y: 20
                            //Drag.dragType: Drag.Automatic
                            Drag.mimeData: {"urls": [file.filePath]}
                            //Drag.mimeData: {"text/plain": file.filePath, "text/uri-list": ""}
                            // Drag.keys: "text/uri-list"
                            Drag.keys: "internFileDrag"

                            StateGroup {
                              id: fileState
                              states: State {
                                  name: "dragging"
                                  when: mouseRegionImage.pressed
                                  PropertyChanges { target: file; x: file.x; y: file.y }
                              }
                            }

                            Image {
                                x: 25
                                source: model.object.fileType == "Folder" ? "../../img/buttons/browser/folder-icon.png" : "file:///" + model.object.filepath
                                sourceSize.width: 40
                                sourceSize.height: 40

                                anchors.horizontalCenter: parent.horizontalCenter
                            }

                            Text {
                                id: textElement
                                text: model.object.fileName
                                color: model.object.isSelected ? "black" : "white"
                                font.bold: model.object.isSelected
                                width: 125
                                elide: Text.ElideRight
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }// endColumn
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
                    id: background
                    color: model.object.isSelected ? "#00b2a1" : "transparent"
                    radius: 5
                    height: 25
                    width: listview.width

                    MouseArea {
                        id: mouseRegionImage
                        anchors.fill : parent
                        onClicked: {
                            if (mouse.button == Qt.RightButton)
                                options.popup()
                                winFile.fileName = textElement.text

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
                            console.debug("sel.count: " + sel.count)
                            for(var selIndex = 0; selIndex < sel.count; ++selIndex)
                            {
                                console.debug("sel: " + selIndex + " -> " + sel.get(selIndex).fileName)
                            }
                            winFile.changeSelectedList(sel)
                        }

                        onDoubleClicked: {
                            model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
                        }

                        //hoverEnabled: true
                        onReleased: file.Drag.drop()
                        drag.target: file
                    }

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
                            text: model.object.fileName
                            color: model.object.isSelected ? "black" : "white"
                            font.bold: model.object.isSelected
                            width: parent.width
                            elide: Text.ElideRight
                        }
                    }// endRow
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
