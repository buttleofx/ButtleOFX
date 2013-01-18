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

    //presence of the rectangle just avoid a little bug of display
    Rectangle{
        height: parent.height - tabBar.height
        width: parent.width
        y: tabBar.height
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
