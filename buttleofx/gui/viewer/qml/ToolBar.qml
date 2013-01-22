import QtQuick 1.1

Rectangle {
    id: tools
    width: parent.width
    height: parent.height
    color: "#141414"

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
}
