import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQml 2.1
import QtQuick.Controls.Styles 1.0
import QtQuick.Layouts 1.0
import QuickMamba 1.0
import "qmlComponents"

import "../../../gui"
import "../../plugin/qml"

Item {
    id: parametersEditor
    implicitWidth: 300
    implicitHeight: 500

    signal buttonCloseClicked(bool clicked)
    signal buttonFullscreenClicked(bool clicked)

    property variant newNode
    property variant previousNode

    MouseArea{
        anchors.fill:parent
        onClicked:{
            pluginVisible =false
        }
    }

//    property variant clipWrapper

    Tab {
        id: tabBar
        name: "Parameters - Advanced Mode"
        onCloseClicked: parametersEditor.buttonCloseClicked(true)
        onFullscreenClicked: parametersEditor.buttonFullscreenClicked(true)
    }

    property bool pluginVisible:false

    //List of plugins
    PluginBrowser {
        id: pluginBrowser
        z:1
        height: 250
        visible:pluginVisible
        y:player.height+50
        x:parametersEditor.width/2-100
    }

    // Drag&Drop from Browser to ParametersEditor
    DropArea {
        anchors.fill: parent
        keys: "internFileDrag"

        onDropped: {
            _buttleData.currentGraphWrapper = _buttleData.graphWrapper
            _buttleData.currentGraphIsGraph()
            // if before the viewer was showing an image from the brower, we change the currentView
            if (_buttleData.currentViewerIndex > 9){
                _buttleData.currentViewerIndex = player.lastView
                if (player.lastNodeWrapper != undefined)
                    _buttleData.currentViewerNodeWrapper = player.lastNodeWrapper
                player.changeViewer(player.lastView)
            }

            for(var urlIndex in drag.source.selectedFiles)
            {
                _buttleManager.nodeManager.dropFile(drag.source.selectedFiles[urlIndex], 10*urlIndex, 10*urlIndex)
            }
        }
    }

    // Container of the paramNodes
    Rectangle{
        id: contentparamNode
        height: parent.height - tabBar.height - addNode.height - 10
        width: parent.width
        y: tabBar.height + 10
        color: "#141414"

        // scroll all the paramNodes
        ScrollView {
            id: scrollParam
            //anchors.fill: parent
            width : parent.width
            height: parent.height
            anchors.topMargin: 5
            anchors.bottomMargin: 5

            style: ScrollViewStyle {
                        scrollBarBackground: Rectangle {
                            id: scrollBar
                            width:15
                            color: "#212121"
                            border.width: 1
                            border.color: "#333"
                        }
                        decrementControl : Rectangle {
                            id: scrollLower
                            width:15
                            height:15
                            color: styleData.pressed? "#212121" : "#343434"
                            border.width: 1
                            border.color: "#333"
                            radius: 3
                            Image{
                                id: arrow
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                                x:4
                                y:4
                            }
                        }
                        incrementControl : Rectangle {
                            id: scrollHigher
                            width:15
                            height:15
                            color: styleData.pressed? "#212121" : "#343434"
                            border.width: 1
                            border.color: "#333"
                            radius: 3
                            Image{
                                id: arrow
                                source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                                x:4
                                y:4
                            }
                        }
                    }

            // for each node we create a paramNode
            ListView{
                id: listViewParam
                //anchors.fill: parent
                model: _buttleData.editedNodesWrapper
                delegate: paramDelegate
            }

        }

        // delegate of the list of paramNode
        Component {
            id: paramDelegate

            Rectangle{
                id: paramNode
                height: tuttleParamContent.height + tuttleParamTitle.height + 10
                width: contentparamNode.width
                implicitWidth: 300
                implicitHeight: 500
                Layout.minimumHeight: tuttleParamTitle.height
                color: "#141414"

                property variant params : model.object ? model.object.params : null
                property variant currentParamNode : model.object

                property color backgroundInput: "#343434"
                property color borderInput: "#444"

                property color activeFocusOn : "white"
                property color activeFocusOff : "grey"


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
                        source: tuttleParamContent.visible ? "file:///" + _buttleData.buttlePath +  "/gui/img/buttons/params/arrow_hover.png" : "file:///" + _buttleData.buttlePath +  "/gui/img/buttons/params/arrow_right.png"
                        width: 12
                        height: 12
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.topMargin: 8
                        anchors.rightMargin: 20
                    }

                    Text{
                        id: name
                        color: "white"
                        text: currentParamNode.name
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 30
                        font.pointSize: 11
                        clip: true
                    }

                    Rectangle {
                        id: deadMosquito
                        width: 23
                        height: 21
                        x: tuttleParamTitle.x + 3
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
                                         target: deadMosquitoImage;
                                         source: ""
                                     }
                                 },
                                 State {
                                     name: "currentViewerNode"
                                     when: paramNode.currentParamNode == _buttleData.currentViewerNodeWrapper
                                     PropertyChanges {
                                         target: deadMosquitoImage;
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
                                 if (tuttleParamContent.visible == true){
                                    tuttleParamContent.visible = false
                                    tuttleParamContent.height = 0
                                }
                                else{
                                    //tuttleParamContent.height = newHeight
                                    tuttleParamContent.height = tuttleParam.contentHeight + 20
                                    tuttleParamContent.visible = true
                                }
                            }
                            else if (mouse.button == Qt.MidButton) {
                                _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                _buttleData.currentViewerNodeWrapper = paramNode.currentParamNode
                                _buttleData.currentViewerFrame = 0
                                // we assign the node to the viewer, at the frame 0
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
                            // we assign the node to the viewer, at the frame 0
                            _buttleData.assignNodeToViewerIndex(paramNode.currentParamNode, 0)
                            _buttleEvent.emitViewerChangedSignal()
                        }
                    }

                    Image {
                        id: closeButton
                        source: "file:///" + _buttleData.buttlePath +  "/gui/img/icons/close.png"
                        width: 10
                        height: 10
                        x: name.x + name.width + 5
                        y: name.y + 4

                        MouseArea {
                            id: closeMouseArea
                            anchors.fill: parent
                            hoverEnabled: true

                            onClicked: {
                                var clips = _buttleData.graphWrapper.deleteNodeWrapper(name.text)
                                if(clips)
                                    _buttleManager.connectionManager.connectWrappers(clips.get(0), clips.get(1))
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
                                         source:  "file:///" + _buttleData.buttlePath +  "/gui/img/icons/close_hover.png"
                                     }
                                 }
                             ]
                        }
                    }
                }


                /* Params depend on the node type (Tuttle data)*/
                Rectangle {
                    id: tuttleParamContent
                    height: index == listViewParam.count-1 ? tuttleParam.contentHeight + 20 : 0
                    width: parent.width
                    y: tuttleParamTitle.height
                    visible: index == listViewParam.count-1 ? true : false
                    color : "transparent"

                    property string lastGroupParam : "No Group."

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
                                source : model.object.paramType + ".qml"
                                width: parent.width
                                x: 15 // here is the distance to the left of the listview
                                z:0

                                ToolTip{
                                    id:tooltip
                                    visible: false
                                    paramHelp: model.object.doc
                                    z:param.z+1
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
                    }//Listview
                }//item param
            }
        }

    }

    // Add a node
    Button {
        id: addNode
        anchors.bottom: parent.bottom
        //y : listViewParam.height
        width : parent.width
        height: 50

        iconSource:
            if (hovered){
                "file:///" + _buttleData.buttlePath +  "/gui/img/buttons/tools/bigplus_hover.png"
            }else{
                "file:///" + _buttleData.buttlePath +  "/gui/img/buttons/tools/bigplus.png"
            }

        style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

        onClicked: {
            if(pluginVisible==false) {pluginVisible=true}
            else {pluginVisible=false}
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
                    // we create a new node and connect it to the last but one node of the concerned graph
                    previousNode =_buttleData.lastNode()

                    _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                    if (previousNode == undefined)
                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object, 0, 0)
                    else
                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object, previousNode.xCoord+140, previousNode.yCoord)

                    // if there is only one node, we don't connect it
                    if (previousNode != undefined){
                        newNode = _buttleData.lastNode()
                        _buttleManager.connectionManager.connectWrappers(previousNode.outputClip, newNode.srcClips.get(0))
                    }
                }
            }// menuItem
            onObjectAdded: nodesMenu.insertItem(index, object)
            onObjectRemoved: nodesMenu.removeItem(object)
        } // Instantiator
    } //Menu
    */
}
