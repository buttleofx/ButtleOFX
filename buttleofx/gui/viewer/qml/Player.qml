import QtQuick 1.1
//import Qt 4.7 //useless?
//import QtMultimediaKit 1.1

Item {
    id: player
    implicitWidth: 850
    implicitHeight: 400

    TabBar{}

    Rectangle {
        id: container
        width: parent.width
        height: parent.height-30
        clip: true
        y: 30

        color: "#141414"
        gradient: Gradient {
            GradientStop { position: 0.085; color: "#141414" }
            GradientStop { position: 1; color: "#111111" }
        }

        property double sizeScaleEvent: 0.1
        property int sizeDragEvent: 5

        Viewer {}

Rectangle {
    id: tools
    width: parent.width
    height: 30
    anchors.bottom: parent.bottom
    color: "#141414"

    Rectangle {
        id: magGlassIn
        width: parent.height-4
        height: parent.height-4
        x: 2
        y: 2
        color: "transparent"

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
    }

}
