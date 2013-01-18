import QtQuick 1.1
//import QtMultimediaKit 1.1

Item {
    id: player
    implicitWidth: 850
    implicitHeight: 400
    
    TabBar{
        id: tabBar
        width: parent.width
        height: 25
    }

    Rectangle{
        height: parent.height - tabBar.height
        width: parent.width
        y: tabBar.height
        color: "#141414"
        gradient: Gradient {
            GradientStop { position: 0.085; color: "#141414" }
            GradientStop { position: 1; color: "#111111" }
        }

        Viewer {
            width: parent.width
            height: parent.height
            clip: true
        }

        ToolBar{
            width: parent.width
            height: 25
        }
    }

}
