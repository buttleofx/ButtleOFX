import QtQuick 1.1

Rectangle {
    id: graphEditor
    width: 850
    height: 350
    z: 0
    clip: true

    Graph {
        id: graph
        y: 30
        width : parent.width
        height: parent.height
    }

    Tools {
        width : parent.width
        height: 30

        onClickCreationNode: {
            console.log("Noeud created clicking from Tools")
            nodeCreation(nodeType, -graph.originX + 20, -graph.originY + 20)
        }
    }

    // Function to create a node one a precise position
    function nodeCreation(nodeType, insertPosX, insertPosY){
        _buttleData.getGraphWrapper().creationNode(nodeType)
        _buttleData.getGraphWrapper().getLastCreatedNodeWrapper().coord = Qt.point(insertPosX, insertPosY)
    }

}
