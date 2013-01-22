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

    Rectangle {
        id: tabBarRegion
        width: parent.width
        implicitHeight: 25
        color: "red"
        Layout.verticalSizePolicy: Layout.Fixed
        TabBar {
            id: tabBar
            width: parent.width
            height: 25
        }
    }

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
                width: parent.width
                color: "transparent"
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
                color: "blue"
                Layout.verticalSizePolicy: Layout.Fixed
                ToolBar {
                    id: toolBar
                    anchors.fill: parent
                }
            }
        }
    }
}
