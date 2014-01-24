import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQml 2.1
import QtQuick.Controls.Styles 1.0
import QtQuick.Layouts 1.0
import QuickMamba 1.0

import "../../../gui"

Item {
    id: parametersEditor
    implicitWidth: 300
    implicitHeight: 500

    signal buttonCloseClicked(bool clicked)
    signal buttonFullscreenClicked(bool clicked)

    property variant newNode
    property variant previousNode

//    property variant clipWrapper

    Tab {
        id: tabBar
        name: "Parameters - Advanced Mode"
        onCloseClicked: parametersEditor.buttonCloseClicked(true)
        onFullscreenClicked: parametersEditor.buttonFullscreenClicked(true)
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
                        source: tuttleParamContent.visible ? _buttleData.buttlePath +  "/gui/img/buttons/params/arrow_hover.png" : _buttleData.buttlePath +  "/gui/img/buttons/params/arrow_right.png"
                        width: 12
                        height: 12
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.topMargin: 8
                        anchors.rightMargin: 20
                    }

                    Text{
                        color: "white"
                        text: currentParamNode.name
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        font.pointSize: 11
                        clip: true
                    }

                    MouseArea {
                        anchors.fill: parent
                        acceptedButtons: Qt.LeftButton | Qt.MidButton

                        onPressed: {
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
                _buttleData.buttlePath +  "/gui/img/buttons/tools/bigplus_hover.png"
            }else{
                _buttleData.buttlePath +  "/gui/img/buttons/tools/bigplus.png"
            }

        style:
            ButtonStyle {
                background: Rectangle {
                    anchors.fill: parent
                    color: "transparent"
                }
            }

        onClicked: {
            console.log("Clic on Add a Node!")
            nodesMenu.popup();
        }
    }

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
                    _buttleManager.nodeManager.creationNode("_buttleData.graph", object, 0, 0)

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

}
