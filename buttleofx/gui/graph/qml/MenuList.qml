import QtQuick 1.1

Item {
    id: menulist
    property alias menuState: nodeMenuView.state
    property variant clickFrom: tools

    ListView {
        id: nodeMenuView

        property string parentName : "tuttle/"

        x: 0
        y: 30
        width: 120
        height: 500
        model: _buttleData.getQObjectPluginsIdentifiersByParentPath("tuttle/")
        delegate {
            Component {
                Rectangle {
                    id: nodeMenuElement
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
                                nodeMenuView.parentName = nodeMenuView.parentName + model.object + "/"

                                if (_buttleData.nextSonIsAPlugin(nodeMenuView.parentName) == true) {
                                    console.log("CREATION NODE")
                                    nodeMenuView.state = "hidden"
                                    clickFrom.clickCreationNode(model.object)
                                }
                                else {
                                    console.log("NEWMODEL")
                                    var newModel = _buttleData.getQObjectPluginsIdentifiersByParentPath(nodeMenuView.parentName)
                                    nodeMenuView.model = newModel
                                }
                            }
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
                    model: _buttleData.getQObjectPluginsIdentifiersByParentPath("tuttle/")
                    parentName: "tuttle/"
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

    

