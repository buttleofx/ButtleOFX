import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0

// Parent of the ParamEditor is the Row of the ButtleApp
ApplicationWindow {
    id: paramEditor

    property variant params
    property variant currentParamNode

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

    // Buttle params
    Rectangle {
        id: buttleParams
        height: 170
        width: paramEditor.width
        color: paramEditor.background
        border.width: 1
        border.color: "#333"

        Rectangle {
            id:headerBar
            height: 15
            width:parent.width
            color: "transparent"

            Image {
                id: close
                source: "file:///" + _buttleData.buttlePath + "/gui/img/icons/close.png"
                x: headerBar.width-15
                y: 5

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true

                    onEntered: {
                        close.source = "file:///" + _buttleData.buttlePath + "/gui/img/icons/close_hover.png"
                    }
                    onExited: {
                        close.source = "file:///" + _buttleData.buttlePath + "/gui/img/icons/close.png"
                    }
                    onClicked: {
                        editNode=false
                    }
                }
            }
        }


        Loader {
            sourceComponent: currentParamNode ? nodeParamComponent : undefined
            anchors.top: parent.top
            anchors.topMargin: 20

            Component {
                id: nodeParamComponent

                Column {
                    spacing: 5

                    // Name of the node (Buttle data)
                    Item {
                        id: nodeNameUserItem
                        implicitWidth: 300
                        implicitHeight: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 10

                        Row {
                            id: nodeNameUserContainer
                            spacing: 5

                            // Title
                            Text {
                                id: nodeNameUserText
                                anchors.top: parent.top
                                anchors.verticalCenter: parent.verticalCenter
                                color: textColor
                                text: "Name : "
                            }

                            // Input field limited to 50 characters
                            Rectangle {
                                height: 20
                                implicitWidth: 200
                                color: paramEditor.backgroundInput
                                border.width: 1
                                border.color: paramEditor.borderInput
                                radius: 3
                                clip: true

                                TextInput {
                                    id: nodeNameUserInput
                                    text: currentParamNode ? currentParamNode.nameUser : ""
                                    anchors.left: parent.left
                                    width: parent.width - 10
                                    height: parent.height
                                    anchors.leftMargin: 5
                                    maximumLength: 100
                                    selectByMouse: true
                                    color: activeFocus ? activeFocusOn : activeFocusOff

                                    onAccepted: {
                                        currentParamNode.nameUser = nodeNameUserInput.text
                                    }
                                    onActiveFocusChanged: {
                                        currentParamNode.nameUser = nodeNameUserInput.text
                                    }

                                    KeyNavigation.backtab: nodeCoordYInput
                                    KeyNavigation.tab: nodeColorRGBInput
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    acceptedButtons: Qt.RightButton
                                    onClicked: currentParamNode.nameUser = currentParamNode.getDefaultNameUser()
                                }
                            }
                        }
                    }

                    // Type of the node (Buttle data)
                    Item {
                        id: nodeTypeItem
                        implicitWidth: 300
                        implicitHeight: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 10

                        Row {
                            id: nodeTypeContainer
                            spacing: 10

                            // Title
                            Text {
                                id: nodeTypeText
                                text: "Type : "
                                color: textColor
                                anchors.top: parent.top
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            // Input field limited to 50 characters
                            Rectangle {
                                height: 20
                                implicitWidth: 200
                                clip: true
                                color: "transparent"

                                Text {
                                    id: nodeTypeInput
                                    text: currentParamNode ? currentParamNode.nodeType : ""
                                    anchors.left: parent.left
                                    anchors.leftMargin: 5
                                    color: "grey"
                                }

                                Rectangle {
                                    id:helpButton
                                    width: 15
                                    height: 15
                                    x: nodeTypeInput.x + nodeTypeInput.width + 4
                                    color: "#010101"
                                    radius: 10
                                    border.width: 1
                                    border.color: "#444"

                                    Text{
                                        id: helpText
                                        text: "?"
                                        color: "white"
                                        x: 4
                                    }

                                    MouseArea {
                                        id: downNodeMouseArea
                                        anchors.fill: parent
                                        hoverEnabled: true

                                        onClicked: {
                                            doc.show()
                                        }
                                        onEntered: {
                                            helpButton.color = "#343434"
                                        }
                                        onExited: {
                                            helpButton.color = "#010101"
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // Color of the node (Buttle data)
                    Item {
                        id: nodecolorItem
                        implicitWidth: 300
                        implicitHeight: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 10

                        Row {
                            id: nodeColorContainer
                            spacing: 10

                            // Title
                            Text {
                                id: nodeColorText
                                text: "Color : "
                                color: textColor
                                anchors.top: parent.top
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            // Input field limited: rgb
                            Rectangle {
                                height: 20
                                implicitWidth: 80
                                color: paramEditor.backgroundInput
                                border.width: 1
                                border.color: paramEditor.borderInput
                                radius: 3
                                clip: true

                                TextInput {
                                    id: nodeColorRGBInput
                                    // text: currentParamNode ? currentParamNode.color : ""
                                    anchors.left: parent.left
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.leftMargin: 5
                                    width: parent.width - 10
                                    height: parent.height
                                    maximumLength: 50
                                    selectByMouse: true
                                    color: activeFocus ? activeFocusOn : activeFocusOff

                                    onAccepted: currentParamNode.color = nodeColorRGBInput.text
                                    onActiveFocusChanged: currentParamNode.color = nodeColorRGBInput.text

                                    KeyNavigation.backtab: nodeNameUserInput
                                    KeyNavigation.tab: nodeCoordXInput
                                } // textinput

                                MouseArea {
                                    anchors.fill: parent
                                    acceptedButtons: Qt.RightButton
                                    onClicked: {
                                        currentParamNode.color = currentParamNode.getDefaultColor();
                                        console.log("Clicked");
                                    }
                                }
                            } // Rectangle of nodeColorContainer
                        } // Row nodeColorContainer
                    } // Item nodeColorItem

                    // Coord of the node (Buttle data)
                    Item {
                        id: nodecoordItem
                        implicitWidth: 300
                        implicitHeight: 30
                        anchors.left: parent.left
                        anchors.leftMargin: 10

                        Row {
                            id: nodeCoordContainer
                            spacing: 10

                            // Input label: "x : "
                            Rectangle {
                                height: 20
                                implicitWidth: 15
                                color: "transparent"

                                Text{
                                    id: nodeCoordXLabel
                                    text: "x :"
                                    anchors.left: parent.left
                                    anchors.leftMargin: 5
                                    color: textColor
                                }
                            }

                            // Input field limited : x
                            Rectangle {
                                height: 20
                                implicitWidth: 35
                                color: paramEditor.backgroundInput
                                border.width: 1
                                border.color: paramEditor.borderInput
                                radius: 3
                                clip: true

                                TextInput {
                                    id: nodeCoordXInput
                                    text: currentParamNode ? currentParamNode.coord.x : ""
                                    anchors.left: parent.left
                                    anchors.leftMargin: 5
                                    width: parent.width - 10
                                    height: parent.height
                                    color: activeFocus ? activeFocusOn : activeFocusOff
                                    selectByMouse: true

                                    onAccepted: {
                                        currentParamNode.xCoord = nodeCoordXInput.text
                                    }
                                    onActiveFocusChanged: {
                                        currentParamNode.xCoord = nodeCoordXInput.text
                                    }

                                    KeyNavigation.backtab: nodeColorRGBInput
                                    KeyNavigation.tab: nodeCoordYInput

                                }
                            }

                            // Input label: "y : "
                            Rectangle {
                                height: 20
                                implicitWidth: 15
                                color: "transparent"

                                Text {
                                    id: nodeCoordYLabel
                                    text: "y :"
                                    anchors.left: parent.left
                                    anchors.leftMargin: 5
                                    color: textColor
                                }
                            }

                            // Input field limited: y
                            Rectangle {
                                height: 20
                                implicitWidth: 35
                                color: paramEditor.backgroundInput
                                border.width: 1
                                border.color: paramEditor.borderInput
                                radius: 3
                                clip: true

                                TextInput {
                                    id: nodeCoordYInput
                                    text: currentParamNode ? currentParamNode.coord.y : ""
                                    anchors.left: parent.left
                                    anchors.leftMargin: 5
                                    width: parent.width - 10
                                    height: parent.height
                                    color: activeFocus ? activeFocusOn : activeFocusOff
                                    selectByMouse: true

                                    onAccepted: {
                                        currentParamNode.yCoord = nodeCoordYInput.text
                                    }
                                    onActiveFocusChanged: {
                                        currentParamNode.yCoord = nodeCoordYInput.text
                                    }

                                    KeyNavigation.backtab: nodeCoordXInput
                                    KeyNavigation.tab: nodeNameUserInput
                                }
                            }
                        }
                    }
                } // Column
            } // Component
        } // Loader
    } // Rectangle of buttleParam
}
