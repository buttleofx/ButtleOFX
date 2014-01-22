import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

ApplicationWindow {

    property variant currentParamNode
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
        color: "#212121"
        border.width: 1
        border.color: "#333"

        property string lastGroupParam : "No Group."

        ScrollView {
            height: parent.height-40
            width: parent.width
            y:40

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

                model: _buttleData.pluginsIdentifiers

                delegate: Component {
                    Rectangle {
                        id: nodes
                        color: "#141414"
                        border.color:"transparent"
                        border.width: 1
                        radius: 3
                        width: 200
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
                            }
                        }
                        Text{
                            text: object
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
            text:currentParamNode.nameUser
            color: "white"
            font.pointSize: 11
            horizontalAlignment: Text.Center
            width: parent.width-15
            height: parent.height-15
            x:15
            y:15

        }

        Text{
            text: currentParamNode.pluginDoc
            color: "white"
            width: parent.width-15
            height: parent.height-15
            wrapMode:Text.Wrap
            x:15
            y:60
        }
    }
}