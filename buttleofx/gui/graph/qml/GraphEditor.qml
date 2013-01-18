import QtQuick 1.1

Rectangle {
    id: graphEditor
    width: 850
    height: 350
    z: 0
    property variant graphX: 0
    property variant graphY: 0
    
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
            console.log("Noeud créé en cliquant depuis Tools")
            nodeCreation(nodeType, -graph.originX + 20, -graph.originY + 20)
        }
    }

    function nodeCreation(nodeType, insertPosX, insertPosY){
        _buttleData.getGraphWrapper().creationNode(nodeType)
        _buttleData.getGraphWrapper().getLastCreatedNodeWrapper().coord = Qt.point(insertPosX, insertPosY)
    }

}
