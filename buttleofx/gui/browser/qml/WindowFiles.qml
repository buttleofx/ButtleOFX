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

            model: fileModel.fileItems
            delegate: Component {
                Column {
                    id : file
                    Image {
                        x: 25
                        source: model.object.fileType == "Folder" ? "../../img/buttons/browser/folder-icon.png" : "file:///" + model.object.filepath
                        sourceSize.width: 40
                        sourceSize.height: 40


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
                        color: model.object.isSelected ? "blue" : "white"
                        font.bold: model.object.isSelected
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
                }
            }
        }
    }

}
