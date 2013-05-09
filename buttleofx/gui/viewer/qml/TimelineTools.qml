import QtQuick 1.1

Item {
    id: timelineTools
    anchors.fill: parent
    //timer comes from Player 
    property variant timer
    property int nbFrames

    function doAction(buttonName) {
        switch (buttonName) {
            case "begin":
                //same result as if we push the stop button
                timer.stop()
                break;

            case "previous":
                timer.previousFrame()
                break;

            case "stop":
                timer.stop()
                break;

            case "pause":
                timer.pause()
                break;

            case "play":
                timer.play()
                break;

            case "next":
                timer.nextFrame()
                break;

            case "end":
                timer.frame = nbFrames - 1
                break;
            default:
                break;
        }
    }

    ListModel {
        id: modelButtonsTimeline
        ListElement { buttonName: "begin"; imageSource: "begin.png"; imageSourceLocked: "begin_locked.png"; imageSourceHover: "begin_hover.png"; state: "normal"}
        ListElement { buttonName: "previous"; imageSource: "previous.png"; imageSourceLocked: "previous_locked.png"; imageSourceHover: "previous_hover.png"; state: "normal" }
        ListElement { buttonName: "stop"; imageSource: "stop.png"; imageSourceLocked: "stop_locked.png"; imageSourceHover: "stop_hover.png"; state: "normal" }
        ListElement { buttonName: "pause"; imageSource: "pause.png"; imageSourceLocked: "pause_locked.png"; imageSourceHover: "pause_hover.png"; state: "normal" }
        ListElement { buttonName: "play"; imageSource: "play.png"; imageSourceLocked: "playlocked.png"; imageSourceHover: "play_hover.png"; state: "normal" }
        ListElement { buttonName: "next"; imageSource: "next.png"; imageSourceLocked: "next_locked.png"; imageSourceHover: "next_hover.png"; state: "normal" }
        ListElement { buttonName: "end"; imageSource: "end.png"; imageSourceLocked: "end_locked.png"; imageSourceHover: "end_hover.png"; state: "normal" }
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

                        property string imgPath: _buttleData.buttlePath + "/gui/img/buttons/viewer/"

                        width: 8
                        height: 8
                        y: 5
                        color: "transparent"

                        Image {
                            id: imageButton
                            source: parent.imgPath + imageSource
                            MouseArea {
                                id: buttonTimelineMousearea
                                hoverEnabled: true
                                anchors.fill: parent
                                anchors.margins: -2 //to allow to push the button easily
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
//                                        source: parent.imgPath + imageSourceLocked
//                                     }
//                                 },
                                 State {
                                     name: "normal"
                                     when: !buttonTimelineMousearea.containsMouse
                                     PropertyChanges {
                                        target: imageButton
                                        source: parent.imgPath + imageSource
                                     }
                                 },
                                 State {
                                     name: "hover"
                                     when: buttonTimelineMousearea.containsMouse
                                     PropertyChanges {
                                        target: imageButton
                                        source: parent.imgPath + imageSourceHover
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
