import QtQuick 2.1
import QtQuick.Window 2.1
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0
import Qt.labs.folderlistmodel 2.1

Window {
    id: fileViewerWindow
    width: 630
    height: 380
    color: "#141414"
    flags: Qt.Dialog

    property string buttonText
    property string folderModelFolder
    property string entryBarText: entryBar.text

    signal buttonClicked(string currentFile)

    FolderListModel {
        id: folderModel
        showDirsFirst: true
        folder: _buttleData.homeDir
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
                    "../browser_v2/qml/img/parent_hover.png"
                } else {
                    "../browser_v2/qml/img/parent.png"
                }

                style:
                ButtonStyle {
                    background: Rectangle {
                        anchors.fill: parent
                        color: "transparent"
                    }
                }

                onClicked: {
                    folderModel.folder = folderModel.parentFolder
                }
            }

            Rectangle {
                Layout.fillWidth: true
                height: 24
                color: "black"
                radius: 5
                border.color: "grey"

                TextInput {
                    id: urlBar
                    x: 5
                    y: 4

                    text: folderModel.folder.toString().substring(7)
                    readOnly: true
                    selectByMouse: true
                    Layout.fillWidth: true

                    color: "white"
                    selectionColor: "#00b2a1"
                }
            }
        }

        ScrollView {
            anchors.fill: parent

            style: ScrollViewStyle {
                scrollBarBackground: Rectangle {
                    id: scrollBar
                    width: styleData.hovered ? 8 : 4
                    color: "transparent"

                    Behavior on width { PropertyAnimation { easing.type: Easing.InOutQuad ; duration: 200 } }
                }

                handle: Item {
                    implicitWidth: 15
                    Rectangle {
                        color: "#00b2a1"
                        anchors.fill: parent
                    }
                }

                decrementControl : Rectangle {
                    visible: false
                }

                incrementControl : Rectangle {
                    visible: false
                }
            }

            GridView {
                id: folderView
                model: folderModel
                anchors.fill: parent
                anchors.topMargin: 20
                cellWidth: 150
                cellHeight: 100
                boundsBehavior: Flickable.StopAtBounds
                focus: true

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

                    Rectangle{  
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
                                    "../browser_v2/qml/img/folder-icon.png"
                                } else if (supportedFormats.indexOf(folderModel.get(index, "fileSuffix").toLowerCase()) != -1) {
                                    folderModel.get(index, "filePath")
                                } else {
                                    "../browser_v2/qml/img/file-icon.png"
                                }
                            }
                        }

                        Text {
                            text: fileName
                            color: "white"
                            width: folderView.cellWidth - 10
                            horizontalAlignment: Text.AlignHCenter
                            wrapMode: Text.WrapAnywhere
                        }
                    }

                    MouseArea {
                        anchors.fill: parent

                        onClicked: {
                            folderView.currentIndex = index
                            if (!folderModel.isFolder(index)) {
                                entryBar.text = folderModel.get(index, "fileName")
                            } else {
                                entryBar.text = ""
                            }
                        }
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
                onClicked: fileViewerWindow.buttonClicked(folderModel.folder + "/" + entryBarText)
            }
        }
    }
}
