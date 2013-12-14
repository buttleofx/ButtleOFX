import QtQuick 2.0
import QtQuick.Layouts 1.0
import TimerPlayer 1.0

Item {
    id: player
    implicitWidth: 950
    implicitHeight: 400

    // remark : in python if there are ten frames, they are numbered from 0 to 9 so we need some time to add 1 for display
    property variant node
    property real nodeFps : node ? node.fps :  25
    property int nodeNbFrames: node ? node.nbFrames : 1
    property real nodeDurationSeconds: node ? node.nbFrames/node.fps : 0
    property bool isPlaying: false

    TimerPlayer {
        //class Timer defined in python
        //property associated : frame, acces with timer.frame
        id: timer
        fps: nodeFps 
        nbFrames: nodeNbFrames
    }

    property variant timer : timer

    // Displays an integer with 2 digits
    function with2digits(n) {
        return n > 9 ? "" + n: "0" + n;
    }

    // Returns the string displayed under the viewer. It's the current time.
    function getTimePosition() {
        var totalHours = Math.floor(nodeDurationSeconds / 3600)
        var totalMinutes = Math.floor((nodeDurationSeconds - totalHours*3600) / 60)
        var totalSeconds = Math.floor(nodeDurationSeconds - totalHours*3600 - totalMinutes*60)

        var durationElapsedSeconds = timer ? Math.floor((timer.frame + 1) / timer.fps) : 0
        var elapsedHours = Math.floor(durationElapsedSeconds / 3600)
        var elapsedMinutes = Math.floor((durationElapsedSeconds - elapsedHours*3600) / 60)
        var elapsedSeconds = Math.floor(durationElapsedSeconds - elapsedHours*3600 - elapsedMinutes*60)

        return with2digits(elapsedHours) + ":" + with2digits(elapsedMinutes) + ":" + with2digits(elapsedSeconds) + " / " + with2digits(totalHours) + ":" + with2digits(totalMinutes) + ":" + with2digits(totalSeconds)
    }

    // Changes the viewer : displays the vew n°indexViewer.
    // It updates in ButtleData all informations of the current viewer : the nodeWrapper, the viewerIndex, the frame, and it sets the right frame on the timeline.
    function changeViewer(indexViewer) {
        // first we save the frame for the current node, to be able to retrieve the frame later
        if (_buttleData.currentViewerNodeWrapper != null)
            _buttleData.assignNodeToViewerIndex(_buttleData.currentViewerNodeWrapper, timer.frame)

        // then we change the viewer
        _buttleData.currentViewerIndex = indexViewer
        _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(indexViewer)

        // and we change the frame of the viewer (if there isn't a node in this view, returns 0)
        var frame = _buttleData.getFrameByViewerIndex(indexViewer)
        _buttleData.currentViewerFrame = frame
        timer.frame = frame

        _buttleEvent.emitViewerChangedSignal()
    }

    function doAction(action) {
        timelineTools.doAction(action)
    }

    onNodeChanged: {
        //console.log("Node Changed : ", node)
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
                //color: "transparent"
                color: "blue"
                Layout.minimumHeight: 50
                Layout.fillHeight: true

                Component {
                    id: viewer_component
                    Viewer {
                        id: viewer
                        //here we send the frame the viewer has to display
                        frameViewer: timer ? timer.frame : 0
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

                property int impHeightValue: 25

                y: parent.height + tabBar.height
                width: parent.width
                color: "transparent"
                Layout.minimumWidth : 700
                Layout.preferredHeight: 25
                Layout.preferredWidth: parent.width

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

                    Item {
                        y: 10
                        anchors.left: parent.left
                        anchors.leftMargin: 25
                        TimelineTools {
                            id: timelineTools
                            timer: timer
                            nbFrames: player.nodeNbFrames
                        }
                    }

                    // Mosquitos element (buttons to select the viewer)
                   Row {
                        id: selectViewer

                        property int yValue: 8
                        y: yValue

                        spacing: 2
                        anchors.right: parent.right
                        anchors.rightMargin: parent.height

                        // when there isn't enough place to display this element and the timeline tools on the same line, we display them with 2 lines
                        onXChanged: {
                            if (selectViewer.x < 350) {
                                toolBarRegion.implicitHeight = toolBarRegion.impHeightValue * 2
                                selectViewer.y = selectViewer.yValue + selectViewer.height - 3
                            }
                            else {
                                toolBarRegion.implicitHeight = toolBarRegion.impHeightValue
                                selectViewer.y = selectViewer.yValue
                            }
                        }

                        // Mosquito
                        Rectangle {
                            id: mosquitoTool
                            StateGroup {
                                id: mosquitoState
                                states: State {
                                    name: "dragging"
                                    when: mosquitoMouseArea.pressed
                                    PropertyChanges { target: mosquitoTool; x: mosquitoTool.x; y: mosquitoTool.y }
                                }
                            }
                            width: 28
                            height: 28
                            color : mosquitoMouseArea.containsMouse ? "#343434" : "transparent"
                            radius: 3

                            Image {
                                id: mosquito
                                source: _buttleData.buttlePath + "/gui/img/mosquito/mosquito.png"
                                anchors.centerIn: parent
                            }

                            Drag.active: mosquitoMouseArea.drag.active
                            Drag.hotSpot.x: 14
                            Drag.hotSpot.y: 14

                            MouseArea {
                                id: mosquitoMouseArea
                                anchors.fill: parent

                                hoverEnabled: true

                                drag.target: parent
                                onReleased: {
                                    mosquitoTool.Drag.drop()
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
                                        player.changeViewer(index+1)
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
                anchors.bottom: toolBarRegion.top

                // main container
                Rectangle {
                    width: parent.width
                    color: "transparent"
                    y: 10
                    Rectangle {
                        id: barTimeline
                        anchors.verticalCenter: parent.verticalCenter
                        width: parent.width
                        height: 2

                        Rectangle{
                            id: whiteBar
                            x: barTimeline.x
                            width: cursorTimeline.x - barTimeline.x + cursorTimeline.width/2
                            height: parent.height
                            color: "white"
                        }
                        Rectangle{
                            id: greyBar
                            x: barTimeline.x + cursorTimeline.x + cursorTimeline.width/2
                            width: barTimeline.width - whiteBar.width
                            height: parent.height
                            color: "grey"
                        }
                        MouseArea {
                            anchors.fill : parent
                            anchors.margins: -10
                            onPressed : {
                                // -10 because of margins

                                //cursorTimeline.x = mouse.x - 10 - cursorTimeline.width/2
                                //timer.frame = (cursorTimeline.x + cursorTimeline.width/2) * nodeNbFrames /barTimeline.width;

                                timer.frame = (mouse.x - 10) * nodeNbFrames /barTimeline.width;
                                //timer.pause()
                            }
                        }
                        /* blocks the cursor even if window isn't resize...
                        onWidthChanged: {
                            cursorTimeline.x = timer.frame * (barTimeline.width - cursorTimeline.width/2) / nodeNbFrames;
                        }
                        */
                    }

                    // cursor timeline (little white rectangle)
                    Rectangle {
                        id: cursorTimeline
                        anchors.verticalCenter: parent.verticalCenter

                        property int frame: timer ? timer.frame : 0
                        x: barTimeline.x + (frame * barTimeline.width / nodeNbFrames) - cursorTimeline.width/2
                        height: 10
                        width: 5
                        radius: 1
                        color: "white"

                        MouseArea{
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.XAxis
                            drag.minimumX: barTimeline.x
                            drag.maximumX: barTimeline.x + barTimeline.width
                            anchors.margins: -10  // allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
                            onPressed: {
                                timer.pause()  // stop if it was playing
                                timer.launchProcessGraph()  // used this to use the processGraph (should be faster)
                            }
                            onPositionChanged: {
                                timer.frame = (cursorTimeline.x + cursorTimeline.width/2) * nodeNbFrames / barTimeline.width
                            }
                            onReleased: {
                                timer.pause()  // to close the processGraph launch with onPressed
                            }
                        }
                    }
                }
            }
        } //ColumnLayout
    } // Viewer & tools
} // Item player

