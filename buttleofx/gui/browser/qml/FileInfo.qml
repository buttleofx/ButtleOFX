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
        if( visible )
            rootMouseArea.forceActiveFocus()
    }
    MouseArea {
        id: rootMouseArea
        anchors.fill: parent
        hoverEnabled: true
        onContainsMouseChanged: {
            // Hack TODO: need another solution to hide the window
            if( ! containsMouse )
            {
                fileInfo.visible = ! ( mouseX <= 3 || mouseY <= 3 ||
                                       mouseX >= rootMouseArea.width - 3 || mouseY >= rootMouseArea.height - 3 )
            }
        }
    }

    Item {
        id: marginItem
        anchors.fill: parent
        anchors.margins: 5

        Loader {
            id: fileLoader
            sourceComponent: currentFile ? fileComponent : undefined

            Component {
                id: fileComponent

                ColumnLayout {
                    spacing: 5
                    width: parent.width
                    height: childrenRect.height

                    // Name of the file
                    Item {
                        id: fileName
                        width: parent.width
                        implicitHeight: childrenRect.height

                        RowLayout {
                            id: fileNameContainer
                            spacing: 5

                            /* Title */
                            Text {
                                id: fileNameText
                                color: textColor
                                text: "Name: "
                            }

                            // Input field limited to 50 characters
                            Rectangle {
                                height: 20
                                implicitWidth: 200
                                color: fileInfo.backgroundInput
                                border.width: 1
                                border.color: fileInfo.borderInput
                                radius: 3
                                clip: true

                                TextInput {
                                    id: fileNameInput
                                    text: currentFile.fileName
                                    width: parent.width - 10
                                    height: parent.height
                                    maximumLength: 100
                                    selectByMouse : true
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
                        implicitHeight: fileDetailedInfoLoader.childrenRect.height
                        color: "red"

                        Loader {
                            id: fileDetailedInfoLoader
                            sourceComponent: currentFile.fileType != 'Folder' ? fileDetailedInfo : undefined
                        }

                        Component {
                            id: fileDetailedInfo
                            ColumnLayout {
                                width: parent.width
                                implicitHeight: childrenRect.height

                                /* Extension of file */
                                RowLayout {
                                    id: fieExtensionContainer
                                    spacing: 5
                                    width: parent.width
                                    implicitHeight: childrenRect.height

                                    Text {
                                        id: fileExtensionText
                                        color: textColor
                                        text: "Extension: "
                                    }

                                    Rectangle {
                                        height: 20
                                        implicitWidth: 200
                                        clip: true
                                        color: "transparent"
                                        Text{
                                            id: fileExtensionInput
                                            text: currentFile.fileExtension
                                            color: "grey"
                                        }
                                    }
                                }

                                // Weight of file
                                RowLayout {
                                    id: fileWeight
                                    width: parent.width
                                    implicitHeight: childrenRect.height

                                    Text {
                                        id: fileWeightText
                                        color: textColor
                                        text: "Weight: "
                                    }

                                    Rectangle {
                                        height: 20
                                        implicitWidth: 200
                                        clip: true
                                        color: "transparent"
                                        Text{
                                            id: fileWeightInput
                                            text: (currentFile.fileWeight > 1000000 ? (currentFile.fileWeight/1000000).toFixed(2) +" Mo" : (currentFile.fileWeight/1000).toFixed(2) + " Ko")
                                            color: "grey"
                                        }
                                    }
                                }

                                // Size of File
                                RowLayout {
                                    id: fileSize
                                    width: parent.width
                                    implicitHeight: childrenRect.height

                                    Text {
                                        id: fileSizeText
                                        color: textColor
                                        text: "Size: "
                                    }

                                    Rectangle {
                                        height: 20
                                        implicitWidth: 200
                                        clip: true
                                        color: "transparent"

                                        Text {
                                            id: fileSizeInput
                                            property size imageSize: currentFile.imageSize
                                            text: "width: " + imageSize.width + ", height: " + imageSize.height
                                            color: "grey"
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Rectangle {
                        id:remove
                        width: parent.width
                        implicitHeight: 30
                        Layout.minimumHeight: 20
                        color: "blue"

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

