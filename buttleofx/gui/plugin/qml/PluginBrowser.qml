import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0

Item {
    id: pluginList

    property color background: "#141414"
    property color backgroundInput: "#343434"
    property color borderInput: "#444"

    property color textColor : "white"
    property color activeFocusOn : "white"
    property color activeFocusOff : "grey"

    Rectangle{
        id: pluginRect
        height: parent.height
        width: 200
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

                property variant plugin

                Keys.onReturnPressed: {
                    if(listOfPlugin.model.count==1){
                        // using listOfPlugin.model[0] doesn't work
                        _buttleManager.nodeManager.creationNode("_buttleData.graph", _buttleData.getSinglePluginSuggestion(text), 0, 0)
                        pluginVisible=false
                    }
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

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: {
                                nodes.border.color= "#333"
                                nodes.color= "#343434"
                            }
                            onExited: {
                                nodes.color= "#141414"
                                nodes.border.color= "transparent"
                            }
                            onClicked: {
                                pluginVisible=false
                                onTriggered: _buttleManager.nodeManager.creationNode("_buttleData.graph", object.pluginType, 0, 0)
                            }
                        }
                        Text{
                            text: object.pluginType
                            color: "white"
                            y:6
                            x:15
                        }
                    }
                }
            }
        }
    }
}

