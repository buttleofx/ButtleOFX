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

        property url imageFile: _buttleData.graphWrapper.currentNodeWrapper.image

        property double sizeScaleEvent: 0.1
        property int sizeDragEvent: 5

        Viewer {}

        ToolBar{}
    }

}
