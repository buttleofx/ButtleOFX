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
        Item {
            implicitWidth: parent.width
            Layout.minimumHeight: 100
            implicitHeight: 300
            Layout.fillHeight: true

            Graph{
                id: graph
                implicitWidth: parent.width
                Layout.minimumHeight: 100
                implicitHeight: 300
                Layout.fillHeight: true
                clip: true
                color: "transparent"
                readOnly: false
                miniatureState: false
                onClickCreationNode: {
                    // console.log("Node created clicking from Graph")
                    _buttleManager.nodeManager.creationNode(nodeType, -graph.originX + graph.mouseX, -graph.originY + graph.mouseY)
                }
            }

            //The miniature of the graph
            Rectangle{
                property real scaleFactor: 0.15
                property real margins: 300
                anchors.top: graph.top
                anchors.right: graph.right
                anchors.margins: 10
                width: graph.width * scaleFactor
                height: (graph.height + margins) * scaleFactor
                color: "#434343"
                opacity: 0.7

                Graph {
                    id: graphMiniature
                    readOnly: true
                    miniatureState: true
                    miniatureScale: parent.scaleFactor
                    width: parent.width
                    height: parent.height - (parent.margins * parent.scaleFactor)
                    color: "transparent"
                    y: (parent.margins * 0.5) * parent.scaleFactor
                    opacity: 1
                }

                Rectangle {
                    id: visuWindow
                    border.color: "white"
                    border.width: 1
                    color: "transparent"
                    anchors.fill: graphMiniature
                }
            }
        }

    }
}
