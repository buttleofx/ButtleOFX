import QtQuick 1.1

Item {
    id: timelineTools
    anchors.fill: parent

    function doAction(buttonName) {
        switch (buttonName) {
            case "begin":
                playingAnimation.stop();
                cursorTimeline.x = 0;
                timeProperties.formerKeyTime = timeProperties.currentTime;
                break;

            case "previous":
                playingAnimation.stop();
                var xCursorPreviousImage = ((timeProperties.currentTime - 1000/25) * (barTimeline.width - cursorTimeline.width)) / timeProperties.timeDuration; // - 1/25 s
                cursorTimeline.x =  xCursorPreviousImage > 0 ? xCursorPreviousImage : 0;
                timeProperties.formerKeyTime = timeProperties.currentTime;
                break;

            case "stop":
                playingAnimation.stop();
                cursorTimeline.x = 0;
                timeProperties.formerKeyTime = timeProperties.currentTime;
                break;

            case "pause":
                playingAnimation.stop();
                timeProperties.formerKeyTime = timeProperties.currentTime;
                break;

            case "play":
                playingAnimation.start();
                break;

            case "next":
                playingAnimation.stop();
                var xCursorNextImage = ((timeProperties.currentTime + 1000/25) * (barTimeline.width - cursorTimeline.width)) / timeProperties.timeDuration; // + 1/25 s
                cursorTimeline.x = xCursorNextImage < timeline.endPosition ? xCursorNextImage : timeline.endPosition;
                timeProperties.formerKeyTime = timeProperties.currentTime
                break;

            case "end":
                playingAnimation.stop();
                cursorTimeline.x = timeline.endPosition;
                timeProperties.formerKeyTime = timeProperties.currentTime;
                break;
            default:
                break;
        }
    }

    ListModel {
        id: modelButtonsTimeline
        ListElement { buttonName: "begin"; imageSource: "../img/begin.png"; imageSourceLocked: "../img/begin_locked.png"; imageSourceHover: "../img/begin_hover.png"; state: "normal"}
        ListElement { buttonName: "previous"; imageSource: "../img/previous.png"; imageSourceLocked: "../img/previous_locked.png"; imageSourceHover: "../img/previous_hover.png"; state: "normal" }
        ListElement { buttonName: "stop"; imageSource: "../img/stop.png"; imageSourceLocked: "../img/stop_locked.png"; imageSourceHover: "../img/stop_hover.png"; state: "normal" }
        ListElement { buttonName: "pause"; imageSource: "../img/pause.png"; imageSourceLocked: "../img/pause_locked.png"; imageSourceHover: "../img/pause_hover.png"; state: "normal" }
        ListElement {  buttonName: "play"; imageSource: "../img/play.png"; imageSourceLocked: "../img/playlocked.png"; imageSourceHover: "../img/play_hover.png"; state: "normal" }
        ListElement { buttonName: "next"; imageSource: "../img/next.png"; imageSourceLocked: "../img/next_locked.png"; imageSourceHover: "../img/next_hover.png"; state: "normal" }
        ListElement { buttonName: "end"; imageSource: "../img/end.png"; imageSourceLocked: "../img/end_locked.png"; imageSourceHover: "../img/end_hover.png"; state: "normal" }
    }

    Text {
        id: textTimeline
        color: "#bbbbbb"
        text: getTimePosition()//define in player
        y: 2
    }
    Item {
        width: 200
        anchors.left: textTimeline.right
        anchors.leftMargin: 20
        ListView {
            anchors.fill: parent
            model: modelButtonsTimeline
            orientation: ListView.Horizontal
            spacing: 20
            interactive: false
            delegate {
                Component {
                    Rectangle {
                        id: buttonTimeline
                        width: 8
                        height: 8
                        y: 5
                        color: "transparent"

                        Image {
                            id: imageButton
                            source: imageSource
                            MouseArea {
                                id: buttonTimelineMousearea
                                hoverEnabled: true
                                anchors.fill: parent
                                onClicked: {
                                    timelineTools.doAction(buttonName)
                                    //take the focus of the mainWindow
                                    imageButton.forceActiveFocus()
                                }
                            }
                        }

                        StateGroup {
                            id: stateButtonEvents
                             states: [
//                                 State {
//                                     name: "locked"
//                                     PropertyChanges {
//                                        target: imageButton
//                                        source: imageSourceLocked
//                                     }
//                                 },
                                 State {
                                     name: "normal"
                                     when: !buttonTimelineMousearea.containsMouse
                                     PropertyChanges {
                                        target: imageButton
                                        source: imageSource
                                     }
                                 },
                                 State {
                                     name: "hover"
                                     when: buttonTimelineMousearea.containsMouse
                                     PropertyChanges {
                                        target: imageButton
                                        source: imageSourceHover
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
