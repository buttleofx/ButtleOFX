import QtQuick 2.0
import QtQuick.Layouts 1.0

Item {
    id: graphEditor


    ColumnLayout {
        anchors.fill: parent
        spacing: 2

        Tools {
            id: tools
            implicitWidth : parent.width
            Layout.minimumHeight: 40
            Layout.preferredHeight: 40
            implicitHeight: 40
            menuComponent: null

            onClickCreationNode: {
                // console.log("Node created clicking from Tools")
                _buttleManager.nodeManager.creationNode(nodeType, -graph.originX + 20, -graph.originY + 20)
            }
        }
        Graph {
            id: graph
            implicitWidth: parent.width
            Layout.minimumHeight: 100
            implicitHeight: 300
            Layout.fillHeight: true
            clip: true

            onClickCreationNode: {
                // console.log("Node created clicking from Graph")
                _buttleManager.nodeManager.creationNode(nodeType, -graph.originX + graph.mouseX, -graph.originY + graph.mouseY)
            }
        }
    }
}
