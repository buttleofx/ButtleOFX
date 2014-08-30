import QtQuick 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0

ApplicationWindow {
    id: fileInfo

    property variant currentFile
    signal refreshFolder()
    signal deleteItem()

    property color background: "#141414"
    property color backgroundInput: "#343434"
    property color gradian1: "#010101"
    property color gradian2: "#141414"
    property color borderInput: "#444"

    property color textColor: "white"
    property color activeFocusOn: "white"
    property color activeFocusOff: "grey"

    minimumWidth: 280
    minimumHeight: 50
    maximumWidth: minimumWidth
    maximumHeight: 500
    flags: Qt.FramelessWindowHint | Qt.SplashScreen

    height: fileLoader.childrenRect.height
    color: fileInfo.background

    onVisibleChanged: {
        if (visible)
            rootMouseArea.forceActiveFocus()
    }

    MouseArea {
        id: rootMouseArea
        anchors.fill: parent
        hoverEnabled: true
        onContainsMouseChanged: {
            // Hack TODO: need another solution to hide the window
            if (!containsMouse)
            {
                fileInfo.visible = ! (mouseX <= 3 || mouseY <= 3 ||
                                      mouseX >= rootMouseArea.width - 3 || mouseY >= rootMouseArea.height - 3)
            }
        }
    }

    Item {
        id: marginItem
        anchors.fill: parent
        anchors.margins: 5

        Loader {
            id: fileLoader
            width: parent.width
            height: childrenRect.height
            sourceComponent: currentFile ? fileComponent : undefined

            Component {
                id: fileComponent

                ColumnLayout {
                    spacing: 5
                    width: parent.width
                    height: childrenRect.height

                    // Name of the file
                    Rectangle {
                        id: fileName
                        width: parent.width
                        implicitHeight: childrenRect.height

                        RowLayout {
                            id: fileNameContainer
                            spacing: 5
                            width: parent.width
                            height: childrenRect.height

                            // Title
                            Text {
                                id: fileNameText
                                color: textColor
                                text: "Name: "
                            }

                            // Input field limited to 50 characters
                            Rectangle {
                                height: fileNameText.height
                                Layout.fillWidth: true
                                implicitWidth: 200
                                color: fileInfo.backgroundInput
                                border.width: 1
                                border.color: fileInfo.borderInput
                                radius: 3
                                clip: true

                                TextInput {
                                    id: fileNameInput
                                    text: currentFile.fileName
                                    anchors.fill: parent
                                    anchors.leftMargin: 5
                                    anchors.rightMargin: 5
                                    maximumLength: 100
                                    selectByMouse: true
                                    color: activeFocus ? activeFocusOn : activeFocusOff

                                    onAccepted: {
                                        currentFile.fileName = fileNameInput.text
                                    }
                                    onActiveFocusChanged: {
                                        currentFile.fileName = fileNameInput.text
                                    }
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    acceptedButtons: Qt.RightButton
                                    onClicked: currentFile.nameUser = currentFile.getDefaultNameUser()
                                }
                            }
                        }
                    }

                    Rectangle {
                        id: fileDetailedInfoContainer
                        width: parent.width
                        implicitHeight: fileSizeInfoLoader.childrenRect.height + imageDimensionsLoader.childrenRect.height

                        ColumnLayout {
                            width: parent.width
                            implicitHeight: childrenRect.height

                            Loader {
                                id: fileSizeInfoLoader
                                sourceComponent: currentFile.fileType != 'Folder' ? fileSizeInfo : undefined
                            }

                            Loader {
                                id: imageDimensionsLoader
                                sourceComponent: (currentFile.fileType != 'Folder' && currentFile.getSupported() ?
                                                  imageDimensionsInfo : undefined)
                            }

                            Component {
                                id: fileSizeInfo

                                // Size of file
                                RowLayout {
                                    id: fileSize
                                    width: parent.width

                                    Text {
                                        id: fileSizeText
                                        color: textColor
                                        text: "Size: "
                                    }

                                    Text {
                                        id: fileSizeInput
                                        text: (currentFile.fileWeight > 1000000 ? (currentFile.fileWeight / 1000000).toFixed(2)
                                               + " MB" : (currentFile.fileWeight / 1000).toFixed(2) + " KB")
                                        color: "grey"
                                    }
                                }
                            }

                            Component {
                                id: imageDimensionsInfo

                                // Dimensions of image (only displayed if the file is an image, of course)
                                RowLayout {
                                    id: imageDimensions
                                    width: parent.width

                                    Text {
                                        id: imageDimensionsText
                                        color: textColor
                                        text: "Dimensions: "
                                    }

                                    Text {
                                        id: imageDimensionsInput
                                        property size imageDimensions: currentFile.imageSize
                                        text: "width: " + imageDimensions.width + ", height: " + imageDimensions.height
                                        color: "grey"
                                    }
                                }
                            }
                        }
                    }

                    Item {
                        id: remove
                        width: parent.width
                        implicitHeight: 30
                        Layout.minimumHeight: 20

                        Button {
                            id: removeButton
                            height: parent.height - 10
                            width: 200
                            text: "Remove"

                            onClicked: {
                                editFile=false
                                deleteItem()
                            }
                        }
                    }
                }
            }
        }
    }

    /*
    MessageDialog {
        id: deleteMessage
        title: "Delete?"
        icon: StandardIcon.Warning
        text: "Do you really want to delete " + currentFile.fileName + "?"
        standardButtons: StandardButton.No | StandardButton.Yes
        onYes: {
            deleteItem()
            console.log("deleted")
            editFile=false
        }
        onNo: {
            console.log("didn't delete")
        }
    }
    */
}
