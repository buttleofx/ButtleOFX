import QtQuick 1.1
import QtDesktop 0.1

Item {
    id: player
    implicitWidth: 950
    implicitHeight: 400

    property variant node

    QtObject {
        id: m
        property real time : 45 // current position of the signal (milliseconds)
        property real oldSignalPosition : 0 // position of the signal before animation start
        property real signalDuration : 10000 // total durqtion of the signal (milliseconds)
    }

    // Displays an integer with 2 digits
    function with2digits(n){
        return n > 9 ? "" + n: "0" + n;
    }

    // Returns the string displayed under the viewer. It's the current position of the signal.
    function getTimePosition() {
        var totalSeconds = Math.floor(player.signalDuration / 1000)
        var totalMinutes = Math.floor(totalSeconds / 60)
        var totalHours = Math.floor(totalMinutes / 60)

        var elapsedSeconds = Math.floor(player.signalPosition / 1000)
        var elapsedMinutes = Math.floor(totalSeconds / 60)
        var elapsedHours = Math.floor(totalMinutes / 60)

        return with2digits(elapsedHours) + ":" + with2digits(elapsedMinutes) + ":" + with2digits(elapsedSeconds) + " / " + with2digits(totalHours) + ":" + with2digits(totalMinutes) + ":" + with2digits(totalSeconds)

    }

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

        onWidthChanged: {
            console.log("jhbjhb")
        }
    }

    // Viewer & tools
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
                        time: m.time
                        clip: true
                    }
                }
                Loader {
                    sourceComponent: node ? viewer_component : undefined
                    anchors.fill: parent
                }
            }


            // Timeline
            Item {
                id: timeline
                anchors.top: viewerRegion.bottom
                width: parent.width
                implicitHeight: 10

                property double endPosition : barTimeline.x + barTimeline.width - cursorTimeline.width

                // Playing animation
                NumberAnimation {
                     id: playingAnimation
                     target: cursorTimeline
                     properties: "x"
                     from: cursorTimeline.x
                     to: timeline.endPosition
                     duration : player.signalDuration - player.oldSignalPosition
                }

                // main container
                Rectangle {
                    width: parent.width
                    height: parent.height
                    color: "transparent"

                    Rectangle {
                        id: barTimeline
                        anchors.verticalCenter: parent.verticalCenter
                        width: parent.width
                        height: 2

                        Rectangle{
                            id: whiteBar
                            x: barTimeline.x
                            width: cursorTimeline.x - barTimeline.x
                            height: parent.height
                            color: "white"
                        }
                        Rectangle{
                            id: greyBar
                            x: barTimeline.x + cursorTimeline.x
                            width: barTimeline.width - whiteBar.width
                            height: parent.height
                            color: "grey"
                        }
                        MouseArea {
                            anchors.fill : parent
                            anchors.margins: -10
                            onPressed : {
                                cursorTimeline.x = mouse.x
                            }
                            onReleased : {
                                player.oldSignalPosition = player.signalPosition
                                //_glViewport.currentTime = player.signalPosition

                            }
                        }
                    }

                    // cursor timeline (little white rectangle)
                    Rectangle {
                        id: cursorTimeline
                        anchors.verticalCenter: parent.verticalCenter
                        x: (player.signalPosition * (barTimeline.width - cursorTimeline.width)) / player.signalDuration
                        height: 10
                        width: 5
                        radius: 1
                        color: "white"

                        onXChanged: {
                            m.time = (cursorTimeline.x * player.signalDuration) / (barTimeline.width - cursorTimeline.width);
                            //_glViewport.currentTime = player.signalPosition
                         }


                        MouseArea{
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.XAxis
                            drag.minimumX: barTimeline.x
                            drag.maximumX: timeline.endPosition
                            anchors.margins: -10 // allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
                            onPressed: {
                                playingAnimation.stop();
                            }
                            onReleased: {
                                player.oldSignalPosition = player.signalPosition
                            }
                        }
                    }
                }
            }




            // ToolBar
            Rectangle {
                id: toolBarRegion
                anchors.top: timeline.bottom
                width: parent.width
                implicitHeight: 30
                color: "transparent"
                Layout.verticalSizePolicy: Layout.Fixed

                // Tools (zoom, timeline buttons, mosquitos)
                Rectangle {
                    id: tools
                    width: parent.width
                    height: parent.height
                    color: "#141414"

                    // zoomTools
                    Row {
                        id: zoomTools
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        spacing : 5

                        // Zoom +
                        Rectangle {
                            id: magGlassIn
                            width: 22
                            height: 15
                            //x: 2
                            //y: 2
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
                                        color: "#212121"
                                    }
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
                            width: 22
                            height: 15
                            //x: parent.height+2
                            //y: 2
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
                                        color: "#212121"
                                    }
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
                    }

                    TimelineTools {}

                    // mosquitos
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

                        // mosquitos numbers
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
                                            color: "#212121"
                                        }
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
                        } // Repeater mosquito
                    } // Row (selectViewer = mosquitos )
                } // Tools Rectangle (zoom, timeline buttons, mosquitos)
            } // Rectangle (toolBarRegion)
        } //ColumnLayout
    } // Viewer & tools
} // Item player

