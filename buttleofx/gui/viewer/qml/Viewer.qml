import QtQuick 1.1

Rectangle {
    id: viewer
    implicitHeight: 300
    implicitWidth: 800
    color: "#141414"
    gradient: Gradient {
        GradientStop { position: 0.085; color: "#141414" }
        GradientStop { position: 1; color: "#111111" }
    }
    property url imageFile: _buttleData.getGraphWrapper().currentImage
    property double sizeScaleFirstImage: 0.95
    property double sizeScaleEvent: 0.1
    property int sizeDragEvent: 5

    Image  {
        id: imageViewed
        source: imageFile
        fillMode: Image.PreserveAspectFit
        height: (parent.height - 30) * sizeScaleFirstImage
        width: parent.width * sizeScaleFirstImage
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        scale: 1
    }

    MouseArea {
        drag.target: imageViewed
        drag.axis: Drag.XandYAxis
        anchors.fill: parent

        onClicked:{
            console.log("image : " + imageFile)
           /* if((mouse.button === Qt.LeftButton)) {
                // Lorsque l'outil Loupe + est activé
                if(magGlassIn.state == "clicked") {
                    imageViewed.x -= (mouseX - viewer.width/2)
                    imageViewed.y -= (mouseY - viewer.height/2)
                    imageViewed.scale += sizeScaleEvent
                }
                // Lorsque l'outil Loupe - est activé
                if(magGlassOut.state == "clicked") {
                    imageViewed.x -= (mouseX - viewer.width/2)
                    imageViewed.y -= (mouseY - viewer.height/2)
                    imageViewed.scale -= sizeScaleEvent
                }
                //Zoom simple
                if(mouse.modifiers & Qt.ShiftModifier){
                    if (imageViewed.scale-sizeScaleEvent > 0) {
                        imageViewed.scale -= sizeScaleEvent
                    }
                }
                else {
                    imageViewed.scale += sizeScaleEvent
                }
            }*/
        }

        Item {
            focus: true
            Keys.onPressed: {
                if (event.modifiers & Qt.ControlModifier) {
                    if (event.key==Qt.Key_Plus) {
                        imageViewed.scale += sizeScaleEvent
                    }
                    else if (event.key==Qt.Key_Minus) {
                        if (imageViewed.scale-sizeScaleEvent > 0) {
                          imageViewed.scale -= sizeScaleEvent
                        }
                    }
                    else if (event.key==Qt.Key_0) {
                        imageViewed.scale = 1;
                        imageViewed.x = (container.width - imageViewed.width) / 2;
                        imageViewed.y = (container.height - tools.height - imageViewed.height) / 2;
                    }
                    else if (event.key==Qt.Key_Left) {
                        imageViewed.x -= sizeDragEvent;
                    }
                    else if (event.key==Qt.Key_Right) {
                        imageViewed.x += sizeDragEvent;
                    }
                    else if (event.key==Qt.Key_Up) {
                        imageViewed.y -= sizeDragEvent;
                    }
                    else if (event.key==Qt.Key_Down) {
                        imageViewed.y += sizeDragEvent;
                    }
                }
            }
        } // Item (for the key events)
    } // viewer MouseArea
} // viewer
