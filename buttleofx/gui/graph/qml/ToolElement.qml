import QtQuick 2.0

Rectangle {
    id: buttonTools
    anchors.verticalCenter: parent.verticalCenter
    width: 28
    height: 28
    color: "transparent"
    radius: 3

    property string imageSource
    property string imageSourceHover
    property string imageSourceLocked
    property string buttonName
    property string buttonText
    property bool locked

    signal clicked()

    Image {
        id: imageButton
        property string file: buttonTools.imageSource
        source: "file:///" + imageButton.file
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
    }

    MouseArea {
        id: buttonMouseArea
        hoverEnabled: true
        anchors.fill: parent

        onClicked: {
            if (!locked) {
                buttonTools.clicked()
                // Take the focus of the mainWindow
                parent.forceActiveFocus()
            }
        }
    }

    Rectangle {
        id: infoTools
        x: 15
        y: 35
        color: "grey"
        opacity: buttonMouseArea.containsMouse ? 1 : 0

        Text {
            text: buttonText
            color: "#bbbbbb"
        }
    }

    StateGroup {
        id: stateButtonEvents
        states: [
            State {
                name: "locked"
                when: locked

                PropertyChanges {
                    target: buttonTools
                    color: "transparent"
                }
                PropertyChanges {
                    target: imageButton
                    file: imageSourceLocked
                }
            },
            State {
                name: "normal"
                when: !buttonMouseArea.containsMouse

                PropertyChanges {
                    target: buttonTools
                    color: "transparent"
                }
                PropertyChanges {
                    target: imageButton
                    file: imageSource
                }
            },
            State {
                name: "pressed"
                when: buttonMouseArea.containsMouse && buttonMouseArea.pressed

                PropertyChanges {
                    target: buttonTools
                    color: "#00b2a1"
                }
                PropertyChanges {
                    target: imageButton
                    file: imageSource
                }
            },
            State {
                name: "hover"
                when: buttonMouseArea.containsMouse

                PropertyChanges {
                    target: buttonTools
                    color: "#555555"
                }
                PropertyChanges {
                    target: imageButton
                    file: imageSourceHover
                }
            }
        ]
    }
}
