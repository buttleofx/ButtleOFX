import QtQuick 2.1
import QtQuick.Dialogs 1.0
import ButtleFileModel 1.0


Rectangle {
    id: winFile
    color: fileModel.exists ? "green" : "lightblue"

    property string folder
    property string file: gridview.currentIndex

    FileModelBrowser {
        id: fileModel
        folder: winFile.folder

        onFolderChanged: {
            fileModel.selectItem(0)
        }
    }


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
                    source: model.object.fileType == "Folder" ? "./img/folder-icon.png" : model.object.filepath
                    sourceSize.width: 40
                    sourceSize.height: 40


                    MouseArea {
                        id: mouseRegionImage
                        anchors.fill : parent
                        onClicked: {
                            gridview.currentIndex = index
                            fileModel.selectItem(index)
                            //if ctrl:
                            //if shift:
                        }
                        onDoubleClicked: model.object.fileType == "Folder" ? console.log("Go to " + model.object.fileName) : Qt.openUrlExternally(model.object.filepath)
                    }
                }
                Text {
                    text: model.object.fileName
                    color: model.object.isSelected ? "black" : "white"
                    anchors.horizontalCenter: parent.horizontalCenter

                    MouseArea {
                        id: mouseRegionText
                        anchors.fill : parent
                        onClicked: {
                            gridview.currentIndex = index
                            fileModel.selectItem(index)
                            //if ctrl:
                            //if shift:
                        }
                        onDoubleClicked: model.object.fileType == "Folder" ? console.log("Go to " + model.object.fileName) : Qt.openUrlExternally(model.object.filepath)
                    }
                }
            }
        }
        highlight: Rectangle { color: "lightsteelblue"; radius: 5}
    }

}
