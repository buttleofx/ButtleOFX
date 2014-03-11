import QtQuick 2.0
import QtQuick.Layouts 1.0

import QuickMamba 1.0

Rectangle {
    id: qml_nodeRoot

    property variant graphRoot
    property alias nodeWrapper: m.nodeWrapper
    property bool readOnly
    property real miniatureScale
    property bool miniatureState
    property int nodeWidth: 80
    focus: true

    Drag.active: nodeMouseArea.drag.active

    QtObject {
        id: m
        property variant nodeWrapper
        property variant nodeRoot: qml_nodeRoot

        property int inputSpacing: 10
        property int clipSize: graph.zoomCoeff < 0.3 ? 6 : 9
        property int nbInput: m.nodeWrapper.nbInput
        property int inputTopMargin: 10
        property int outputTopMargin: 10
        property int sideMargin: 10
        //property bool isHighlighted: m.nodeWrapper.isHighlighted
    }
    objectName: "qmlNode_" + m.nodeWrapper.name

    x: m.nodeWrapper.coord.x * graph.zoomCoeff
    y: m.nodeWrapper.coord.y * graph.zoomCoeff
    z: _buttleData.graphWrapper.zMax

    //height: 40
    //width: 120

    signal drawSelection(int x, int y, int width, int height)

    color: "transparent"

    MouseArea {
        id: nodeMouseArea
        anchors.fill: parent
        drag.target: parent
        drag.axis: Drag.XandYAxis
        Drag.keys: "node"
        enabled: !readOnly
        acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MidButton
        property int xstart

        onPressed: {
            pluginVisible=false
            // left button : we change the current selected nodes & we start moving
            if (mouse.button == Qt.LeftButton) {
                // we clear the list of selected connections
                _buttleData.clearCurrentConnectionId()

                // we add the node to the list of selected nodes (if it's not already selected)
                if(!_buttleData.nodeIsSelected(m.nodeWrapper)) {
                    // if the Control Key is not pressed, we clear the list of selected nodes
                    if(!(mouse.modifiers & Qt.ControlModifier))
                          _buttleData.clearCurrentSelectedNodeNames()

                    _buttleData.appendToCurrentSelectedNodeWrappers(m.nodeWrapper)
                }

                _buttleData.graphWrapper.zMax += 1
                parent.z = _buttleData.graphWrapper.zMax
                xstart = mouse.x
                //stateMoving.state = "moving"
                _buttleData.graphWrapper.setTmpMoveNode(m.nodeWrapper.name)
            }

            // right button : we change the current param node
           else if (mouse.button == Qt.RightButton) {
                // Param buttle
                editNode = true
                _buttleData.currentParamNodeWrapper = m.nodeWrapper
            }

            // take the focus
            m.nodeRoot.forceActiveFocus()

            // Highlight parents of selected node
            var parentsToHighlight = _buttleData.getParentNodes()
            for(var i=0; i<parentsToHighlight.count; ++i){
                parentsToHighlight.get(i).isHighlighted = true
            }
        }
        onReleased: {
            var dropStatus = parent.Drag.drop()
            //if (dropStatus !== Qt.IgnoreAction)
            // left button : we end moving
            if (mouse.button == Qt.LeftButton) {
                _buttleManager.nodeManager.nodeMoved(m.nodeWrapper.name, qml_nodeRoot.x / graph.zoomCoeff, qml_nodeRoot.y / graph.zoomCoeff)
            }
             //middle button : assign the node to the viewer
            else if (mouse.button == Qt.MidButton){
                _buttleData.currentGraphIsGraph()
                _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                _buttleData.currentViewerNodeWrapper = m.nodeWrapper
                _buttleData.currentViewerFrame = 0
                // we assign the node to the viewer, at the frame 0
                _buttleData.assignNodeToViewerIndex(m.nodeWrapper, 0)
                _buttleEvent.emitViewerChangedSignal()
                player.lastNodeWrapper = _buttleData.currentViewerNodeWrapper
            }
        }

        // double click : we change the current param node
        onDoubleClicked: {
            aNodeIsSelected=true
            _buttleData.currentParamNodeWrapper = m.nodeWrapper
        }

    }

    DropArea {
        anchors.fill: parent
        keys: "mosquitoMouseArea"

        onDropped: {
            _buttleData.currentGraphIsGraph()
            _buttleData.currentGraphWrapper = _buttleData.graphWrapper
            _buttleData.currentViewerNodeWrapper = m.nodeWrapper
            _buttleData.currentViewerFrame = 0
            // we assign the node to the viewer, at the frame 0
            _buttleData.assignNodeToViewerIndex(m.nodeWrapper, 0)
            _buttleEvent.emitViewerChangedSignal()
            player.lastNodeWrapper = _buttleData.currentViewerNodeWrapper
        }
    }

    Rectangle {
        id: nodeBorder
        anchors.centerIn: parent
        radius: 10

        height: parent.height
        width: parent.width
        color:  m.nodeWrapper.color
        opacity: 0.5

        StateGroup {
            id: stateParamNode
             states: [
                 State {
                     name: "currentParamNode"
                     when: m.nodeWrapper == _buttleData.currentParamNodeWrapper
                     PropertyChanges {
                         target: nodeBorder
                         opacity: 1
                     }
                 },
                 State {
                     name: "highlightNode"
                     when: m.nodeWrapper.isHighlighted == true && m.nodeWrapper != _buttleData.currentParamNodeWrapper
                     //when: m.nodeWrapper == _buttleData.currentParamNodeWrapper
                     PropertyChanges {
                         target: nodeBorder
                         color: m.nodeWrapper.color
                         opacity: 1
                     }
                 }
             ]
        }
    }


    RowLayout {
        id: inputClipsLayout
        anchors.fill: parent

        // inputClips
        Item {
            id: inputClipsItem
            y: parent.height /2
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft


            ListView {
                id: inputClipsContainer
                anchors.verticalCenter: parent.verticalCenter
                width: childrenRect.width
                height: childrenRect.height
                spacing: 5 * qml_graphRoot.zoomCoeff
                model: m.nodeWrapper.srcClips

                delegate: Component {
                    Clip {
                        id: in_clip
                        x_inGraph: qml_nodeRoot.x + inputClipsLayout.x + inputClipsItem.x + inputClipsContainer.x + x
                        y_inGraph: qml_nodeRoot.y + inputClipsLayout.y + inputClipsItem.y + inputClipsContainer.y + y

                        port: "input"
                        clipWrapper: model.object
                        graphRoot: m.nodeRoot.graphRoot
                        nodeRoot: m.nodeRoot
                        clipSize: m.clipSize
                        x:-10
                        readOnly: qml_nodeRoot.readOnly
                        miniatureScale: qml_nodeRoot.miniatureScale
                        miniatureState: qml_nodeRoot.miniatureState
                    }
                }
            }

        }
        Item {
            y: parent.height /2
            Layout.fillWidth: true
        }

        // outputClip
        Item {
            id: outputClipContainer

            y: parent.height /2
            implicitWidth: childrenRect.width
            Layout.preferredWidth: childrenRect.width
            Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
            // always only one output clip
            Clip {
                id: out_clip
                anchors.verticalCenter: parent.verticalCenter
                x_inGraph: qml_nodeRoot.x + outputClipContainer.x + x
                y_inGraph: qml_nodeRoot.y + outputClipContainer.y + y

                port: "output"
                clipWrapper: m.nodeWrapper.outputClip
                graphRoot: m.nodeRoot.graphRoot
                nodeRoot: m.nodeRoot
                clipSize: m.clipSize
                x:10
                readOnly: qml_nodeRoot.readOnly
                miniatureScale: qml_nodeRoot.miniatureScale
                miniatureState: qml_nodeRoot.miniatureState
            }
        }
    }

    Rectangle {
        id: nodeRectangle
        anchors.centerIn: parent
        anchors.fill: parent
        anchors.margins: miniatureState ? 4 * miniatureScale : 4 * graph.zoomCoeff
        color: "#bbbbbb"
        radius: 8
        clip: nodeText.isSelected ? false : true
        Rectangle{
            id: background
            anchors.fill: nodeText
            anchors.leftMargin: -4
            anchors.rightMargin: -4
            color: "#212121"
            opacity: 0.6
            radius: 2
            visible: nodeText.isSelected ? miniatureState ? false : true : false
        }

        Text {
            id: nodeText
            anchors.verticalCenter: isSelected ? undefined : parent.verticalCenter
            anchors.horizontalCenter: isSelected ? parent.horizontalCenter : undefined
            x: isSelected ? nodeWidth * 0.5 * zoomCoeff : 5
            y: isSelected ? nodeWidth * 0.5 * zoomCoeff : 0
            text: m.nodeWrapper.nameUser
            font.pointSize: zoomCoeff < 0.7 ? zoomCoeff < 0.4 ? 6 : 7 : 10
            visible: miniatureState ? false : true
            property bool isSelected: _buttleData.nodeIsSelected(m.nodeWrapper)

            StateGroup {
                id: stateNodeContext
                states: [
                    State {
                        name: "readerAndSrc"
                        when: m.nodeWrapper.pluginContext =="OfxImageEffectContextReader" && m.nodeWrapper.params.get(0).value!=""
                        PropertyChanges {
                            target: nodeText
                            y : isSelected ? nodeWidth * zoomCoeff : nodeWidth * 0.65 * zoomCoeff
                            anchors.verticalCenter: undefined
                        }
                    },
                    State {
                        name: "notReaderOrReaderAndNoSrc"
                        when: m.nodeWrapper.pluginContext !="OfxImageEffectContextReader" || (m.nodeWrapper.pluginContext =="OfxImageEffectContextReader" && m.nodeWrapper.params.get(0).value=="")
                        PropertyChanges {
                            target: nodeText
                            y : isSelected ? nodeWidth * 0.5 * zoomCoeff : 0
                            anchors.verticalCenter: isSelected ? undefined : parent.verticalCenter
                        }
                    }
                ]
            }

            // onTextChanged: {
            //     m.nodeWrapper.fitWidth(nodeText.width);
            //     // _buttleData.graphWrapper.updateConnectionsCoord(m.nodeWrapper);
            // }

            Connections {
                target: _buttleData
                onCurrentSelectedNodeWrappersChanged: {
                    nodeText.isSelected = _buttleData.nodeIsSelected(m.nodeWrapper)
                }
            }
            color: isSelected ? m.nodeWrapper.color : "black"
        }

        Rectangle {
            id: miniPictureRect
            width: miniatureState ? nodeWidth * 0.8 * zoomCoeff * miniatureScale : nodeWidth * 0.8 * zoomCoeff
            height: miniatureState ? nodeWidth * 0.5 * zoomCoeff * miniatureScale : nodeWidth * 0.5 * zoomCoeff
            x: miniatureState ? nodeWidth * 0.05 * zoomCoeff * miniatureScale : nodeWidth * 0.05 * zoomCoeff
            y: miniatureState ? nodeWidth * 0.05 * zoomCoeff * miniatureScale : nodeWidth * 0.05 * zoomCoeff
            radius : 2
            state: "normal"
            color: "transparent"
            visible: miniatureState ? false : true

            Image {
                id: miniPicture
                anchors.fill: parent
                fillMode: Image.PreserveAspectFit
                smooth: true
            }

            StateGroup {
                id: statePicture
                states: [
                    State {
                        name: "reader"
                        when: m.nodeWrapper.pluginContext =="OfxImageEffectContextReader" && m.nodeWrapper.params.get(0).value!=""
                        PropertyChanges {
                            target: miniPicture;
                            source: m.nodeWrapper.params.get(0).value 
                        }
                    },
                    State {
                        name: "notReader"
                        when: m.nodeWrapper.pluginContext !="OfxImageEffectContextReader"
                        PropertyChanges {
                            target: miniPicture;
                            source: ""
                        }
                    }
                ]
            }
        }
    }



    Rectangle {
        id: deadMosquito
        width: miniatureState ? 23 * miniatureScale : 23
        height: miniatureState ? 21 * miniatureScale : 21
        x: m.nodeRoot.width - 12
        y: -10
        state: "normal"
        color: "transparent"
        visible: miniatureState ? false : true

        Image {
            id: deadMosquitoImage
            anchors.fill: parent
         }

        StateGroup {
            id: stateViewerNode
             states: [
                 State {
                     name: "normal"
                     when: m.nodeWrapper != _buttleData.currentViewerNodeWrapper
                     PropertyChanges {
                         target: deadMosquitoImage;
                         source: ""
                     }
                 },
                 State {
                     name: "currentViewerNode"
                     when: m.nodeWrapper == _buttleData.currentViewerNodeWrapper
                     PropertyChanges {
                         target: deadMosquitoImage;
                         source: "file:///" + _buttleData.buttlePath + "/gui/img/mosquito/mosquito_dead.png"
                     }
                 }
             ]
        }
    }

    /*StateGroup {
        id: stateMoving
        state: "normal"
        states: [
            State {
                name: "normal"
                PropertyChanges { target: m.nodeRoot; x: m.nodeWrapper.coord.x; y: m.nodeWrapper.coord.y }
            },
            State {
                name: "moving"
                PropertyChanges { target: m.nodeRoot; x: m.nodeWrapper.coord.x; y: m.nodeWrapper.coord.y }
            }
        ]
    }*/

    StateGroup {
        id: statePressed
        states: [
            State {
                name: "pressed"
                when: nodeMouseArea.pressed
                PropertyChanges { target: m.nodeRoot; opacity: .5 }
            },
            State {
                name: "miniature"
                when: miniatureState
                PropertyChanges {
                      target: m.nodeRoot
                      x: ((m.nodeWrapper.coord.x * graphContainer.width) / qml_graphRoot.width) * miniatureScale
                      y: ((m.nodeWrapper.coord.y * graphContainer.height) / qml_graphRoot.height) * miniatureScale
                }
            }
        ]
    }

    onXChanged: {
        if (nodeMouseArea.drag.active) {
            m.nodeRoot.nodeIsMoving()
        }
    }
    onYChanged: {
        if (nodeMouseArea.drag.active) {
            m.nodeRoot.nodeIsMoving()
        }
    }

    function nodeIsMoving() {
        _buttleManager.nodeManager.nodeIsMoving(m.nodeWrapper.name, m.nodeRoot.x / graph.zoomCoeff, m.nodeRoot.y / graph.zoomCoeff)
    }
}
