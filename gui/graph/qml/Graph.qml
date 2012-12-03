import QtQuick 1.1

Rectangle {
    width: 850
    height: 350 - 30
    y: 30
    gradient: Gradient {
        GradientStop { position: 0.0; color: "#111111" }
        GradientStop { position: 0.015; color: "#212121" }
    }

    Keys.onPressed: {
        if (event.key==Qt.Key_Delete) {
            if (node.focus == true){
                deleteNode()
            }
        }
    }
    MouseArea {
            anchors.fill: parent
             acceptedButtons: Qt.LeftButton | Qt.RightButton
             onPressed: {
                 if (mouse.button == Qt.RightButton) {
                     nodeMenu.state = "opened"
                     nodeMenu.x = mouseX
                     nodeMenu.y = mouseY
                 }
             }
         }

    Item {
            id: nodeMenu
            state: "closed"
            Rectangle {
                id: createButton
                width: 100
                height: 20
                color: "#141414"

                Text {
                    id: createButtonText
                    horizontalAlignment:  Text.AlignHCenter
                    text: "Create Node"
                    font.pointSize: 10
                    color: "white"

                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        _nodeManager.createNode();
                        nodeMenu.state = "closed"
                    }
                }
            }

            states: [
            State {
                name: "closed";
                PropertyChanges {
                    target: nodeMenu
                    opacity: 0.0

                }
            },
            State {
                 name: "opened";
                 PropertyChanges {
                     target: nodeMenu
                     opacity: 1.0
                 }
            } ]
        }
}
