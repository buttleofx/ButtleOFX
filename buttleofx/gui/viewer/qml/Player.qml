import QtQuick 1.1
import QtDesktop 0.1
import TimerPlayer 1.0

Item {
    id: player
    implicitWidth: 950
    implicitHeight: 400

    property variant node

    TimerPlayer {
        //class Timer defined in python
        //property associated : frame, acces with timer.frame
        id: timer
    }

    QtObject {
        id: timeProperties
        property real currentTime : 0 // current position of the time (milliseconds)
        property real formerKeyTime : 0 // position of the time before animation starts
        
        // for video
        // frames per second of the video, fps and nbFrames are QProperties declared in nodeWrapper.py
        property real fps: node ? node.fps : 1
        // number total of frames of the video 
        property int nbFrames: node ? node.nbFrames : 0
        // timeDuration is the duration of the video
        property real timeDuration : node ? nbFrames/fps*1000 : 0
    }


    // Displays an integer with 2 digits
    function with2digits(n) {
        return n > 9 ? "" + n: "0" + n;
    }

    // Returns the string displayed under the viewer. It's the current time.
    function getTimePosition() {
        var totalSeconds = Math.floor(timeProperties.timeDuration / 1000)
        var totalMinutes = Math.floor(totalSeconds / 60)
        var totalHours = Math.floor(totalMinutes / 60)

        var elapsedSeconds = Math.floor(timeProperties.currentTime / 1000)
        var elapsedMinutes = Math.floor(totalSeconds / 60)
        var elapsedHours = Math.floor(totalMinutes / 60)

        return with2digits(elapsedHours) + ":" + with2digits(elapsedMinutes) + ":" + with2digits(elapsedSeconds) + " / " + with2digits(totalHours) + ":" + with2digits(totalMinutes) + ":" + with2digits(totalSeconds)
    }

    onNodeChanged: {
        console.log("Node Changed : ", node)
    }

    /*************************** TabBar*************************************/
    Item {
        id: tabBar
        implicitWidth: 950
        implicitHeight: 30
        property color tabColor: "#141414"

        Row{
            spacing: 1
            Rectangle {
                id:tab1
                implicitWidth: 100
                implicitHeight: 200
                radius: 10
                color: tabBar.tabColor
                Text {
                    id: tabLabel
                    anchors.horizontalCenter: parent.horizontalCenter
                    y:10
                    text: "Viewer"
                    color: "white"
                    font.pointSize: 10
                }
            }

            /*Rectangle {
                id: tab2
                implicitWidth: 30
                implicitHeight: 200
                radius: 10
                color: tabBar.tabColor
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#141414" }
                    GradientStop { position: 0.11; color: "#141414" }
                    GradientStop { position: 0.15; color: "#111111" }
                    GradientStop { position: 0.16; color: "#111111" }
                }
                Image {
                    id: addButton
                    source: "../img/plus.png"
                    anchors.centerIn: parent
                }
            }*/
        }
    }

    /********************************Viewer and Tools************************************/
    Rectangle {
        id: viewerAndTools
        height: parent.height - tabBar.height
        width: parent.width
        y: tabBar.height
        color: "#141414"

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
                        //here we send the frame the viewer has to display
                        frameViewer: timer.frame
                        // we moove the cursor of the timeline when the frame is changed
                        onFrameViewerChanged: {
                            cursorTimeline.x = timer.frame * (barTimeline.width - cursorTimeline.width) / timeProperties.nbFrames
                        }
                        //time: timeProperties.currentTime
                        //fps: timeProperties.fps
                        clip: true
                    }
                }
                Loader {
                    sourceComponent: node ? viewer_component : undefined
                    anchors.fill: parent
                }

                Rectangle {
                    id: titleErrorDisplay
                    color: "#00b2a1"
                    width: titleError.width + 20
                    height: titleError.lineCount * 20
                    border.width: 2
                    border.color: "black"
                    state: "hidden"
                   Text {
                        id: titleError
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        anchors.verticalCenter: parent.verticalCenter
                        text: node ? "Can't display node : " + node.name : "No current node"
                    }
                    Rectangle {
                        id: errorDisplay
                        color: "#00b2a1"
                        border.width: 2
                        border.color: "black"
                        anchors.top: parent.bottom
                        anchors.left: parent.left
                        width: errorMessage.width + 20
                        height: errorMessage.lineCount * 20
                        opacity: 0
                        Text {
                            id: errorMessage
                            text: _buttleManager.viewerManager.nodeError
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                        }
                    }

                    MouseArea {
                        id: errorArea
                        anchors.fill: parent
                        onClicked: {
                            errorDisplay.opacity = (errorDisplay.opacity == 0) ? 1 : 0
                            //elements.state = ( elements.state == "hidden") ? "shown" : "hidden"
                        }
                    }
                    states: [
                        State {
                            name: "hidden"
                            when: _buttleManager.viewerManager.nodeError == ""
                            PropertyChanges {
                                target: titleErrorDisplay
                                opacity: 0
                            }
                        }, 
                        State {
                            name: "shown"
                            when: _buttleManager.viewerManager.nodeError != ""
                            PropertyChanges {
                                target: titleErrorDisplay
                                opacity: 1
                            }
                        }
                    ]
                }
            }

            /******************* ToolBar *************************************/
            Rectangle {
                id: toolBarRegion
                y: parent.height + tabBar.height
                width: parent.width
                implicitHeight: 25
                color: "transparent"
                Layout.verticalSizePolicy: Layout.Fixed

                // Tools (zoom, timeline buttons, mosquitos)
                Rectangle {
                    id: tools
                    width: parent.width
                    height: parent.height
                    color: "#141414"
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: "#141414" }
                        GradientStop { position: 0.15; color: "#010101" }
                        GradientStop { position: 0.16; color: "#141414" }
                        GradientStop { position: 1; color: "#141414" }
                    }

                    // WILL BE USED LATER
                    // Zoom tools
/*                    Row {
                        id: zoomTools
                        y: 15
                        spacing : 5

                        // Zoom +
                        Rectangle {
                            id: magGlassIn
                            width: 22
                            height: 15
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
*/
                    Item {
                        anchors.verticalCenter: tools.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 25
                        TimelineTools {
                            timer: timer
                        }
                    }


                    // WILL BE USED LATER
                    // Mosquitos
                   Row {
                        id: selectViewer
                        spacing: 2
                        anchors.right: parent.right
                        anchors.rightMargin: parent.height
                        y: 8

                        // Mosquito
                        Rectangle {
                            id: mosquitoTool
                            width: 28
                            height: 28
                            color : mosquitoMouseArea.containsMouse ? "#343434" : "transparent"
                            radius: 3

                            Image {
                                id: mosquito
                                source: _buttleData.buttlePath + "/gui/img/mosquito/mosquito.png"
                                anchors.centerIn: parent
                            }

                            MouseArea {
                                hoverEnabled: true
                                id: mosquitoMouseArea
                                anchors.fill: parent

                                onPressed: {
                                    _buttleManager.viewerManager.mosquitoDragEvent()
                                }
                            }
                        }

                        // mosquitos numbers
                        Repeater {
                            id: number
                            model: 9

                            Rectangle {
                                id: numberElement
                                width: 28
                                height: 28
                                color: _buttleData.currentViewerIndex == index+1 ? "#343434" : "transparent"
                                radius: 3

                                Text {
                                    text: model.index + 1
                                    color: "white"
                                    anchors.top: parent.top
                                    anchors.topMargin: 6
                                    anchors.left: parent.left
                                    anchors.leftMargin: 12
                                }

                                 MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                        _buttleData.currentViewerIndex = index + 1
                                        _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(index+1)
                                        _buttleEvent.emitViewerChangedSignal()
                                    }
                                }

                                /*states: [
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
                                ]*/
                            }
                        } // Repeater mosquito 

                    } // Row (selectViewer = mosquitos )

                } // Tools Rectangle (zoom, timeline buttons, mosquitos)
            } // Rectangle (toolBarRegion)

            /****************Timeline*******************/
            Item {
                id: timeline
                width: parent.width
                implicitHeight: 10
                property double endPosition : barTimeline.x + barTimeline.width - cursorTimeline.width

                // Playing animation
                /*NumberAnimation {
                     id: playingAnimation
                     target: cursorTimeline
                     properties: "x"
                     from: cursorTimeline.x
                     to: timeline.endPosition
                     duration : timeProperties.timeDuration - timeProperties.formerKeyTime
                }*/

                // main container
                Rectangle {
                    width: parent.width
                    color: "transparent"
                    y: -25
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
                                barTimeline.forceActiveFocus()
                            }
                            onReleased : {
                                timeProperties.formerKeyTime = timeProperties.currentTime
                            }
                        }
                        /*onWidthChanged: {
                            cursorTimeline.x = (timeProperties.currentTime * (barTimeline.width - cursorTimeline.width)) / timeProperties.timeDuration
                        }*/
                    }

                    // cursor timeline (little white rectangle)
                    Rectangle {
                        id: cursorTimeline
                        anchors.verticalCenter: parent.verticalCenter
                        x: timer.frame * (barTimeline.width - cursorTimeline.width) / timeProperties.nbFrames
                        height: 10
                        width: 5
                        radius: 1
                        color: "white"

                        /*onXChanged: {
                            timeProperties.currentTime = (cursorTimeline.x * timeProperties.timeDuration) / (barTimeline.width - cursorTimeline.width);
                        }*/

                        MouseArea{
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.XAxis
                            drag.minimumX: barTimeline.x
                            drag.maximumX: timeline.endPosition
                            anchors.margins: -10 // allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
                           /* onPressed: {
                                playingAnimation.stop();
                                cursorTimeline.forceActiveFocus()
                            }
                            onReleased: {
                                //timer.frame = (cursorTimeline.x * timeProperties.nbFrames) / (barTimeline.width - cursorTimeline.width);
                                timeProperties.formerKeyTime = timeProperties.currentTime
                            }*/
                        }
                    }
                }
            }
        } //ColumnLayout
    } // Viewer & tools
} // Item player

