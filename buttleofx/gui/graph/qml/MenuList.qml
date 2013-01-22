import QtQuick 1.1

Item {
    id: menulist
    property alias menuState: nodeMenuView.state
    property variant clickFrom: tools

   //ListModel {
//    ListView {
//        id: nodeMenuModel
//        model: _buttleApp.tuttlePluginsNames
//        delegate {
//            ListElement { cat1 : "Prout"; cat2: model.object }
//        }

//    /*
//        ListElement { cat1: "Color"; cat2: "Invert" }
//        ListElement { cat1: "Color"; cat2: "Gamma" }
//        ListElement { cat1: "Filter"; cat2: "Blur" }
//        ListElement { cat1: "Geometry"; cat2: "Crop" }
//        ListElement { cat1: "Geometry"; cat2: "Resize" }
//        */
//    }

//    Component {
//        id: nodeMenuDelegate
//        Row{
//            Rectangle {
//                width: 120
//                height: 25
//                gradient: Gradient {
//                    GradientStop { position: 0.0; color: "#111111" }
//                    GradientStop { position: 1.0; color: "#212121" }
//                }
//                Text{
//                    anchors.left: parent.left
//                    anchors.leftMargin: 5
//                    anchors.verticalCenter: parent.verticalCenter
//                    text: section
//                    color: "#ddd"
//                }
//            }
//        }
//    }

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
//        section.property: "cat1"
//        section.criteria: ViewSection.FullString
//        section.delegate: nodeMenuDelegate
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

    
