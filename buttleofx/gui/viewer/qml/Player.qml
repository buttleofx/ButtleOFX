import QtQuick 2.0
import QtQuick.Layouts 1.0
import TimerPlayer 1.0

import "../../../gui"

Item {
    id: player

    signal buttonCloseClicked(bool clicked)
    signal buttonFullscreenClicked(bool clicked)

    // Remark: in python if there are ten frames, they are numbered from 0 to 9 so we need some time to add 1 for display
    property variant node
    property real nodeFps: node ? node.fps : 25
    property int nodeNbFrames: node ? node.nbFrames : 1
    property real nodeDurationSeconds: node ? node.nbFrames/node.fps : 0
    property bool isPlaying: false

    property int lastView: 1 // The last view where the user was
    property variant lastNodeWrapper

    TimerPlayer {
        //Class Timer defined in python
        // property associated: frame, acces with timer.frame
        id: timer
        fps: nodeFps
        nbFrames: nodeNbFrames
    }

    property variant timer: timer

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

    // Changes the viewer: displays the vew n°indexViewer.
    // It updates in ButtleData all informations of the current viewer : the nodeWrapper, the viewerIndex, the frame, and it sets the right frame on the timeline.
    function changeViewer(indexViewer) {
        // First we save the frame for the current node, to be able to retrieve the frame later
        if (_buttleData.currentViewerNodeWrapper != null)
            _buttleData.assignNodeToViewerIndex(_buttleData.currentViewerNodeWrapper, timer.frame)

        // Then we change the viewer
        _buttleData.currentViewerIndex = indexViewer
        _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(indexViewer)

        // And we change the frame of the viewer (if there isn't a node in this view, returns 0)
        var frame = _buttleData.getFrameByViewerIndex(indexViewer)
        _buttleData.currentViewerFrame = frame
        timer.frame = frame

        _buttleEvent.emitViewerChangedSignal()
    }

    function doAction(action) {
        timelineTools.doAction(action)
    }

    onNodeChanged: {
        // console.log("Node Changed : ", node)
    }

    Tab {
        id: tabBar
        name: "Viewer"
        onCloseClicked: player.buttonCloseClicked(true)
        onFullscreenClicked: player.buttonFullscreenClicked(true)
    }

    // Viewer and Tools
    Rectangle {
        id: viewerAndTools
        implicitHeight: parent.height - tabBar.height
        implicitWidth: parent.width
        y: tabBar.height
        color: "#141414"

        ColumnLayout {
            // Viewer
            anchors.fill: parent

            Rectangle {
                id: viewerRegion
                implicitWidth: parent.width
                color: "transparent"
                Layout.minimumHeight: 5
                Layout.preferredHeight: parent.height - toolBarRegion.implicitHeight
                Layout.preferredWidth: parent.width - 10

                Component {
                    id: viewer_component

                    Viewer {
                        id: viewer
                        // Here we send the frame the viewer has to display
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
                    implicitWidth: titleError.width + 20
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
                        implicitWidth: errorMessage.width + 20
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

            // ToolBar
            Rectangle {
                id: toolBarRegion

                property int impHeightValue: 50

                y: parent.height + tabBar.height
                implicitWidth: parent.width
                color: "transparent"
                // Layout.minimumWidth: 700
                Layout.preferredHeight: 50
                Layout.preferredWidth: parent.width

                // Tools (zoom, timeline buttons, mosquitos)
                Rectangle {
                    id: tools
                    implicitWidth: parent.width
                    // height: parent.height
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

                    // Mosquitoes element (buttons to select the viewer)
                    Row {
                        id: selectViewer

                        property int yValue: 8
                        y: yValue

                        spacing: 2
                        anchors.right: parent.right
                        anchors.rightMargin: parent.height

                        // When there isn't enough place to display this element and the timeline tools on the same line, we display them with 2 lines
                        onXChanged: {
                            if (selectViewer.x < 350) {
                                toolBarRegion.implicitHeight = toolBarRegion.impHeightValue * 2
                                // selectViewer.y = selectViewer.yValue + selectViewer.height - 3
                                selectViewer.y = selectViewer.yValue + selectViewer.height - 3
                            } else {
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
                            color: mosquitoMouseArea.containsMouse ? "#343434" : "transparent"
                            radius: 3

                            Image {
                                id: mosquito
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/mosquito/mosquito.png"
                                anchors.centerIn: parent
                            }

                            Drag.active: mosquitoMouseArea.drag.active
                            Drag.hotSpot.x: 14
                            Drag.hotSpot.y: 14
                            // Drag.dragType: Drag.Automatic
                            Drag.keys: "mosquitoMouseArea"

                            MouseArea {
                                id: mosquitoMouseArea
                                anchors.fill: parent
                                hoverEnabled: true
                                onReleased: parent.Drag.drop()
                                drag.target: parent
                            }
                        }

                        // Mosquitoes numbers
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
                                        _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                        _buttleData.currentGraphIsGraph()

                                        player.changeViewer(index+1)
                                        player.lastView = index+1
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

            // Timeline
            Item {
                id: timeline
                implicitWidth: parent.width
                implicitHeight: 10
                anchors.bottom: toolBarRegion.top

                // Main container
                Rectangle {
                    implicitWidth: parent.width
                    color: "transparent"
                    y: 10

                    Rectangle {
                        id: barTimeline
                        anchors.verticalCenter: parent.verticalCenter
                        implicitWidth: parent.width
                        height: 2

                        Rectangle {
                            id: whiteBar
                            x: barTimeline.x
                            width: cursorTimeline.x - barTimeline.x + cursorTimeline.width/2
                            height: parent.height
                            color: "white"
                        }

                        Rectangle {
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

                    // Cursor timeline (little white rectangle)
                    Rectangle {
                        id: cursorTimeline
                        anchors.verticalCenter: parent.verticalCenter

                        property int frame: timer ? timer.frame : 0
                        x: barTimeline.x + (frame * barTimeline.width / nodeNbFrames) - cursorTimeline.width/2
                        height: 10
                        width: 5
                        radius: 1
                        color: "white"

                        MouseArea {
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.XAxis
                            drag.minimumX: barTimeline.x
                            drag.maximumX: barTimeline.x + barTimeline.width
                            // Allow to have an area around the cursor which allows to select the cursor even if we are not exactly on it
                            anchors.margins: -10

                            onPressed: {
                                timer.pause()  // Stop if it was playing
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
        }
    }
}
