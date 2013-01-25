import QtQuick 1.1


Item {
    id: menulist
    property alias menuState: nodeMenuView.state
    property variant clickFrom: tools

    property string parentName

    ListView {
        id: nodeMenuView
        property string parentName : parentName
        model: _buttleData.getQObjectPluginsIdentifiersByParentPath(parentName) // liste de MenuItem qui connaissent leurs enfants

        delegate {
            Component {
                Item {
                    width: 120
                    height: 20
                    MouseArea {
                        anchors.fill : parent
                        onClicked: {
                            if (object.type == "node") {
                                // create node
                            }
                            else {
                                menuItemLoader.sourceComponent = object.listMenuItem
                            }
                        }

                    }
                    Loader {
                        id: menuItemLoader

                        Component {
                            MenuList {
                                parentName: nodeMenuView.parentName + object.label + "/"

                            }
                        }

                    }

                }





            }
        }
    }
}

//Item {
//    id: menulist
//    property alias menuState: nodeMenuView.state
//    property variant clickFrom: tools

//    property bool truc : false

//    ListView {
//        id: nodeMenuView

//        property string parentName : "tuttle/"

//        x: 0
//        y: 30
//        width: 120
//        height: 500
//        model: _buttleData.getQObjectPluginsIdentifiersByParentPath("tuttle/")
//        delegate {
//            Component {
//                Rectangle {
//                    id: nodeMenuElement
//                    width: 120
//                    height: 20
//                    color: "#343434"
//                    Text {
//                        anchors.left: parent.left
//                        anchors.leftMargin: 15
//                        anchors.verticalCenter: parent.verticalCenter
//                        color: "#eee"
//                        text: object
//                    }
//                    MouseArea {
//                        anchors.fill: parent
//                        hoverEnabled: true
//                        onEntered: parent.color = "#bbb"
//                        onExited: parent.color = "#343434"
//                        onClicked: {
//                            if(nodeMenuView.state == "shown"){
//                                nodeMenuView.parentName = nodeMenuView.parentName + object + "/"

//                                if (_buttleData.nextSonIsAPlugin(nodeMenuView.parentName) == true) {
//                                    console.log("CREATION NODE")
//                                    nodeMenuView.state = "hidden"
//                                    clickFrom.clickCreationNode('tuttle.' + object)
//                                }
//                                else {
//                                    console.log("NEWMODEL")
//                                    var newModel = _buttleData.getQObjectPluginsIdentifiersByParentPath(nodeMenuView.parentName)
//                                    console.log("1")


//                                    nodeMenuView.model = newModel

//                                    //Qt.createQmlObject()


//                                    console.log("2")
//                                }
//                            }
//                        }
//                    }
//                }
//            }
//        }

//        state: "hidden"
//        states: [
//            State {
//                name: "hidden"
//                PropertyChanges {
//                    target: nodeMenuView
//                    height: 0
//                    opacity: 0
//                }
//            },
//            State {
//                name: "shown"
//                PropertyChanges {
//                    target: nodeMenuView
//                    height: nodeMenuView.contentHeight > 0 ? nodeMenuView.contentHeight : 0
//                    opacity: 1
//                    model: _buttleData.getQObjectPluginsIdentifiersByParentPath("tuttle/")
//                    parentName: "tuttle/"
//                }
//            }
//        ]
//        transitions: [
//            Transition {
//                NumberAnimation { target: nodeMenuView; property: "height"; duration: 200 }
//                NumberAnimation { target: nodeMenuView; property: "opacity"; duration: 200 }
//            }
//        ]

//    }
//}

    

