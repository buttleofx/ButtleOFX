import QtQuick 1.1

Row {
    anchors.verticalCenter: parent.verticalCenter
    anchors.left: zoomTools.right
    anchors.leftMargin: 50
    spacing: 8
    property int buttonSize : 8

    Text {
        id: textTimeline
        color: "#bbbbbb"
        text: getTimePosition()//define in player
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
                timeProperties.formerKeyTime = timeProperties.currentTime
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
                var xCursorPreviousImage = ((timeProperties.currentTime - 1000/25) * (barTimeline.width - cursorTimeline.width)) / timeProperties.timeDuration // - 1/25 s
                cursorTimeline.x =  xCursorPreviousImage > 0 ? xCursorPreviousImage : 0
                timeProperties.formerKeyTime = timeProperties.currentTime
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
                timeProperties.formerKeyTime = timeProperties.currentTime
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
                var xCursorNextImage = ((timeProperties.currentTime + 1000/25) * (barTimeline.width - cursorTimeline.width)) / timeProperties.timeDuration // + 1/25 s
                cursorTimeline.x = xCursorNextImage < timeline.endPosition ? xCursorNextImage : timeline.endPosition
                timeProperties.formerKeyTime = timeProperties.currentTime
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
                timeProperties.formerKeyTime = timeProperties.currentTime
            }
        }
    }

}
