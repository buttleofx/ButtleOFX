import QtQuick 1.1
//import Qt 4.7 //useless?
//import QtMultimediaKit 1.1

Rectangle {
    id: container
    implicitWidth: 850
    implicitHeight: 400
    clip: true
    color: "#212121"
    property url imageFile: _graphWrapper.getWrapper(_graphWrapper.getCurrentNode()).getImage()

    property color backColor: "#212121"
    property color toolbarColor: "#141414"
    property color textColor: "white"

    property double sizeScaleEvent: 0.1
    property int sizeDragEvent: 5
    property double sizeScaleFirstImage: 0.95

    //y of the toolBar of the bottom is 5% of the player, PROBLEM HERE
    property int toolHeight: 2

    TabBar{}

    Viewer {}

    // New Tools Bar
    Rectangle {
            id: tools
            width: parent.width
            //before height: 20
            height: 5/100 * parent.height 
            anchors.bottom: parent.bottom
            color: toolbarColor

            Rectangle {
                id: magGlassIn
                width: parent.height
                height: parent.height
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
                            color: "red"}
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
                width: parent.height
                height: parent.height
                x: parent.height + parent.height/2
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
                            color: "red"}
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

    // Old Tools bar
    /*Rectangle {
         id: tools
         width: parent.width
         height: 20
         anchors.bottom: parent.bottom
         color: toolbarColor
         Rectangle {
             id: zoomInButton
             width: 20
             height: 20
             anchors.verticalCenter: parent.verticalCenter
             color: "transparent"
             Text {
                 id: plusButton
                 anchors.centerIn: parent
                 text: "+"
                 font.pointSize: 16
                 color: textColor
             }
             MouseArea {
                 anchors.fill: parent
                 onClicked: {
                     console.log("Zoom in")
                     imageViewed.scale += sizeScaleEvent
                 }

             }
         }
         Rectangle {
             id: zoomOutButton
             width: 20
             height: 20
             x: 20
             anchors.verticalCenter: parent.verticalCenter
             color: "transparent"
             Text {
                 anchors.centerIn: parent
                 text: "-"
                 font.pointSize: 16
                 color: textColor
             }
             MouseArea {
                 anchors.fill: parent
                 onClicked: {
                     console.log("Zoom out")
                     if (imageViewed.scale-sizeScaleEvent > 0) {
                       imageViewed.scale -= sizeScaleEvent
                     }
                 }
             }
          }

         Rectangle {
             id: resetButton
             width: 20
             height: 20
             x: 40
             anchors.verticalCenter: parent.verticalCenter
             color: "transparent"
             Text {
                 anchors.centerIn: parent
                 text: "="
                 font.pointSize: 16
                 color: textColor
             }
             MouseArea {
                 anchors.fill: parent
                 onClicked: {
                     console.log("Reset");
                     imageViewed.scale = 1;
                     imageViewed.x = (container.width - imageViewed.width) / 2;
                     imageViewed.y = (container.height - tools.height - imageViewed.height) / 2;

                 }
             }
          }
     }*/





}
