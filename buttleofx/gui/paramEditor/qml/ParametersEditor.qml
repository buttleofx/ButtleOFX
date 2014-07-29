import QtQml 2.1
import QtQuick 2.0
import QuickMamba 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0
import "../../../gui"
import "qmlComponents"
import "../../plugin/qml"

Item {
    id: parametersEditor
    implicitWidth: 300
    implicitHeight: 500

    signal buttonCloseClicked(bool clicked)
    signal buttonFullscreenClicked(bool clicked)

    property variant newNode
    property variant previousNode
    property bool displayGraph

    MouseArea {
        anchors.fill:parent

        onClicked:{
            pluginVisible =false
        }
    }

    // property variant clipWrapper

    Tab {
        id: tabBar
        name: "Parameters - Advanced Mode"
        onCloseClicked: parametersEditor.buttonCloseClicked(true)
        onFullscreenClicked: parametersEditor.buttonFullscreenClicked(true)
    }

    property bool pluginVisible:false

    // List of plugins
    PluginBrowser {
        id: pluginBrowser
        visible: pluginVisible
        x: leftColumn.width + mainWindowQML.x + addNode.width / 2 - width / 2
        y: mainWindowQML.y + mainWindowQML.height - 302
    }

    // Drag & Drop from Browser to ParametersEditor
    DropArea {
        anchors.fill: parent
        keys: "internFileDrag"

        onDropped: {
            _buttleData.currentGraphWrapper = _buttleData.graphWrapper
            _buttleData.currentGraphIsGraph()
            // If before the viewer was showing an image from the brower, we change the currentView
            if (_buttleData.currentViewerIndex > 9) {
                _buttleData.currentViewerIndex = player.lastView
                if (player.lastNodeWrapper != undefined)
                    _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                player.changeViewer(player.lastView)
            }

            for (var urlIndex in drag.source.selectedFiles) {
                _buttleManager.nodeManager.dropFile(drag.source.selectedFiles[urlIndex], 10 * urlIndex, 10 * urlIndex)
            }
        }
    }

    // Container of the paramNodes
    Rectangle {
        id: contentparamNode
        height: parent.height - tabBar.height - addNode.height - 50
        width: parent.width
        y: tabBar.height + 50
        color: "#141414"

        // Scroll all the paramNodes
        ScrollView {
            id: scrollParam
            // anchors.fill: parent
            width: parent.width
            height: parent.height
            anchors.topMargin: 5
            anchors.bottomMargin: 5
            y: 10

            style: ScrollViewStyle {
                scrollBarBackground: Rectangle {
                    id: scrollBar
                    width: 15
                    color: "#212121"
                    border.width: 1
                    border.color: "#333"
                }

                decrementControl : Rectangle {
                    id: scrollLower
                    width: 15
                    height: 15
                    color: styleData.pressed? "#212121" : "#343434"
                    border.width: 1
                    border.color: "#333"
                    radius: 3

                    Image {
                        id: arrow
                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                        x: 4
                        y: 4
                    }
                }
                incrementControl : Rectangle {
                    id: scrollHigher
                    width: 15
                    height: 15
                    color: styleData.pressed? "#212121" : "#343434"
                    border.width: 1
                    border.color: "#333"
                    radius: 3

                    Image {
                        id: arrow
                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                        x: 4
                        y: 4
                    }
                }
            }

            // For each node we create a paramNode
            ListView {
                id: listViewParam
                // anchors.fill: parent
                model: _buttleData.graphCanBeSaved? _buttleData.getSortedNodesWrapper():_buttleData.getSortedNodesWrapper()
                delegate: paramDelegate
            }
        }

        // Delegate of the list of paramNode
        Component {
            id: paramDelegate

            Rectangle {
                id: paramNode
                height: tuttleParamContent.height + tuttleParamTitle.height + 10
                width: contentparamNode.width
                implicitWidth: 300
                implicitHeight: 500
                Layout.minimumHeight: tuttleParamTitle.height
                color: "#141414"

                property variant params: model.object ? model.object.params : null
                property variant currentParamNode: model.object

                property color backgroundInput: "#343434"
                property color borderInput: "#444"

                property color activeFocusOn: "white"
                property color activeFocusOff: "grey"

                // Title of the node
                Rectangle {
                    id: tuttleParamTitle
                    height: 40
                    implicitWidth: paramNode.width
                    implicitHeight: 40
                    color: "#141414"

                    gradient: Gradient {
                        GradientStop { position: 0.0; color: "#141414" }
                        GradientStop { position: 0.85; color: "#141414" }
                        GradientStop { position: 0.86; color: "#00b2a1" }
                        GradientStop { position: 1; color: "#141414" }
                    }

                    Image {
                        source: tuttleParamContent.visible ? "file:///" + _buttleData.buttlePath +
                            "/gui/img/buttons/params/arrow_hover.png" : "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow_right.png"
                        width: 12
                        height: 12
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.topMargin: 8
                        anchors.rightMargin: 20
                    }

                    Text {
                        id: name
                        color: "white"
                        text: currentParamNode.name
                        anchors.top: parent.top
                        anchors.topMargin: 4
                        anchors.left: parent.left
                        anchors.leftMargin: 50
                        font.pointSize: 11
                        clip: true
                    }

                    Rectangle {
                        id: deadMosquito
                        width: 23
                        height: 21
                        x: tuttleParamTitle.x + 23
                        y: tuttleParamTitle.y + 3
                        state: "normal"
                        color: "transparent"

                        Image {
                            id: deadMosquitoImage
                            anchors.fill: parent
                        }

                        StateGroup {
                            id: stateViewerNode
                            states: [
                                State {
                                    name: "normal"
                                    when: paramNode.currentParamNode != _buttleData.currentViewerNodeWrapper

                                    PropertyChanges {
                                        target: deadMosquitoImage
                                        source: ""
                                    }
                                },
                                State {
                                    name: "currentViewerNode"
                                    when: paramNode.currentParamNode == _buttleData.currentViewerNodeWrapper

                                    PropertyChanges {
                                        target: deadMosquitoImage
                                        source: "file:///" + _buttleData.buttlePath + "/gui/img/mosquito/mosquito_dead.png"
                                    }
                                }
                            ]
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        acceptedButtons: Qt.LeftButton | Qt.MidButton

                        onPressed: {
                            pluginVisible =false

                            if (mouse.button == Qt.LeftButton) {
                                if (tuttleParamContent.visible == true) {
                                    tuttleParamContent.visible = false
                                    tuttleParamContent.height = 0
                                } else {
                                    // tuttleParamContent.height = newHeight
                                    tuttleParamContent.height = tuttleParam.contentHeight + 20
                                    tuttleParamContent.visible = true
                                }
                            } else if (mouse.button == Qt.MidButton) {
                                _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                _buttleData.currentViewerNodeWrapper = paramNode.currentParamNode
                                _buttleData.currentViewerFrame = 0
                                // We assign the node to the viewer, at the frame 0
                                _buttleData.assignNodeToViewerIndex(paramNode.currentParamNode, 0)
                                _buttleEvent.emitViewerChangedSignal()
                            }
                        }
                    }

                    DropArea {
                        anchors.fill: parent
                        keys: "mosquitoMouseArea"

                        onDropped: {
                            _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                            _buttleData.currentViewerNodeWrapper = paramNode.currentParamNode
                            _buttleData.currentViewerFrame = 0
                            // We assign the node to the viewer, at the frame 0
                            _buttleData.assignNodeToViewerIndex(paramNode.currentParamNode, 0)
                            _buttleEvent.emitViewerChangedSignal()
                        }
                    }

                    Image {
                        id: upNode
                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                        x: 8
                        y: 0

                        MouseArea {
                            id: upNodeMouseArea
                            anchors.fill: parent
                            hoverEnabled: true

                            onClicked: {
                                listViewParam.currentIndex = index
                                _buttleData.nodeGoesUp(listViewParam.currentIndex)

                                if (listViewParam.currentIndex > 0) {
                                    var firstUpNode = _buttleData.graphWrapper.getNodeWrapperByIndex(index - 1)
                                    var secondUpNode = _buttleData.graphWrapper.getNodeWrapperByIndex(index)

                                    if (firstUpNode.pluginContext != "OfxImageEffectContextReader")
                                        _buttleManager.connectionManager.switchNodes(firstUpNode,secondUpNode)
                                }
                            }
                        }

                        StateGroup {
                            id: upNodeStateButtonEvents
                            states: [

                                State {
                                    name: "reader"
                                    when: currentParamNode.pluginContext == "OfxImageEffectContextReader"

                                    PropertyChanges {
                                        target: upNode
                                        source: ""
                                    }
                                },
                                State {
                                    name: "hover"
                                    when: upNodeMouseArea.containsMouse

                                    PropertyChanges {
                                        target: upNode
                                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2_hover.png"
                                    }
                                }
                            ]
                        }
                    }

                    Image {
                        id: downNode
                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                        x: 8
                        y: 20

                        MouseArea {
                            id: downNodeMouseArea
                            anchors.fill: parent
                            hoverEnabled: true

                            onClicked: {
                                listViewParam.currentIndex = index
                                _buttleData.nodeGoesDown(listViewParam.currentIndex)

                                if (listViewParam.count - 1 > listViewParam.currentIndex) {
                                    var firstDownNode = _buttleData.graphWrapper.getNodeWrapperByIndex(index)
                                    var secondDownNode = _buttleData.graphWrapper.getNodeWrapperByIndex(index + 1)

                                    if (firstDownNode.pluginContext != "OfxImageEffectContextReader")
                                        _buttleManager.connectionManager.switchNodes(firstDownNode,secondDownNode)
                                }
                            }
                        }

                        StateGroup {
                            id: downNodeStateButtonEvents

                            states: [
                                State {
                                    name: "reader"
                                    when: currentParamNode.pluginContext == "OfxImageEffectContextReader"

                                    PropertyChanges {
                                        target: downNode
                                        source: ""
                                    }
                                },
                                State {
                                    name: "hover"
                                    when: downNodeMouseArea.containsMouse

                                    PropertyChanges {
                                        target: downNode
                                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow_hover.png"
                                    }
                                }
                            ]
                        }
                    }

                    Image {
                        id: closeButton
                        source: "file:///" + _buttleData.buttlePath + "/gui/img/icons/close.png"
                        width: 10
                        height: 10
                        x: name.x + name.width + 5
                        y: name.y + 4

                        MouseArea {
                            id: closeMouseArea
                            anchors.fill: parent
                            hoverEnabled: true

                            onClicked: {
                                _buttleManager.connectionManager.reconnect(name.text)
                            }
                        }

                        StateGroup {
                            id: stateButtonEvents

                            states: [
                                State {
                                    name: "hover"
                                    when: closeMouseArea.containsMouse

                                    PropertyChanges {
                                        target: closeButton
                                        source: "file:///" + _buttleData.buttlePath + "/gui/img/icons/close_hover.png"
                                    }
                                }
                            ]
                        }
                    }
                }


                // Params depend on the node type (Tuttle data)
                Rectangle {
                    id: tuttleParamContent
                    height: index == listViewParam.count-1 ? tuttleParam.contentHeight + 20 : 0
                    width: parent.width
                    y: tuttleParamTitle.height
                    visible: index == listViewParam.count-1 ? true : false
                    color: "transparent"
                    property string lastGroupParam: "No Group."

                    ListView {
                        id: tuttleParam
                        anchors.fill: parent
                        anchors.topMargin: 10
                        anchors.bottomMargin: 10
                        height: count ? tuttleParam.contentHeight : 0
                        y: parent.y + 10
                        spacing: 6
                        interactive: false
                        model: paramNode.params

                        delegate: Component {
                            Loader {
                                id: param
                                source: model.object.paramType + ".qml"
                                width: parent.width
                                x: 15 // Here is the distance to the left of the listview
                                z: 0

                                ToolTip {
                                    id: tooltip
                                    visible: false
                                    paramHelp: model.object.doc
                                    z: param.z + 1
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    acceptedButtons: Qt.RightButton
                                    hoverEnabled:true

                                    onClicked: {
                                        model.object.hasChanged = false
                                        model.object.value = model.object.getDefaultValue()
                                        model.object.pushValue(model.object.value)
                                    }
                                    onEntered: {
                                        tooltip.visible=true
                                    }
                                    onExited: {
                                        tooltip.visible=false
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // Add a node
    Button {
        id: addNode
        anchors.bottom: parent.bottom
        // y: listViewParam.height
        width: parent.width
        height: 50

        iconSource:
        if (hovered) {
            "file:///" + _buttleData.buttlePath + "/gui/img/buttons/tools/bigplus_hover.png"
        } else {
            "file:///" + _buttleData.buttlePath + "/gui/img/buttons/tools/bigplus.png"
        }

        style:
        ButtonStyle {
            background: Rectangle {
                anchors.fill: parent
                color: "transparent"
            }
        }

        onClicked: {
            if (pluginVisible == false) {
                pluginVisible = true
            } else {
                pluginVisible = false
            }
        }
    }

    Button {
        id: displayTheGraph

        property string imageSource: hovered ? "file:///" + _buttleData.buttlePath +
            "/gui/img/buttons/tools/plus_hover.png": "file:///" + _buttleData.buttlePath + "/gui/img/buttons/tools/plus.png"

        anchors.top: parent.top
        anchors.topMargin: 25
        anchors.left: parent.left
        width: parent.width
        height: 43

        iconSource: imageSource

        style:
        ButtonStyle {
            background: Rectangle {
                anchors.fill: parent
                color: "transparent"
            }
        }

        onClicked: {
            displayGraph = !displayGraph
        }

        StateGroup {
            id: states

            states: [
                State {
                    name: "browser"
                    when: !displayGraph

                    PropertyChanges {
                        target: displayTheGraph
                        imageSource: hovered ? "file:///" + _buttleData.buttlePath +
                            "/gui/img/buttons/params/graph_hover.png" : "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/graph.png"
                    }
                },
                State {
                    name: "graph"
                    when: displayGraph

                    PropertyChanges {
                        target: displayTheGraph
                        imageSource: hovered ? "file:///" + _buttleData.buttlePath +
                            "/gui/img/buttons/params/browser_hover.png" : "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/browser.png"
                    }
                }
            ]
        }
    }

    /*
    Menu {
        id: nodesMenu
        title: "Nodes"

        Instantiator {
            model: _buttleData.pluginsIdentifiers
            MenuItem {
                text: object

                onTriggered: {
                    // We create a new node and connect it to the last but one node of the concerned graph
                    previousNode =_buttleData.lastNode()

                    _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                    if (previousNode == undefined)
                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object, 0, 0)
                    else
                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object, previousNode.xCoord+140, previousNode.yCoord)

                    // If there is only one node, we don't connect it
                    if (previousNode != undefined){
                        newNode = _buttleData.lastNode()
                        _buttleManager.connectionManager.connectWrappers(previousNode.outputClip, newNode.srcClips.get(0))
                    }
                }
            }
            onObjectAdded: nodesMenu.insertItem(index, object)
            onObjectRemoved: nodesMenu.removeItem(object)
        }
    }
    */
}
