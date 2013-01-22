import QtQuick 1.1

Item {
    id: menulist
    property alias menuState: nodeMenuView.state
    property variant clickFrom: tools

    ListView {
        id: nodeMenuView
        x: 0
        y: 30
        width: 120
        height: 500
        model: _buttleData.tuttlePluginsNames
        delegate {
            Rectangle {
                width: 120
                height: 20
                color: "#343434"
                Text {
                    anchors.left: parent.left
                    anchors.leftMargin: 15
                    anchors.verticalCenter: parent.verticalCenter
                    color: "#eee"
                    text: model.object
                }
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: parent.color = "#bbb"
                    onExited: parent.color = "#343434"
                    onClicked: {
                        if(nodeMenuView.state == "shown"){                          
                            clickFrom.clickCreationNode(model.object)
                            nodeMenuView.state = "hidden"
                        }
                    }
                }
            }
        }

        state: "hidden"
        states: [
            State {
                name: "hidden"
                PropertyChanges {
                    target: nodeMenuView
                    height: 0
                    opacity: 0
                }
            },
            State {
                name: "shown"
                PropertyChanges {
                    target: nodeMenuView
                    height: nodeMenuView.contentHeight > 0 ? nodeMenuView.contentHeight : 0
                    opacity: 1
                }
            }
        ]
        transitions: [
            Transition {
                NumberAnimation { target: nodeMenuView; property: "height"; duration: 200 }
                NumberAnimation { target: nodeMenuView; property: "opacity"; duration: 200 }
            }
        ]
    } 
}

    
