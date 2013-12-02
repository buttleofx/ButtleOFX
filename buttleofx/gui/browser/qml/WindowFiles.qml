import QtQuick 2.1
import Qt.labs.folderlistmodel 1.0
import QtQuick.Dialogs 1.0
import ButtleFileModel 1.0

Rectangle{
    id: winFile
	color: "green"

    property string folder
	property string file: gridview.currentIndex
    onFolderChanged: {
        console.log("WindowsFiles folder: ", folder)
    }

    // margins: 20
    /*
    FolderListModel{
        id: fileModel
        folder: winFile.folder
        onFolderChanged: {
            console.log("FolderListModel folder: ", folder)
        }
        showDirsFirst: true
        nameFilters: [ "*.png", "*.jpg" ]
    }*/
    FileModelBrowser {
        id: fileModel
        folder: winFile.folder
    }

	GridView{
        id: gridview
		height : parent.height
		width : parent.width
		cellWidth: 150

        model: fileModel
		delegate: Column {
			id : file
			Image{
				x: 25
                source: model.type == "Folder" ? "./img/folder-icon.png" : "file://"+ model.filepath
				sourceSize.width: 40
				sourceSize.height: 40
                Component.onCompleted: {
                    console.log("Image Component.onCompleted: ", source)
                }

				MouseArea{
					id: mouseRegionImage
					anchors.fill : parent
					onClicked: gridview.currentIndex = index
					onDoubleClicked: folder1.isFolder(index) ? console.log("Go to " + fileName) : console.log("Open " + fileName)
				}
			}	
			Text{
                text: model.filepath
				anchors.horizontalCenter: parent.horizontalCenter

				MouseArea{
					id: mouseRegionText
					anchors.fill : parent
					onClicked: gridview.currentIndex = index
                    onDoubleClicked: console.log("Open " + model.filepath)
				}
            }
		}
		highlight: Rectangle { color: "lightsteelblue"; radius: 5}
		focus: true
	}

}
