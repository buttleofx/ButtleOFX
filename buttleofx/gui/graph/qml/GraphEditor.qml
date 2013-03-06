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

        onClickCreationNode: {
            console.log("Node created clicking from Graph")
            _buttleManager.creationNode(nodeType, -graph.originX + graph.mouseX , -graph.originY + graph.mouseY)
        }
    }

    Tools {
        id: tools
        width : parent.width
        height: 40
        menuComponent: null

        onClickCreationNode: {
            console.log("Node created clicking from Tools")
            _buttleManager.creationNode(nodeType, -graph.originX + 20, -graph.originY + 20)
        }
    }

    // Function to create a node on a precise position
    //function nodeCreation(nodeType, insertPosX, insertPosY){
    //    _buttleData.creationNode(nodeType)
    //    _buttleData.graphWrapper.getLastCreatedNodeWrapper().coord = Qt.point(insertPosX, insertPosY)
    //}

}
