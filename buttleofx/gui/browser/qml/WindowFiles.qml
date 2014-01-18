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

        GridView {
            id: gridview
            height : parent.height
            width : parent.width
            cellWidth: 150
            visible: viewGrid ? false : true

            model: fileModel.fileItems
            delegate: Component {
                Rectangle {
                    id: background
                    color: model.object.isSelected ? "#888888FF" : "transparent"
                    radius: 5
                    height: 80
                    width: 100

                    Column {
                        id : file
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
                                    gridview.currentIndex = index
                                    fileModel.selectItem(index)
                                    winFile.changeFile(model.object.filepath)
                                    winFile.changeFileType(model.object.fileType)
                                    //if ctrl:
                                    //if shift:
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
                            width: 125
                            elide: Text.ElideRight
                            anchors.horizontalCenter: parent.horizontalCenter

                            MouseArea {
                                id: mouseRegionText
                                anchors.fill : parent
                                onClicked: {
                                    gridview.currentIndex = index
                                    fileModel.selectItem(index)
                                    winFile.changeFile(model.object.filepath)
                                    winFile.changeFileType(model.object.fileType)
                                    //if ctrl:
                                    //if shift:
                                }
                                onDoubleClicked: {
                                    model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
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

        ListView {
            id: listview
            height : parent.height
            width : parent.width
            visible: viewGrid

            model: fileModel.fileItems
            delegate: Component {
                Rectangle {
                    id: background
                    color: model.object.isSelected ? "#888888FF" : "transparent"
                    radius: 5
                    height: 30
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
                                listview.currentIndex = index
                                fileModel.selectItem(index)
                                winFile.changeFile(model.object.filepath)
                                winFile.changeFileType(model.object.fileType)
                                //if ctrl:
                                //if shift:
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
                        width: 125
                        elide: Text.ElideRight


                        MouseArea {
                            id: mouseRegionText
                            anchors.fill : parent
                            onClicked: {
                                listview.currentIndex = index
                                fileModel.selectItem(index)
                                winFile.changeFile(model.object.filepath)
                                winFile.changeFileType(model.object.fileType)
                                //if ctrl:
                                //if shift:
                            }
                            onDoubleClicked: {
                                model.object.fileType == "Folder" ? winFile.goToFolder(model.object.filepath) : Qt.openUrlExternally("file:///" + model.object.filepath)
                            }
                        }
                    }
                }// endRow
                }
            }//endComponent
        }
    }

}
