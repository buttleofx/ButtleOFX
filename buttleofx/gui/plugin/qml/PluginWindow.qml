import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

ApplicationWindow {

    property variant currentParamNode

    property string currentPluginType
    property string currentPluginDoc
    property string currentPluginGroup
	property color gradian1: "#010101"
    property color gradian2: "#141414"

	id:pluginsIdentifiers
	x: 400
	y: 400
	minimumWidth: 800
	minimumHeight: 600
    maximumWidth: minimumWidth
    maximumHeight: minimumHeight
	color: "#212121"

	Rectangle {
        id: list
        height: parent.height
        width: 200
        color: "#141414"
        border.width: 1
        border.color: "#333"

        property string lastGroupParam : "No Group."

        Rectangle{
            id: searchBar
            height: 20
            width: parent.width-20
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            x:10
            y:60
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

                property variant plugin:_buttleData.getSinglePluginSuggestion(text)

                Keys.onReturnPressed: {
                    if(pluginList.model.count==1){
                        plugin:_buttleData.getSinglePluginSuggestion(text)
                        // using pluginList.model[0] doesn't work
                        currentPluginType=plugin.pluginType
                        currentPluginDoc=plugin.pluginDescription
                        currentPluginGroup=plugin.pluginGroup
                    }
                }
            }
        }

        ScrollView {
            height: parent.height-100
            width: parent.width
            y:100

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
                id: pluginList
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
                        width: 198
                        height: 30
                        x: 1

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
                                aNodeIsSelected=false
                                currentPluginType=object.pluginType
                                currentPluginDoc=object.pluginDescription
                                currentPluginGroup=object.pluginGroup
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

        Rectangle{
            id: pluginTitle
            width: list.width-2
            height: 40
            color: "#141414"
            gradient: Gradient {
                GradientStop { position: 0.0; color: gradian2 }
                GradientStop { position: 0.85; color: gradian2 }
                GradientStop { position: 0.86; color: gradian1 }
                GradientStop { position: 1; color: gradian2 }
            } 

            Text {
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 10
                color: "white"
                font.pointSize: 11
                text: "Plugins"
            }
        }
    }
    Rectangle{
        id: hint
        height: parent.height
        width: parent.width-list.width
        color: "#141414"
        x:list.width
        Text{
            text:aNodeIsSelected? currentParamNode.nodeType : currentPluginType
            color: "white"
            font.pointSize: 11
            horizontalAlignment: Text.Center
            width: parent.width-15
            height: parent.height-15
            x:15
            y:15
        }

        Text{
            text:aNodeIsSelected? currentParamNode.pluginGroup : currentPluginGroup
            color: "#00b2a1"
            width: parent.width-15
            height: parent.height-15
            wrapMode:Text.Wrap
            x:15
            y:60
        }

        Text{
            text:aNodeIsSelected? currentParamNode.pluginDoc : currentPluginDoc
            color: "white"
            width: parent.width-15
            height: parent.height-15
            wrapMode:Text.Wrap
            x:15
            y:100
        }
    }
}
