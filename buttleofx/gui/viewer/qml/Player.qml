import QtQuick 1.1

Item {
    id: player
    width: 850
    height: 400
    z: 1
    clip: true

    property variant node

    onNodeChanged: {
        console.log("Node Changed : ", node)
    }
    
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
        color: "#141414"
        gradient: Gradient {
            GradientStop { position: 0.085; color: "#141414" }
            GradientStop { position: 1; color: "#111111" }
        }

        Loader {
            sourceComponent: node ? viewer_component : undefined
            anchors.fill: parent
            Component {
                id: viewer_component
                Viewer {
                    id: viewer
                    anchors.fill: parent
                    imageFile: node.image
                    clip: true
                }
            }
        }

        ToolBar{
            id: toolBar
            width: parent.width
            height: 25
        }
    }
}
