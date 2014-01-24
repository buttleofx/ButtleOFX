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

                                MouseArea {
                                    id: mouseRegionImage
                                    anchors.fill : parent
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
                                        console.debug("sel.count: " + sel.count)
                                        for(var selIndex = 0; selIndex < sel.count; ++selIndex)
                                        {
                                            console.debug("sel: " + selIndex + " -> " + sel.get(selIndex).fileName)
                                        }
                                        winFile.changeSelectedList(sel)
                                    }

                                    onDoubleClicked: {
                                        //model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
                                        //model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : console.log("A lier au viewer")

                                        if (model.object.fileType != "Folder"){

                                            readerNode.nodeWrapper = _buttleData.nodeReaderWrapperForBrowser(model.object.filepath)
                                            console.log ("New node from the browser", readerNode.nodeWrapper.name)
                                            _buttleData.currentGraphWrapper = _buttleData.graphBrowserWrapper
                                            //_buttleData.currentGraphWrapper = _buttleData.graphWrapper

                                            _buttleData.currentViewerNodeWrapper = readerNode.nodeWrapper
                                            _buttleData.currentViewerFrame = 0
                                            // we assign the node to the viewer, at the frame 0
                                            _buttleData.assignNodeToViewerIndex(readerNode.nodeWrapper, 0)
                                            _buttleEvent.emitViewerChangedSignal()

                                        }
                                        else{
                                            winFile.goToFolder(model.object.filepath)
                                        }
                                    }

                                    //hoverEnabled: true
                                    onReleased: file.Drag.drop()
                                    drag.target: file
                                }
                            }

                            Text {
                                text: model.object.fileName
                                color: model.object.isSelected ? "black" : "white"
                                font.bold: model.object.isSelected
                                width: 125
                                elide: Text.ElideRight
                                anchors.horizontalCenter: parent.horizontalCenter

                                MouseArea {
                                    id: mouseRegionText
                                    anchors.fill : parent
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
                                        winFile.changeSelectedList(sel)
                                    }
                                    onDoubleClicked: {
                                        //model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
                                    }
                                }
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

                    Row {
                        width: parent.width
                        spacing: 10
                        Image {
                            x: 25
                            source: model.object.fileType == "Folder" ? "../../img/buttons/browser/folder-icon.png" : "file:///" + model.object.filepath
                            sourceSize.width: 20
                            sourceSize.height: 20

                            MouseArea {
                                id: mouseRegionImage
                                anchors.fill : parent
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
                                    winFile.changeSelectedList(sel)
                                }
                                onDoubleClicked: {
                                    model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
                                }
                            }
                        }

                        Text {
                            text: model.object.fileName
                            color: model.object.isSelected ? "black" : "white"
                            font.bold: model.object.isSelected
                            width: parent.width
                            elide: Text.ElideRight

                            MouseArea {
                                id: mouseRegionText
                                anchors.fill : parent
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
                                    winFile.changeSelectedList(sel)
                                }
                                onDoubleClicked: {
                                    //model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
                                }
                            }
                        }
                    }// endRow
                }// end Rectangle
            }//endComponent
        }
    }

}
