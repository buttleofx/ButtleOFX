import QtQuick 1.1
import QtDesktop 0.1

Item {
    id: player
    implicitWidth: 850
    implicitHeight: 400

    property variant node

    onNodeChanged: {
        console.log("Node Changed : ", node)
    }

    TabBar {
        id: tabBar
        width: parent.width
        height: 25
    }

    //presence of the rectangle just avoid a little bug of display
    Rectangle {
        height: parent.height - tabBar.height
        width: parent.width
        y: tabBar.height
        color: "#141414"
        gradient: Gradient {
            GradientStop { position: 0.085; color: "#141414" }
            GradientStop { position: 1; color: "#111111" }
        }

        ColumnLayout {
            anchors.fill: parent

            Rectangle {
                id: viewerRegion
                color: "yellow"
                width: parent.width
                Layout.minimumHeight: 50
                Layout.verticalSizePolicy: Layout.Expanding

                Component {
                    id: viewer_component

                    Viewer {
                        id: viewer
                        imageFile: node.image
                        clip: true
                    }
                }
                Loader {
                    sourceComponent: node ? viewer_component : undefined
                    anchors.fill: parent
                }
            }
            Rectangle {
                id: toolBarRegion
                anchors.top: viewerRegion.bottom
                width: parent.width
                implicitHeight: 30
                Layout.verticalSizePolicy: Layout.Fixed
                ToolBar {
                    id: toolBar
                    anchors.fill: parent
                }
            }
        }
    }
}
