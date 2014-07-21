import QtQuick 2.1
import Qt.labs.folderlistmodel 1.0

Rectangle {
    id: leftColumn
    color: "red"

    ListView {
        id: listview
        y: 20
        x: 10
        height : parent.height
        width : parent.height
        currentIndex: -1

        model: FolderListModel {
            id: folders
            folder: "/home/lucie-linux/"
            showDirsFirst: true
        }

        delegate: Column {
            Text {
                text: fileName
                anchors.horizontalCenter: parent.horizontalCenter

                MouseArea {
                    id: mouseRegion
                    anchors.fill : parent
                    onClicked: {
                        console.log( fileName + " Clicked")
                        listview.currentIndex = index
                    }
                }
            }
        }

        highlight: Rectangle {
            color: "lightsteelblue"
            radius: 5
        }

        keyNavigationWraps: false
    }
}
