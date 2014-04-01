import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0

ApplicationWindow {
    id: pluginList

    property color background: "#141414"
    property color backgroundInput: "#343434"
    property color borderInput: "#444"

    property color textColor : "white"
    property alias searchPluginText : searchPlugin.text
    property alias searchPlugin: searchPlugin
    property bool graphEditor

    width: 200
    height: 250
    flags: Qt.FramelessWindowHint | Qt.Tool

    Rectangle{
        id: pluginRect
        height: parent.height
        width: parent.width
        color: pluginList.background
        border.width: 1
        border.color: "#333"
        z:2

        Rectangle{
            id: searchBar
            height: 20
            width: parent.width-20
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            x:10
            y:10
            clip: true

            Image{
                id: searchPicture
                source: "file:///" + _buttleData.buttlePath + "/gui/img/icons/search.png"
                height:10
                width:10
                x:5
                y:5
            }
            TextInput {
                id : searchPlugin
                y: 2
                x: 20
                height: parent.height
                width: parent.width
                clip: true
                selectByMouse: true
                selectionColor: "#00b2a1"
                color: "white"
                focus:true

                property variant plugin

                // onFocusChanged:{
                //     if(searchPlugin.visible){
                //         searchPlugin.focus= true
                //     }
                // }
                // onVisibleChanged: {
                //     if(searchPlugin.visible){
                //         searchPlugin.focus= true
                //     }
                // }

                Keys.onPressed: {
                    if ((event.key == Qt.Key_Return)||(event.key == Qt.Key_Enter)) {
                        if (listOfPlugin.model.count==1){
                            plugin= _buttleData.getSinglePluginSuggestion(text).pluginType
                            if (!graphEditor){
                                // we create a new node and connect it to the last but one node of the concerned graph
                                previousNode =_buttleData.lastNode()

                                _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                if (previousNode == undefined)
                                    _buttleManager.nodeManager.creationNode("_buttleData.graph", plugin, 0, 0)
                                else
                                    _buttleManager.nodeManager.creationNode("_buttleData.graph", plugin, previousNode.xCoord+140, previousNode.yCoord)

                                // if there is only one node, we don't connect it
                                if (previousNode != undefined){
                                    newNode = _buttleData.lastNode()
                                    if (newNode.nbInput != 0)
                                        _buttleManager.connectionManager.connectWrappers(previousNode.outputClip, newNode.srcClips.get(0))
                                }
                            }
                            else{
                                if (_buttleData.currentSelectedNodeWrappers.count == 1) {
                                    var selectedNode = _buttleData.currentSelectedNodeWrappers.get(0)
                                    _buttleManager.nodeManager.creationNode("_buttleData.graph", plugin, selectedNode.xCoord+140, selectedNode.yCoord)
                                    var createdNode = _buttleData.lastNode()
                                    if (createdNode.nbInput != 0)
                                        _buttleManager.connectionManager.connectWrappers(selectedNode.outputClip, createdNode.srcClips.get(0))
                                }
                                else 
                                    _buttleManager.nodeManager.creationNode("_buttleData.graph", plugin, 0, 0)
                            }
                            pluginVisible=false
                            searchPluginText = ""
                        }
                    }
                }
                Keys.onEscapePressed: {
                    pluginVisible = false
                }
            }
        }

        ScrollView {
            height: parent.height-42
            width: parent.width-2
            y:41
            x:1
            
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

            ListView {
                id: listOfPlugin
                height: count ? contentHeight : 0
                interactive: false
                focus: true
                model: _buttleData.getPluginsWrappersSuggestions(searchPlugin.text)

                delegate: Component {
                    Rectangle {
                        id: nodes
                        color: "#141414"
                        border.color:"transparent"
                        border.width: 1
                        radius: 3
                        width: 200-10
                        height: 30
                        x: 3

                        Keys.onPressed: {
                            //previous plugin
                            if (event.key == Qt.Key_Up){
                                console.debug("up")
                                listOfPlugin.currentItem.color="#141414"
                                listOfPlugin.currentItem.border.color="transparent"
                                listOfPlugin.currentIndex = listOfPlugin.currentIndex>0? listOfPlugin.currentIndex-1:listOfPlugin.currentIndex
                                listOfPlugin.currentItem.color="#242424"
                                listOfPlugin.currentItem.border.color="#343434"
                            }

                            //next plugin
                            if (event.key == Qt.Key_Down){
                                console.debug("down")
                                listOfPlugin.currentItem.color="#141414"
                                listOfPlugin.currentItem.border.color="transparent"
                                listOfPlugin.currentIndex = listOfPlugin.currentIndex<listOfPlugin.count-1? listOfPlugin.currentIndex+1:listOfPlugin.currentIndex
                                listOfPlugin.currentItem.color="#242424"
                                listOfPlugin.currentItem.border.color="#343434"
                            }

                            if (event.key == Qt.Key_Return){
                                console.debug("add")
                                listOfPlugin.currentItem.color="#333"
                                listOfPlugin.currentItem.border.color="#343434"
                                if (!graphEditor){
                                    // we create a new node and connect it to the last but one node of the concerned graph
                                    previousNode =_buttleData.lastNode()

                                    _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                    if (previousNode == undefined)
                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                                    else
                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, previousNode.xCoord+140, previousNode.yCoord)

                                    // if there is only one node, we don't connect it
                                    if (previousNode != undefined){
                                        newNode = _buttleData.lastNode()
                                        if (newNode.nbInput != 0)
                                            _buttleManager.connectionManager.connectWrappers(previousNode.outputClip, newNode.srcClips.get(0))
                                    }
                                }
                                else{
                                    if (_buttleData.currentSelectedNodeWrappers.count == 1) {
                                        var selectedNode = _buttleData.currentSelectedNodeWrappers.get(0)
                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, selectedNode.xCoord+140, selectedNode.yCoord)
                                        var createdNode = _buttleData.lastNode()
                                        if (createdNode.nbInput != 0)
                                            _buttleManager.connectionManager.connectWrappers(selectedNode.outputClip, createdNode.srcClips.get(0))
                                    }
                                    else 
                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                                }
                                pluginVisible=false
                                searchPluginText = ""
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: {
                                nodes.color= nodes.color=="#333"? "#333":"#242424"
                                nodes.border.color="#343434"
                            }
                            onExited: {
                                nodes.color= nodes.color=="#333"? "#333":"#141414"
                                nodes.border.color="transparent"
                            }
                            onClicked: {
                                listOfPlugin.currentIndex=index
                                if (!graphEditor){
                                    // we create a new node and connect it to the last but one node of the concerned graph
                                    previousNode =_buttleData.lastNode()

                                    _buttleData.currentGraphWrapper = _buttleData.graphWrapper
                                    if (previousNode == undefined)
                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                                    else
                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, previousNode.xCoord+140, previousNode.yCoord)

                                    // if there is only one node, we don't connect it
                                    if (previousNode != undefined){
                                        newNode = _buttleData.lastNode()
                                        if (newNode.nbInput != 0)
                                            _buttleManager.connectionManager.connectWrappers(previousNode.outputClip, newNode.srcClips.get(0))
                                    }
                                }
                                else{
                                    if (_buttleData.currentSelectedNodeWrappers.count == 1) {
                                        var selectedNode = _buttleData.currentSelectedNodeWrappers.get(0)
                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, selectedNode.xCoord+140, selectedNode.yCoord)
                                        var createdNode = _buttleData.lastNode()
                                        if (createdNode.nbInput != 0)
                                            _buttleManager.connectionManager.connectWrappers(selectedNode.outputClip, createdNode.srcClips.get(0))
                                    }
                                    else 
                                        _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                                }
                                pluginVisible=false
                                searchPluginText = ""
                            }
                        }
                        Text{
                            text: object.pluginLabel
                            color: "white"
                            y:6
                            x:15
                            width: 170
                            elide:Text.ElideRight
                        }
                    }
                }
            }
        }
    }
}

