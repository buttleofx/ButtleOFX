import QtQuick 1.1
import QtDesktop 0.1

Item {
    id: player
    implicitWidth: 950
    implicitHeight: 400

    property variant node

    onNodeChanged: {
        console.log("Node Changed : ", node)
    }

    // TabBar
    Rectangle {
        id: tabBar
        implicitWidth: 950
        implicitHeight: 25
        color: "#353535"
        property color tabColor: "#141414"

        Item {
            id: tab1
            implicitWidth: 100
            implicitHeight: 20
            height: parent.height
            Rectangle {
                anchors {
                    fill: parent;
                    bottomMargin: -radius
                }
                Text {
                    id: tabLabel
                    anchors.horizontalCenter: parent.horizontalCenter
                    y:5
                    text: "Viewer 1"
                    color: "white"
                    font.pointSize: 10
                }
                radius: 10
                color: tabBar.tabColor
            }
        }

        Item {
            id: tab2
            implicitWidth: 30
            height: parent.height
            x: tab1.width + 1
            Rectangle {
                anchors {
                    fill: parent;
                    bottomMargin: -radius
                }
                Image {
                    id: addButton
                    source: "../img/plus.png"
                    anchors.centerIn: parent
                }
                radius: 10
                color: tabBar.tabColor
            }
        }
    }
    //

    Rectangle {
        height: parent.height - tabBar.height
        width: parent.width
        y: tabBar.height
        color: "#141414"
        gradient: Gradient {
            GradientStop { position: 0.085; color: "#141414" }
            GradientStop { position: 1; color: "#111111" }
        }

        ColumnLayout {
            //Viewer
            anchors.fill: parent
            Rectangle {
                id: viewerRegion
                width: parent.width
                color: "transparent"
                Layout.minimumHeight: 50
                Layout.verticalSizePolicy: Layout.Expanding
                Component {
                    id: viewer_component
                    Viewer {
                        id: viewer
                        imageFile: node.image
                        clip: true
                    }
                }
                Loader {
                    sourceComponent: node ? viewer_component : undefined
                    anchors.fill: parent
                }
            }
            //
            Rectangle {
                id: toolBarRegion
                anchors.top: viewerRegion.bottom
                width: parent.width
                implicitHeight: 30
                color: "transparent"
                Layout.verticalSizePolicy: Layout.Fixed
                //ToolBar
                Rectangle {
                    id: tools
                    width: parent.width
                    height: parent.height
                    color: "#141414"

                    // Zoom +
                    Rectangle {
                        id: magGlassIn
                        width: parent.height-4
                        height: parent.height-4
                        x: 2
                        y: 2
                        color: "#141414"

                        Image {
                            id: magGlassInButton
                            source: "../img/zoom_plus.png"
                            anchors.centerIn: parent
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                console.log("Zoom activated")

                                if(magGlassIn.state != "clicked") {
                                    magGlassIn.state = "clicked"
                                    magGlassOut.state = "unclicked"
                                }

                                else {
                                    magGlassIn.state = "unclicked"
                                }
                            }
                        }

                        states: [
                            State {
                                name: "clicked"
                                PropertyChanges {
                                    target: magGlassIn
                                    color: "#212121"}
                               },
                            State {
                            name: "unclicked";
                            PropertyChanges {
                                target: magGlassIn
                                color: "transparent"
                            }
                              }
                        ]
                    }

                    // Zoom -
                    Rectangle {
                        id: magGlassOut
                        width: parent.height-4
                        height: parent.height-4
                        x: parent.height+2
                        y: 2
                        color: "transparent"

                        Image {
                            id: magGlassOutButton
                            source: "../img/zoom_moins.png"
                            anchors.centerIn: parent
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                console.log("ZoomOut activated")
                                if(magGlassOut.state != "clicked") {
                                    magGlassOut.state = "clicked"
                                    magGlassIn.state = "unclicked"
                                }

                                else {
                                    magGlassOut.state = "unclicked"
                                }
                            }
                        }

                        states: [
                            State {
                                name: "clicked"
                                PropertyChanges {
                                    target: magGlassOut
                                    color: "#212121"}
                               },
                            State {
                            name: "unclicked";
                            PropertyChanges {
                                target: magGlassOut
                                color: "transparent"
                            }
                              }
                        ]
                    }

                    Row {
                        id: selectViewer
                        spacing: 5
                        anchors.right: parent.right
                        anchors.rightMargin: parent.height + 1

                        // Mosquito
                        Rectangle {
                            id: mosquitoTool
                            width: parent.height-4
                            height: parent.height-4
                            color: "transparent"
                            y: 4
                            //x: parent.width - 100

                            Image {
                                id: mosquito
                                source: "../img/mosquito.png"
                                anchors.centerIn: parent
                            }
                        }

                        Repeater {
                            id: number
                            model: 9

                            Rectangle {
                                id: numberElement
                                width: tools.height - 4
                                height: tools.height - 4
                                y: 2
                                color: "#343434"
                                radius: 3
                                state: "unclicked"

                                Text {
                                    text: model.index + 1
                                    color: "white"
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.left: parent.left
                                    anchors.leftMargin: 10

                                    //anchors.verticalCenter: parent.verticalCenter
                                }

                                 MouseArea {
                                    anchors.fill: parent
                                    onClicked: { 
                                        for(var i=0; i<9; ++i) {
                                            selectViewer.children[i].state = "unclicked"
                                        }
                                        numberElement.state = "clicked"
                                    }
                                }

                                states: [
                                    State {
                                        name: "clicked"
                                        PropertyChanges {
                                            target: numberElement
                                            color: "#212121"}
                                       },
                                    State {
                                    name: "unclicked";
                                    PropertyChanges {
                                        target: numberElement
                                        color: "transparent"
                                    }
                                      }
                                ]
                            }

                            states: [
                                State {
                                    name: "clicked"
                                    PropertyChanges {
                                        target: numberElement
                                        color: "#212121"}
                                   },
                                State {
                                    name: "unclicked";
                                    PropertyChanges {
                                        target: numberElement
                                        color: "transparent"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
}
