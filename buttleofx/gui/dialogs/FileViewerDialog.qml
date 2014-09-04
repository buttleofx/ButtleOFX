import QtQuick 2.1
import QtQuick.Window 2.1
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0
import Qt.labs.folderlistmodel 2.1

Window {
    id: mainWindow
    width: 630
    height: 380
    flags: Qt.Dialog
    color: "#141414"
    visible: false
    property string buttonText: ""
    property string currentFolder: folderModel.folder
    property string entryBarText: entryBar.text

    signal buttonClicked

    FolderListModel {
        id: folderModel
        showDirsFirst: true
        folder: "/home/james/"
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 4

        RowLayout {
            id: headerBar
            anchors.top: parent.top
            anchors.leftMargin: parent.spacing
            anchors.rightMargin: parent.spacing

            Button {
                id: parentFolderButton
                width: 15
                height: 15

                iconSource:
                if (hovered) {
                    "../img/buttons/browser/parent_hover.png"
                } else {
                    "../img/buttons/browser/parent.png"
                }

                style:
                ButtonStyle {
                    background: Rectangle {
                        anchors.fill: parent
                        color: "transparent"
                    }
                }

                onClicked: { folderModel.folder = folderModel.parentFolder }
            }

            Rectangle {
                Layout.fillWidth: true
                height: 24
                color: "black"
                radius: 5
                border.color: "grey"

                TextInput {
                    x: 5
                    y: 4

                    readOnly: true
                    selectByMouse: true
                    Layout.fillWidth: true

                    color: "white"
                    text: folderModel.folder.toString().substring(7)
                    selectionColor: "#00b2a1"
                }
            }
        }

        ScrollView {
            anchors.top: headerBar.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: bottomRow.top
            anchors.bottomMargin: 4

            GridView {
                id: folderView
                model: folderModel
                cellWidth: 100
                cellHeight: 100
                highlightFollowsCurrentItem: false

                highlight: Rectangle {
                    width: folderView.cellWidth
                    height: folderView.cellHeight
                    color: "#00b2a1"
                    radius: 4

                    x: folderView.currentItem.x
                    y: folderView.currentItem.y
                    Behavior on x { SmoothedAnimation { duration: -1; velocity: -1 } }
                    Behavior on y { SmoothedAnimation { duration: -1; velocity: -1 } }
                }

                delegate: Rectangle {
                    width: folderView.cellWidth
                    height: folderView.cellHeight
                    color: "transparent"

                    Column {
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter

                        Image {
                            anchors.horizontalCenter: parent.horizontalCenter
                            width: 55
                            height: 55
                            asynchronous: true
                            fillMode: Image.PreserveAspectFit
                            sourceSize.width: width
                            sourceSize.height: height
                            property variant supportedFormats: ["bmp", "gif", "jpg", "jpeg", "png", "pbm", "pgm", "ppm", "xbm", "xpm"]

                            source: {
                                if (folderModel.isFolder(index)) {
                                    "../img/buttons/browser/folder-icon.png"
                                } else if (supportedFormats.indexOf(folderModel.get(index, "fileSuffix").toLowerCase()) != -1) {
                                    folderModel.get(index, "filePath")
                                } else {
                                    "../img/buttons/browser/file-icon.png"
                                }
                            }
                        }
                        Text {
                            width: folderView.cellWidth - 10
                            horizontalAlignment: Text.AlignHCenter
                            wrapMode: Text.WrapAnywhere
                            text: fileName
                            color: "white"
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: folderView.currentIndex = index

                        onDoubleClicked: {
                            if (folderModel.isFolder(index)) {
                                    folderModel.folder = folderModel.get(index, "filePath")
                            }
                        }
                    }
                }
            }
        }

        RowLayout {
            id: bottomRow
            Layout.fillWidth: true
            Layout.fillHeight: true
            anchors.bottom: parent.bottom

            TextField {
                id: entryBar
                Layout.fillWidth: true
            }

            Button {
                text: buttonText

                style:
                ButtonStyle {
                    background: Rectangle {
                        radius: 6
                        implicitWidth: 100
                        implicitHeight: 25

                        border.color: control.hovered ? "#00B2A1" : "#9F9C99"
                        border.width: control.hovered ? 3 : 2

                        gradient: Gradient {
                            GradientStop { position: 0; color: control.pressed ? "#EFEBE7" : "#EFEBE7" }
                            GradientStop { position: .5; color: control.pressed ? "#D9D9D9" : "#EFEBE7" }
                            GradientStop { position: 0; color: control.pressed ? "#EFEBE7" : "#EFEBE7" }
                        }
                    }
                }
                onClicked: mainWindow.buttonClicked()
            }
        }
    }
}
