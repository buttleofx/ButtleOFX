import QtQuick 1.1

Row {
    anchors.verticalCenter: parent.verticalCenter
    anchors.left: zoomTools.right
    anchors.leftMargin: 50
    spacing: 8
    property int buttonSize : 8

    Text {
        id: textTimeline
        color: "white"
        text: getTimePosition()
    }

    // back to begin
    Rectangle {
        id: beginbutton
        width: parent.buttonSize
        height: parent.buttonSize
        y: 2
        color: "transparent"

        Image {
            source: "../img/begin.png"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                playingAnimation.stop();
                cursorTimeline.x = 0
                player.oldSignalPosition = player.signalPosition
            }
        }
    }

    // previous image
    Rectangle {
        id: previousbutton
        width: parent.buttonSize
        height: parent.buttonSize
        y: 2
        color: "transparent"

        Image {
            source: "../img/previous.png"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                playingAnimation.stop();
                cursorTimeline.x =  ((player.signalPosition - 1000/25) * (barTimeline.width - cursorTimeline.width)) / player.signalDuration // - 1/25 s
                player.oldSignalPosition = player.signalPosition
            }
        }
    }

    // stop
    Rectangle {
        id: stopbutton
        width: parent.buttonSize
        height: parent.buttonSize
        y: 2
        color: "transparent"

        Image {
            source: "../img/stop.png"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                playingAnimation.stop();
                player.oldSignalPosition = player.signalPosition
            }
        }
    }

    // play
    Rectangle {
        id: playbutton
        width: parent.buttonSize
        height: parent.buttonSize
        y: 2
        color: "transparent"

        Image {
            source: "../img/play.png"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                playingAnimation.start();
            }
        }
    }

    // next image
    Rectangle {
        id: nextbutton
        width: parent.buttonSize
        height: parent.buttonSize
        y: 2
        color: "transparent"

        Image {
            source: "../img/next.png"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                playingAnimation.stop();
                cursorTimeline.x =  ((player.signalPosition + 1000/25) * (barTimeline.width - cursorTimeline.width)) / player.signalDuration // + 1/25 s
                player.oldSignalPosition = player.signalPosition
            }
        }
    }

    // go to end
    Rectangle {
        id: endbutton
        width: parent.buttonSize
        height: parent.buttonSize
        y: 2
        color: "transparent"

        Image {
            source: "../img/end.png"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                playingAnimation.stop();
                cursorTimeline.x = timeline.endPosition
                player.oldSignalPosition = player.signalPosition
            }
        }
    }

}
