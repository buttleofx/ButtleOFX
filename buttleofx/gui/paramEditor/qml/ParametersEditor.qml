import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQml 2.1
import QtQuick.Controls.Styles 1.0
import QuickMamba 1.0

import "../../../gui"

Item {
    id: parametersEditor
    implicitWidth: 325
    implicitHeight: parent.height

    signal buttonCloseClicked(bool clicked)
    signal buttonFullscreenClicked(bool clicked)

    property variant newNode
    property variant previousNode

    Tab {
        id: tabBar
        name: "Parameters - Advanced Mode"
        onCloseClicked: parametersEditor.buttonCloseClicked(true)
        onFullscreenClicked: parametersEditor.buttonFullscreenClicked(true)
    }

    Rectangle{
        id: paramTitle
        width: parent.width
        height: 40
        y: tabBar.height
        color: "#141414"
        /*gradient: Gradient {
               GradientStop { position: 0.0; color: "#141414" }
               GradientStop { position: 0.85; color: "#141414" }
               GradientStop { position: 0.86; color: "#010101" }
               GradientStop { position: 1; color: "#010101" }
        }*/

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.leftMargin: 10
            color: "white"
            font.pointSize: 11
            text: "Parameters"
            clip: true
        }


    }


    // Container of the paramEditors
    Rectangle{
        id: contentParamEditor
        height: parent.height - paramTitle.height - addNode.height
        width: parent.width
        y: paramTitle.height
        color: "#141414"

        // scroll all the parameditors
        ScrollView {
            id: scrollParam
            //anchors.fill: parent
            width : parent.width
            height: parent.height
            anchors.topMargin: 5
            anchors.bottomMargin: 5

            // for each node we create a ParamEditor
            ListView{
                id: listViewParam
                //anchors.fill: parent
                model: _buttleData.editedNodesWrapper
                delegate: paramDelegate
            }

        }

        // delegate of the list of ParamEditor
        Component {
            id: paramDelegate
            Rectangle{
                height: paramEditor_multiple.height + 50 // 40 : size of paramTitle

                ParamEditorForParametersEditor {
                    id: paramEditor_multiple
                    width: contentParamEditor.width
                    params: model.object ?  model.object.params : null
                    currentParamNode: model.object
                }

            }
        }

    }

    // Add a node
    MouseArea{
        id: addNode
        y : listViewParam.height + paramTitle.height
        width : parent.width
        height : imageAddNode.height + 30


        Image{
            id: imageAddNode
            width: 30
            height : 30
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            source: _buttleData.buttlePath +  "/gui/img/buttons/tools/plus.png"

        }

        onClicked : {
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

                        previousNode =_buttleData.nodeOfParametersEditorToConnect()

                        _buttleData.currentGraphIsGraph()
                        _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                        // if before the viewer was showing an image from the brower, we change the currentView
                        if (_buttleData.currentViewerIndex > 9){
                            _buttleData.currentViewerIndex = 1
                            player.changeViewer(1)
                            _buttleEvent.emitViewerChangedSignal()
                        }
                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object, 0, 0)

                        // if there is only one node, we don't connect it
                        if (_buttleData.nodeOfParametersEditorToConnect().size > 1){
                            console.debug ("_buttleData.nodeOfParametersEditorToConnect()", _buttleData.nodeOfParametersEditorToConnect())
                            newNode = _buttleData.nodeOfParametersEditorToConnect()
                            console.debug("new node qml", newNode)

                            _buttleManager.connectionManager.connectWrappers(previousNode, newNode)
                        }
                    }

                }// menuItem
                onObjectAdded: nodesMenu.insertItem(index, object)
                onObjectRemoved: nodesMenu.removeItem(object)
            } // Instantiator
        } //Menu
}
