import QtQuick 2.0

Item {
    id: connectionItem
    property variant connectionModel

    property int x1
    property int y1
    property int x2
    property int y2

    CanvasConnection {
        id: connection

        x1: parent.x1
        y1: parent.y1
        x2: parent.x2
        y2: parent.y2

        state: "normal"

        QtObject {
            id: m
            property variant connectionModel: connectionItem.connectionModel
        }

        MouseArea {
            // Returns true if we click on the curve
            function intersectPath(mouseX, mouseY, margin){
                for(var x = mouseX - margin; x< mouseX + margin; x++){
                    for(var y = mouseY - margin; y< mouseY + margin; y++){
                        if(connection.getContext("2d").isPointInPath(x, y)){
                            return true;
                        }
                    }
                }
                return false;
            }

            anchors.fill: parent
            hoverEnabled: true

            //Propagate the event to the connections below
            onPressed: mouse.accepted = intersectPath(mouseX, mouseY, 5)
            onClicked: {
                _buttleData.currentConnectionWrapper = m.connectionModel
                _buttleData.clearCurrentSelectedNodeNames();
            }

            // The accepted property of the MouseEvent parameter is ignored in this handler.
            onPositionChanged: {
                mouse.accepted = intersectPath(mouseX, mouseY, 5)
            }
        }

        StateGroup{
            id: stateConnection
            states: [
                State {
                    name: "selectedConnection"
                    when: m.connectionModel == _buttleData.currentConnectionWrapper
                    PropertyChanges { target: connection; r: 187; g: 187; b: 187 }
                },
                State {
                    name: "normal"
                    when: m.connectionModel != _buttleData.currentConnectionWrapper
                    PropertyChanges { target: connection; r: 0; g: 178; b: 161 }
                }
            ]
            // Need to re-paint the connection after each change of state.
            onStateChanged: {
                connection.requestPaint()
            }
        }
    }
}
