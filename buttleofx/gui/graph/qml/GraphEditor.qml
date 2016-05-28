import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQuick.Window 2.1
import QtQuick.Controls 1.0

import "../../../gui"
import "../../paramEditor/qml"
import "../../plugin/qml"

Item {
    id: graphEditor

    signal buttonCloseClicked(bool clicked)
    signal buttonFullscreenClicked(bool clicked)

    Tab {
        id: tabBar
        name: urlOfFileToSave == "" ? "Graph:    Untitled graph" : "Graph:    " + _buttleData.getFileName(urlOfFileToSave)
        onCloseClicked: graphEditor.buttonCloseClicked(true)
        onFullscreenClicked: graphEditor.buttonFullscreenClicked(true)
    }

    property bool editNode: false
    property bool pluginVisible: false

    Keys.onTabPressed: {
        pluginVisible = true
    }

    // List of plugins
    PluginBrowser {
        id: pluginBrowser
        visible: pluginVisible
        graphEditor: true
        x: leftColumn.width
        y: topLeftView.height + mainWindowQML.y + 74

        StateGroup {
            id: statesBrowser
            states: [
                State {
                    name: "view1&2"
                    when: selectedView == 3

                    PropertyChanges {
                        target: pluginBrowser
                        x: mainWindowQML.x + 13
                    }
                },
                State {
                    name: "view3"
                    when: selectedView != 3

                    PropertyChanges {
                        target: pluginBrowser
                        x: leftColumn.width + mainWindowQML.x + 13
                    }
                }
            ]
        }
    }

//    ParamButtleEditor {
//        id: paramButtleEditor
//        visible: editNode
//        currentParamNode: _buttleData.currentParamNodeWrapper
//        /*
//        TODO
//        property point pos: worldToScene(currentParamNode.coord)
//        x: pos.x
//        y: pos.y
//        */
//        x: _buttleData.currentParamNodeWrapper ? (currentParamNode.coord.x + 80) * graph.zoomCoeff + graph.offsetX +
//            (1-graph.zoomCoeff)*420 + leftColumn.width: 0
//        y: _buttleData.currentParamNodeWrapper ? (currentParamNode.coord.y + 95)*graph.zoomCoeff  + graph.offsetY +
//            (1-graph.zoomCoeff)*200 + topLeftView.height + 35 + mainWindowQML.y: 0
//    }

    ColumnLayout {
        anchors.fill: parent
        anchors.topMargin: tabBar.height
        spacing: 2

        Tools {
            id: tools
            // y: tabBar.height
            implicitWidth: parent.width
            Layout.minimumHeight: 40
            Layout.preferredHeight: 40
            implicitHeight: 40
            menuComponent: null

            onClickCreationNode: {
                // console.log("Node created clicking from Tools")
                _buttleData.setActiveGraphId("graphEditor")
                _buttleManager.nodeManager.creationNode("graphEditor", nodeType, -graph.originX + 20, -graph.originY + 20)
            }
        }

        Item {
            implicitWidth: parent.width
            Layout.minimumHeight: 100
            implicitHeight: 300
            Layout.fillHeight: true

            Graph {
                id: graph
                implicitWidth: parent.width
                height: parent.height
                Layout.fillHeight: true
                clip: true
                color: "transparent"
                readOnly: false
                miniatureState: false

                onClickCreationNode: {
                    // console.log("Node created clicking from Graph")
                    _buttleData.setActiveGraphId("graphEditor")
                    _buttleManager.nodeManager.creationNode("graphEditor", nodeType, -graph.originX + graph.mouseX, -graph.originY + graph.mouseY)
                }

                MouseArea {
                    id: leftMouseArea
                    property real xStart
                    property real yStart
                    property real graphContainer_xStart
                    property real graphContainer_yStart

                    property bool drawingSelection: false
                    property bool selectMode: true
                    property bool moveMode: false

                    z: -1
                    anchors.fill: parent
                    hoverEnabled: true
                    acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton

                    onPressed: {
                        // console.debug("graph.zoomCoef: " + graph.zoomCoeff)
                        // console.debug("graph.origin: " + graph.originX + ", " + graph.originY)
                        // console.debug("mouse: " + mouse.x + ", " + mouse.y)

                        pluginVisible=false
                        editNode=false
                        xStart = mouse.x
                        yStart = mouse.y
                        graphContainer_xStart = graph.originX
                        graphContainer_yStart = graph.originY

                        rectangleSelection.x = mouse.x
                        rectangleSelection.y = mouse.y
                        rectangleSelection.width = 1
                        rectangleSelection.height = 1
                        moveMode = (mouse.buttons & Qt.MiddleButton) ||
                                   ((mouse.buttons & Qt.RightButton) && (mouse.modifiers & Qt.ControlModifier))
                        selectMode = (mouse.buttons & Qt.LeftButton)

                        if (selectMode) {
                            rectangleSelection.visible = true
                            drawingSelection = true
                        }
                    }

                    function updateGraphOriginDuringMove(mouse) {
                        var xOffset = (mouse.x - xStart) / graph.zoomCoeff
                        var yOffset = (mouse.y - yStart) / graph.zoomCoeff
                        graph.originX = graphContainer_xStart + xOffset
                        graph.originY = graphContainer_yStart + yOffset

                    }

                    onReleased: {
                        if (moveMode) {
                            updateGraphOriginDuringMove(mouse)
                            moveMode=false
                        }
                        else if (selectMode) {
                            rectangleSelection.visible = false
                            _buttleData.clearCurrentSelectedNodeNames()
                            graph.selectionRect(rectangleSelection.x - graph.originX, rectangleSelection.y - graph.originY,
                                                rectangleSelection.width, rectangleSelection.height)
                        }
                    }

                    onPositionChanged: {
                        if (moveMode) {
                            updateGraphOriginDuringMove(mouse)
                        } else if (selectMode) {
                            if (mouse.x < xStart) {
                                rectangleSelection.x = mouse.x
                                rectangleSelection.width = xStart - mouse.x
                            } else {
                                rectangleSelection.width = mouse.x - xStart
                            }

                            if (mouse.y < yStart) {
                                rectangleSelection.y = mouse.y
                                rectangleSelection.height = yStart - mouse.y
                            } else {
                                rectangleSelection.height = mouse.y - yStart
                            }
                        }
                    }

                    onWheel: {
                        var zoomStep = wheel.angleDelta.y > 0 ? graph.zoomSensitivity : 1.0 / graph.zoomSensitivity

                        // console.debug("graph.zoomCoef: " + graph.zoomCoeff)
                        // console.debug("graph.origin: " + graph.originX + ", " + graph.originY)
                        // console.debug("wheel mouse: " + wheel.x + ", " + wheel.y)

                        var mouseNoZoom = Qt.point(wheel.x / graph.zoomCoeff, wheel.y / graph.zoomCoeff)
                        // mouse position if we apply the new zoom (without translate compensation)
                        graph.zoomCoeff *= zoomStep
                        var mouseNewZoom = Qt.point(mouseNoZoom.x * graph.zoomCoeff, mouseNoZoom.y * graph.zoomCoeff)
                        var offsetCompensation = Qt.point((wheel.x - mouseNewZoom.x) / graph.zoomCoeff,
                                                          (wheel.y - mouseNewZoom.y) / graph.zoomCoeff)

                        graph.originX += offsetCompensation.x
                        graph.originY += offsetCompensation.y
                    }
                }


                function selectionRect(selectionX, selectionY, selectionWidth, selectionHeight) {
                    // remap coordinates from MouseArea to graph frame
                    _buttleData.addNodeWrappersInRectangleSelection(selectionX / container.width * graph.width,
                                                                    selectionY / container.width * graph.width,
                                                                    selectionWidth / graph.zoomCoeff,
                                                                    selectionHeight / graph.zoomCoeff)
                }

                Rectangle {
                    id: rectangleSelection
                    color: "white"
                    border.color: "#00b2a1"
                    opacity: 0.25
                    visible: false
                }
            }

            GraphMiniature{
                id:graphMiniature

                anchors.top: graph.top
                anchors.right: graph.right
                anchors.margins: 10
                width: graph.width * scaleFactor
                height: graph.height * scaleFactor

                color: "#434343"
                opacity: 0.7
                clip: true
                visible: false

                property real scaleFactor: 0.05
            }
        }
    }
}
