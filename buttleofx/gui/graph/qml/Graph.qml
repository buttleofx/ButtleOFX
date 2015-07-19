import QtQuick 2.0
import QtQuick.Dialogs 1.1
import QuickMamba 1.0

Rectangle {
    id: qml_graphRoot  // TODO: rename root
    focus: true

    Keys.onPressed: {
        // Graph toolbar
        if ((event.key == Qt.Key_N) && (event.modifiers & Qt.ControlModifier)) {
            if (!_buttleData.graphCanBeSaved) {
                _buttleData.newData()
            } else {
                newGraph.open()
            }
        }

        if ((event.key == Qt.Key_O) && (event.modifiers & Qt.ControlModifier)) {
            if (!_buttleData.graphCanBeSaved) {
                finderLoadGraph.open()
            } else {
                openGraph.open()
            }
        }

        // Save or save as
        if ((event.key == Qt.Key_S) && (event.modifiers & Qt.ControlModifier)) {
            if (_buttleData.graphCanBeSaved) {
                if (urlOfFileToSave != "") {
                    _buttleData.saveData(urlOfFileToSave)
                } else {
                    finderSaveGraph.open()
                }
            }
        }

        // Send the selected node on the parameters editor
        if ((event.key == Qt.Key_P)) {
            var selectedNodes = _buttleData.currentSelectedNodeWrappers

            // We send the node only if there is only one node selected
            if (selectedNodes.count == 1) {
                var node = selectedNodes.get(0)
                _buttleData.currentParamNodeWrapper = node
            }
        }

        // Plugin window
        if (event.key == Qt.Key_H) {
            doc.show()
        }

        // Assign the mosquito to the selected node
        if ((event.key == Qt.Key_Return)||(event.key == Qt.Key_Enter)) {
            var selectedNodes = _buttleData.currentSelectedNodeWrappers

            // We assign the mosquito only if there is only one node selected
            if (selectedNodes.count == 1) {
                var node = selectedNodes.get(0)
                _buttleData.setActiveNode("graphEditor", node)
                _buttleEvent.emitViewerChangedSignal()
            }
        }

        if (event.key == Qt.Key_Delete) {
            _buttleManager.deleteSelection()
        }
        if ((event.key == Qt.Key_Z) && (event.modifiers & Qt.ControlModifier)) {
            if (_buttleManager.canUndo) {
                _buttleManager.undo()
            }
        }
        if ((event.key == Qt.Key_Y) && (event.modifiers & Qt.ControlModifier)) {
            if (_buttleManager.canRedo) {
                _buttleManager.redo()
            }
        }
        if ((event.key == Qt.Key_D) && (event.modifiers & Qt.ControlModifier)) {
            if (!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                _buttleManager.nodeManager.duplicationNode()
            }
        }
        if ((event.key == Qt.Key_A) && (event.modifiers & Qt.ControlModifier)) {
            _buttleManager.selectAllNodes()
        }
        if ((event.key == Qt.Key_C) && (event.modifiers & Qt.ControlModifier)) {
            if (!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                _buttleManager.nodeManager.copyNode()
            }
        }
        if ((event.key == Qt.Key_V) && (event.modifiers & Qt.ControlModifier)) {
            if (_buttleData.canPaste) {
                _buttleManager.nodeManager.pasteNode()
            }
        }
        if ((event.key == Qt.Key_X) && (event.modifiers & Qt.ControlModifier)) {
            if (!_buttleData.currentSelectedNodeWrappers.isEmpty()) {
                _buttleManager.nodeManager.cutNode()
            }
        }
    }

    QtObject {
        id: m
        property variant graphRoot: qml_graphRoot
    }

    signal clickCreationNode(string nodeType)

    property real zoomCoeff: 1
    property real zoomSensitivity: 1.1
    property real nodeX
    // origin in World coordinates
    property real originX
    property real originY

    property bool readOnly
    property bool miniatureState

    property var container: graphContainer

    /*
    ExternDropArea {
        anchors.fill: parent
        acceptDrop: true
        onDragEnter: {
            acceptDrop = hasUrls
        }
        onDrop: {
            console.log("Drop external files:", acceptDrop)
            if (acceptDrop) {
                _buttleManager.nodeManager.dropFile(firstUrl, pos.x - m.graphRoot.originX, pos.y - m.graphRoot.originY)
            }
        }
    }
    */

    // Drag & Drop from outside the app
    DropArea {
        id: graphDropArea
        anchors.fill: parent
        keys: ["text/uri-list"]

        onDropped: {
            if (!drop.hasUrls) {
                drop.accepted = false
                return
            }

            _buttleData.setActiveGraphId("graphEditor")

            for (var urlIndex in drop.urls) {
                // TODO: screenToScene to take scale into account
                _buttleManager.nodeManager.dropFile(
                    drop.urls[urlIndex],
                    drag.x - m.graphRoot.originX + 10 * urlIndex,
                    drag.y - m.graphRoot.originY + 10 * urlIndex)
            }

            drop.accepted = true
        }
    }

    // Drag & Drop from Browser to Graph
    DropArea {
        anchors.fill: parent
        keys: "internFileDrag"

        onDropped: {
            _buttleData.setActiveGraphId("graphEditor")
            for (var urlIndex in drag.source.selectedFiles) {
                _buttleManager.nodeManager.dropFile(drag.source.selectedFiles[urlIndex], drag.x - m.graphRoot.originX + 10*urlIndex,
                                                    drag.y - m.graphRoot.originY + 10*urlIndex)
            }
        }
    }

    Rectangle {
        id: graphContainer
        x: qml_graphRoot.originX * zoomCoeff
        y: qml_graphRoot.originY * zoomCoeff
        color: "transparent"

        /*
        Item {
            id: repere
            property color repereColor: "red"
            property double size: 50 * zoomCoeff
            property double thickness: 2
            visible: miniatureState ? false : true
            Rectangle {
                id: axeX
                x: -repere.size - 0.5 * repere.thickness
                y: 0
                width: 2 * repere.size + repere.thickness
                height: 2
                color: repere.repereColor
            }
            Rectangle {
                id: axeY
                x: 0
                y: -repere.size - 0.5 * repere.thickness
                width: 2
                height: 2 * repere.size + repere.thickness
                color: repere.repereColor
            }
        }
        */

        Item {
            id: nodes
            anchors.fill: parent
            z: 1

            Repeater {
                id: nodesRepeater
                // model: _buttleData.graphBrowserWrapper.nodeWrappers
                model: _buttleData.graphWrapper.nodeWrappers

                Node {
                    id: node
                    nodeWrapper: model.object
                    graphRoot: m.graphRoot
                    width: nodeWidth * zoomCoeff
                    height: nodeWidth /2 * zoomCoeff
                    readOnly: qml_graphRoot.readOnly
                    miniatureState: qml_graphRoot.miniatureState

                    StateGroup {
                        id: stateViewerNode
                        states: [
                            State {
                                name: "miniatureStateAndReader"
                                when: miniatureState && model.object.pluginContext == "OfxImageEffectContextReader"

                                PropertyChanges {
                                    target: node
                                    width: node.nodeWidth
                                    height: node.nodeWidth
                                }
                            },
                            State {
                                name: "miniatureStateAndNotReader"
                                when: miniatureState && model.object.pluginContext != "OfxImageEffectContextReader"

                                PropertyChanges {
                                    target: node
                                    width: node.nodeWidth
                                    height: node.nodeWidth / 2
                                }
                            },
                            State {
                                name: "readerAndSrc"
                                when: model.object.pluginContext == "OfxImageEffectContextReader" && model.object.params.get(0).value!= ""

                                PropertyChanges {
                                    target: node
                                    width: nodeWidth * zoomCoeff
                                    height: nodeWidth * zoomCoeff
                                }
                            },
                            State {
                                name: "notReaderOrReaderAndNoSrc"
                                when: model.object.pluginContext != "OfxImageEffectContextReader" ||
                                    (model.object.pluginContext == "OfxImageEffectContextReader" && model.object.params.get(0).value== "")

                                PropertyChanges {
                                    target: node
                                    width: nodeWidth * zoomCoeff
                                    height: nodeWidth / 2 * zoomCoeff
                                }
                            }
                        ]
                    }
                }
            }
        }

        Item {
            id: connections
            anchors.fill: parent
            // We set the z to 0 so the canvas is not over the node's clips
            z: 0

            Repeater {
                model: _buttleData.graphWrapper.connectionWrappers
                Connection {
                    id: connection
                    connectionWrapper: model.object
                    property variant nodeOut: _buttleData.graphWrapper.getNodeWrapper(connectionWrapper.out_clipNodeName)
                    property variant clipOut: nodeOut.getClip(connectionWrapper.out_clipName)

                    property variant nodeIn: _buttleData.graphWrapper.getNodeWrapper(connectionWrapper.in_clipNodeName)
                    property variant clipIn: nodeIn.getClip(connectionWrapper.in_clipName)

                    readOnly: qml_graphRoot.readOnly
                    miniatureState: qml_graphRoot.miniatureState

                    x1: clipOut.xCoord
                    y1: clipOut.yCoord
                    x2: clipIn.xCoord
                    y2: clipIn.yCoord

                    visible: connectionWrapper.enabled
                }
            }

            property bool tmpConnectionExists: false
            property string tmpClipName
            property int tmpConnectionX1
            property int tmpConnectionY1
            property int tmpConnectionX2
            property int tmpConnectionY2
            property real alpha: 1

            CanvasConnection {
                id: tmpCanvasConnection
                visible: connections.tmpConnectionExists

                x1: connections.tmpConnectionX1
                y1: connections.tmpConnectionY1
                x2: connections.tmpConnectionX2
                y2: connections.tmpConnectionY2
                opacity: connections.alpha
            }
        }
    }
}
