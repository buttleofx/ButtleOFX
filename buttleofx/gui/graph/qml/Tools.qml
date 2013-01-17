import QtQuick 1.1

Rectangle {
    id: tools
    width: 850
    height: 30

    z: 2000
    anchors.top: parent.top
    color: "#212121"
    Rectangle {
        id: addNodeButton
        implicitWidth: 20
        implicitHeight: 20
        width: 7/10 * parent.height
        height: width
        anchors.verticalCenter: parent.verticalCenter
        color: "#212121"
        Text {
            anchors.centerIn: parent
            text: "+"
            font.pointSize: 16
            color: "white"
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                nodeMenuView.state = (nodeMenuView.state == "hidden") ? "shown" : "hidden"
            }
        }
    }
    Rectangle {
        id: delNodeButton
        implicitWidth: 20
        implicitHeight: 20
        width: 7/10 * parent.height
        height: width
        x: 30
        y: 6
        color: "#212121"
        Text {
            anchors.centerIn: parent
            text: "-"
            font.pointSize: 16
            color: "white"
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                //_graphWrapper.deleteCurrentNode();
                _buttleData.getGraphWrapper().destructionNode(_cmdManager)

            }
        }
    }

    ListModel {
        id: nodeMenuModel
        ListElement { cat1: "Color"; cat2: "Invert" }
        ListElement { cat1: "Color"; cat2: "Gamma" }
        ListElement { cat1: "Filter"; cat2: "Blur" }
        ListElement { cat1: "Geometry"; cat2: "Crop" }
        ListElement { cat1: "Geometry"; cat2: "Resize" }
    }
    Component {
        id: nodeMenuDelegate
        Row{
            Rectangle {
                width: 120
                height: 25
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#111111" }
                    GradientStop { position: 1.0; color: "#212121" }
                }
                Text{
                    anchors.left: parent.left
                    anchors.leftMargin: 5
                    anchors.verticalCenter: parent.verticalCenter
                    text: section
                    color: "#ddd"
                }
            }
        }
    }
    ListView {
        id: nodeMenuView
        x: 0
        y: 30
        width: 120
        height: 500
        model: nodeMenuModel
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
                    text: cat2
                }
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: parent.color = "#bbb"
                    onExited: parent.color = "#343434"
                    onClicked: {
                        if(nodeMenuView.state == "shown"){
                            _buttleData.getGraphWrapper().creationNode(cat2, _cmdManager)
                            nodeMenuView.state = "hidden"
                        }
                    }
                }
            }
        }
        section.property: "cat1"
        section.criteria: ViewSection.FullString
        section.delegate: nodeMenuDelegate
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
                    height: nodeMenuView.contentHeight
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
