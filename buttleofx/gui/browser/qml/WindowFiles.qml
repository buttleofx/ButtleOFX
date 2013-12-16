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
                    source: model.object.fileType == "Folder" ? "./img/folder-icon.png" : "file://" + model.object.filepath
                    sourceSize.width: 40
                    sourceSize.height: 40
                    Component.onCompleted: {
                        console.log("Image Component.onCompleted: ", source)
                    }

                    MouseArea {
                        id: mouseRegionImage
                        anchors.fill : parent
                        onClicked: gridview.currentIndex = index
                        onDoubleClicked: model.object.fileType == "Folder" ? console.log("Go to " + model.object.filepath) : console.log("Open " + model.object.filepath)
                    }
                }
                Text {
                    text: model.object.filepath
                    anchors.horizontalCenter: parent.horizontalCenter

                    MouseArea {
                        id: mouseRegionText
                        anchors.fill : parent
                        onClicked: gridview.currentIndex = index
                        onDoubleClicked: model.object.fileType == "Folder" ? console.log("Go to " + model.object.filepath) : Qt.openUrlExternally(folder + "/" + model.object.filepath)
                    }
                }
            }
        }
        highlight: Rectangle { color: "lightsteelblue"; radius: 5}
    }

}
