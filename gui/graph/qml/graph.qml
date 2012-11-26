import QtQuick 1.0

Rectangle {
    width: 850
    height: 350 - 30

    MouseArea {
            anchors.fill: parent
             acceptedButtons: Qt.LeftButton | Qt.RightButton
             onPressed: {
                 if (mouse.button == Qt.RightButton) {
                     rightMenu.state = "opened"
                     rightMenu.x = mouseX
                     rightMenu.y = mouseY
                 }
             }
         }

    Item {
            id: rightMenu
            state: "closed"
            Rectangle {
                id: createButton
                width: 100
                height: 20
                color: "#141414"

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        addNode()
                        rightMenu.state = "closed"
                    }
                }

                Text {
                    id: createButtonText
                    horizontalAlignment:  Text.AlignHCenter
                    text: "Create Node"
                    font.pointSize: 10
                    color: "white"

                }
            }

            states: [
            State {
                name: "closed";
                PropertyChanges {
                    target: rightMenu
                    opacity: 0.0

                }
            },
            State {
                 name: "opened";
                 PropertyChanges {
                     target: rightMenu
                     opacity: 1.0
                 }
            } ]
        }
}
