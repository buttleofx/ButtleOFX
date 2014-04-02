import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0

//Window of file Infos
ApplicationWindow {
    id: fileInfo

    property variant currentFile

    property color background: "#141414"
    property color backgroundInput: "#343434"
    property color gradian1: "#010101"
    property color gradian2: "#141414"
    property color borderInput: "#444"

    property color textColor: "white"
    property color activeFocusOn: "white"
    property color activeFocusOff: "grey"

    minimumWidth: 280
    minimumHeight: 170
    maximumWidth: minimumWidth
    maximumHeight: minimumHeight
    flags: Qt.FramelessWindowHint | Qt.SplashScreen

    /*FILE INFOS*/
    Rectangle{
        id: info
        height: 170
        width: fileInfo.width
        color: fileInfo.background
        border.width: 1
        border.color: "#333"

        Rectangle{
            id:headerBar
            height: 15
            width:parent.width
            color: "transparent"
            Image{
                id: close
                source: "file:///" + _buttleData.buttlePath + "/gui/img/icons/close.png"
                x:headerBar.width-15
                y:5

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        console.debug(currentFile)
                        close.source = "file:///" + _buttleData.buttlePath + "/gui/img/icons/close_hover.png"
                    }
                    onExited: {
                        close.source = "file:///" + _buttleData.buttlePath + "/gui/img/icons/close.png"
                    }
                    onClicked: {
                        editFile=false
                    }
                }
            }
        }


        Loader {
            sourceComponent: currentFile ? fileComponent : undefined
            anchors.top: parent.top
            anchors.topMargin: 20

            Component {
                id: fileComponent
                Column {
                    spacing: 5

                    /*Name of the file*/
                    Item {
                        id: fileName
                        implicitWidth: 300
                        implicitHeight: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 10

                        Row {
                            id: fileNameContainer
                            spacing: 5

                            /* Title */
                            Text {
                                id: fileNameText
                                anchors.top: parent.top
                                anchors.verticalCenter: parent.verticalCenter
                                color: textColor
                                text: "Name : "
                            }

                            /* Input field limited to 50 characters */
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
                                    text: currentFile ? currentFile.fileName : ""
                                    anchors.left: parent.left
                                    width: parent.width - 10
                                    height: parent.height
                                    anchors.leftMargin: 5
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
                }//column
            }//component
        }//loader
    }
}

