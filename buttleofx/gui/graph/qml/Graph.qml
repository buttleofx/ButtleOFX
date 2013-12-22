import QtQuick 2.0
import QuickMamba 1.0

Item {
    id: qml_graphRoot

    QtObject {
        id: m
        property variant graphRoot: qml_graphRoot
    }

    property alias originX: connectnode.x
    property alias originY: connectnode.y

    signal clickCreationNode(string nodeType)
    signal drawSelection(int selectionX, int selectionY, int selectionWidth, int selectionHeight)


    // Selection area
    MouseArea {
        id: leftMouseArea
        property int xStart
        property int yStart
        property bool drawingSelection : false

        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton
        onClicked: {
            if (tools.menuComponent) {
                tools.menuComponent.destroy();
            }
        }
        onPressed: {
            xStart = mouse.x;
            yStart = mouse.y;
            rectangleSelection.x = mouse.x;
            rectangleSelection.y = mouse.y;
            rectangleSelection.width = 1;
            rectangleSelection.height = 1;
            rectangleSelection.visible = true;
            drawingSelection: true;
        }
        onReleased: {
            rectangleSelection.visible = false;
            _buttleData.clearCurrentSelectedNodeNames();
            m.graphRoot.drawSelection(rectangleSelection.x - m.graphRoot.originX, rectangleSelection.y - m.graphRoot.originY, rectangleSelection.width, rectangleSelection.height)
        }

        onPositionChanged: {
            if(mouse.x < xStart){
                rectangleSelection.x = mouse.x
                rectangleSelection.width = xStart - mouse.x;
            }
            else {
                rectangleSelection.width = mouse.x - xStart;
            }
            if(mouse.y < yStart){
                rectangleSelection.y = mouse.y
                rectangleSelection.height = yStart - mouse.y;
            }
            else {
                rectangleSelection.height = mouse.y - yStart;
            }
        }
    }
    onDrawSelection: {
        _buttleData.addNodeWrappersInRectangleSelection(selectionX, selectionY, selectionWidth, selectionHeight);
    }

    /*
    ExternDropArea {
        anchors.fill: parent
        acceptDrop: true
        onDragEnter: {
            acceptDrop = hasUrls
        }
        onDrop: {
            console.log("Drop external files:", acceptDrop)
            if(acceptDrop) {
                _buttleManager.nodeManager.dropFile(firstUrl, pos.x - m.graphRoot.originX, pos.y - m.graphRoot.originY)
            }
        }
    }
    */
    Rectangle {
        id: connectnode
        Item {
            id: nodes
            width: m.graphRoot.width
            height: m.graphRoot.height
            z: 1
            Repeater {
                id: nodesRepeater
                model: _buttleData.graphWrapper.nodeWrappers
                Node {
                    Component.onDestruction: {
                        nodes.forceActiveFocus()
                    }
                    Component.onCompleted: {
                        console.log("test")
                    }
                    objectName: "qmlNode_" + model.object.name
                    graphRoot: m.graphRoot
                }
            }     
        }

        Item {
            id: connections
            width: m.graphRoot.width
            height: m.graphRoot.height
            // We set the z to 0 so the canvas is not over the node's clips
            z: 0

            ListView {
                model : _buttleData.graphWrapper.connectionWrappers
                delegate : Component {
                    Connection {
                        id:connection2
                        connectionModel: model.object
                        Component.onCompleted:{

                        }

                        property variant nodeOut: _buttleData.graphWrapper.getNodeWrapper(connectionModel.out_clipNodeName)
                        property variant clipOut: nodeOut.getClip(connectionModel.out_clipName)

                        property variant nodeIn: _buttleData.graphWrapper.getNodeWrapper(connectionModel.in_clipNodeName)
                        property variant clipIn: nodeIn.getClip(connectionModel.in_clipName)

                        x1: clipOut.coord.x
                        y1: clipOut.coord.y
                        x2: clipIn.coord.x
                        y2: clipIn.coord.y

                         CanvasConnection {
                            id:connection
                            x1: clipOut.coord.x
                            y1: clipOut.coord.y
                            x2: clipIn.coord.x
                            y2: clipIn.coord.y

                            /*DropArea{
                                id: droparea
                                objectName: "DropArea"
                                anchors.fill: parent
                                onDropped: {
                                    drop.accept()
                                    console.log("dropConnection")
                                }
                                onEntered: {
                                    console.log("drag source : "+ drag.source)
                                }
                                Item{
                                    anchors.fill: parent
                                }
                            }*/
                         }
                     }


                    /*
                    Component.onCompleted: {
                        console.log("qml Connection")
                        console.log("connectionModel.out_clipNodeName: ", connectionModel.out_clipNodeName)
                        console.log("connectionModel.in_clipNodeName: ", connectionModel.in_clipNodeName)
                        console.log("connection: ", x1, y1, x2, y2)
                        console.log("nodeOut.coord.y: ", nodeOut.coord.y)
                        console.log("clipOut.coord.y: ", clipOut.coord.y)
                        if(clipOut.coord.y - nodeOut.coord.y < 5)
                        {
                           console.debug("A -- BUG -- node coord is same than clip coord")
                        }
                    }
                    */
                    /*
                    onClipOutChanged: {
                        console.debug("Connection, onClipOutChanged")
                    }
                    onY1Changed: {
                        console.debug("---------------------")
                        console.debug("Connection, Y1 changed", x1)
                        console.log("connection: ", x1, y1, x2, y2)
                        console.log("nodeOut.coord.y: ", nodeOut.coord.y)
                        console.log("clipOut.coord.y: ", clipOut.coord.y)
                        if(clipOut.coord.y - nodeOut.coord.y < 5)
                        {
                            console.debug("B -- BUG -- node coord is same than clip coord")
                        }
                        console.debug("---------------------")
                    }
                    */
                }
            }

            property bool tmpConnectionExists : false
            property string tmpClipName
            property int tmpConnectionX1
            property int tmpConnectionY1
            property int tmpConnectionX2
            property int tmpConnectionY2

            CanvasConnection {
                id: tmpCanvasConnection
                visible: connections.tmpConnectionExists ? 1 : 0
                x1: connections.tmpConnectionX1
                y1: connections.tmpConnectionY1
                x2: connections.tmpConnectionX2
                y2: connections.tmpConnectionY2
            }
        }
    }

    // Rectangle selection is placed here so it is drawn over the nodes
    Rectangle {
        id: rectangleSelection
        color: "white"
        border.color: "#00b2a1"
        opacity: 0.25
        visible: false
    }

    /*
    WheelArea {
        anchors.fill: parent
        property real nbSteps: 5
        onVerticalWheel: {
            if(scale.xScale > 0.3 ) {
                //scale.origin.x = middleMouseArea.mouseX
                //scale.origin.y = middleMouseArea.mouseY
                //console.log(connectnode.width)
                if(delta < 0 && scale.xScale - 0.2 > 0.3 && scale.yScale - 0.2 > 0.3 ) {
                    scale.xScale -= 0.1
                    scale.yScale -= 0.1
                }
                if(delta > 0) {
                    scale.xScale += 0.1
                    scale.yScale += 0.1
                }
            }
        }
    }
    */
}
