import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Dialogs 1.0
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
                        width: 100

                        property variant selectedFiles

                        Column {
                            id : file

                            Image {
                                x: 25
                                source: model.object.fileType == "Folder" ? "../../img/buttons/browser/folder-icon.png" : "file:///" + model.object.filepath
                                sourceSize.width: 40
                                sourceSize.height: 40

                                anchors.horizontalCenter: parent.horizontalCenter
                            }

                            Text {
                                text: model.object.fileName
                                color: model.object.isSelected ? "black" : "white"
                                font.bold: model.object.isSelected
                                width: 125
                                elide: Text.ElideRight
                                anchors.horizontalCenter: parent.horizontalCenter
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
                            onReleased: fileInColumn.Drag.drop()
                            drag.target: fileInColumn

                            onClicked: {
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
                        onReleased: fileInRow.Drag.drop()
                        drag.target: fileInRow

                        onClicked: {
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

}
