import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

ApplicationWindow {

    property alias searchPluginText: searchPlugin.text

    property string currentPluginLabel
    property string currentPluginDoc
    property string currentPluginGroup
    property string selectedNodeLabel
    property string selectedNodeDoc
    property string selectedNodeGroup
    property color gradian1: "#010101"
    property color gradian2: "#141414"

    id: pluginsIdentifiers
    x: 400
    y: 400
    width: 800
    height: 600
    color: "#212121"

    SplitView {
        width: parent.width
        height: parent.height
        orientation: Qt.Horizontal

        Rectangle {
            id: list
            height: parent.height
            width: 200
            color: "#141414"
            border.width: 1
            border.color: "#333"

            property string lastGroupParam : "No Group."

            Rectangle {
                id: searchBar
                height: 20
                width: parent.width-20
                color: "#212121"
                border.width: 1
                border.color: "#333"
                radius: 3
                x: 10
                y: 60
                clip: true

                Image {
                    id: searchPicture
                    source: "file:///" + _buttleData.buttlePath + "/gui/img/icons/search.png"
                    height: 10
                    width: 10
                    x: 5
                    y: 5
                }

                TextInput {
                    id: searchPlugin
                    y: 2
                    x: 20
                    height: parent.height
                    width: parent.width
                    clip: true
                    selectByMouse: true
                    selectionColor: "#00b2a1"
                    color: "white"
                    focus: true

                    Keys.onPressed: {
                        // Previous plugin
                        if (event.key == Qt.Key_Up) {
                            pluginList.moveSelectionUp()
                        }
                        // Next plugin
                        else if (event.key == Qt.Key_Down) {
                            pluginList.moveSelectionDown()
                        }
                        else if (event.key == Qt.Key_Enter || event.key == Qt.Key_Return) {
                            pluginList.instanciateSelectedPlugin()
                        }
                    }
                }
            }

            ScrollView {
                height: parent.height-100
                width: parent.width
                y: 100

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

                        Image {
                            id: arrow
                            source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                            x: 4
                            y: 4
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

                        Image {
                            id: arrow
                            source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                            x: 4
                            y: 4
                        }
                    }
                }

                ListView {
                    id: pluginList
                    height: count ? contentHeight : 0
                    interactive: false
                    focus: true
                    currentIndex: 0
                    model: _buttleData.getPluginsWrappersSuggestions(searchPlugin.text)
                    highlightFollowsCurrentItem: true
                    keyNavigationWraps: true

                    Component {
                        id: highlightComponent

                        Rectangle {
                            width: pluginList.currentItem.width
                            height: pluginList.currentItem.height
                            color: "#333"
                            radius: 5
                            y: pluginList.currentItem.y

                            Behavior on y {
                                SpringAnimation {
                                    spring: 3
                                    damping: 0.2
                                }
                            }
                        }
                    }

                    highlight: highlightComponent

                    function moveSelectionUp() {
                        if (pluginList.currentIndex == -1)
                            pluginList.currentIndex = 0
                        else
                            pluginList.decrementCurrentIndex()
                    }

                    function moveSelectionDown() {
                        if (pluginList.currentIndex == -1)
                            pluginList.currentIndex = 0
                        else
                            pluginList.incrementCurrentIndex()
                    }

                    function instanciateSelectedPlugin() {
                        var currentObject = pluginList.model.get(pluginList.currentIndex)
                        currentPluginLabel = currentObject.pluginLabel
                        currentPluginDoc = currentObject.pluginDescription
                        currentPluginGroup = currentObject.pluginGroup
                        searchPluginText = ""
                    }

                    delegate: Component {
                        Rectangle {
                            id: nodes
                            color: "transparent"
                            border.color:"transparent"
                            border.width: 1
                            radius: 3
                            width: 198
                            height: 30
                            x: 1

                            Keys.onPressed: {
                                // Previous plugin
                                if (event.key == Qt.Key_Up) {
                                    pluginList.moveSelectionUp()
                                }
                                // Next plugin
                                else if (event.key == Qt.Key_Down) {
                                    pluginList.moveSelectionDown()
                                }
                                else if (event.key == Qt.Key_Enter || event.key == Qt.Key_Return) {
                                    pluginList.instanciateSelectedPlugin()
                                }
                            }

                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true

                                onEntered: {
                                    pluginList.currentIndex = index
                                }
                                onClicked: {
                                    pluginList.currentIndex = index
                                    pluginList.instanciateSelectedPlugin()
                                }
                            }

                            Text{
                                text: object.pluginLabel
                                color: "white"
                                y: 6
                                x: 15
                                width: 170
                                elide: Text.ElideRight
                            }
                        }
                    }
                }
            }

            Rectangle {
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

        Rectangle {
            id: hint
            height: parent.height
            width: parent.width-list.width
            color: "#141414"
            x: list.width

            Text {
                text:_buttleData.currentSelectedNodeWrappers.count!=0 ? selectedNodeLabel : currentPluginLabel
                color: "white"
                font.pointSize: 11
                wrapMode:Text.Wrap
                width: parent.width-15
                height: parent.height-15
                x: 15
                y: 15
            }

            Text {
                text:_buttleData.currentSelectedNodeWrappers.count!=0 ? selectedNodeGroup : currentPluginGroup
                color: "#00b2a1"
                width: parent.width-15
                height: parent.height-15
                wrapMode:Text.Wrap
                x:15
                y:60
            }

            Text{
                text:_buttleData.currentSelectedNodeWrappers.count!=0 ? selectedNodeDoc : currentPluginDoc
                color: "white"
                width: parent.width-15
                height: parent.height-15
                wrapMode:Text.Wrap
                x: 15
                y: 100
            }
        }
    } // Splitview
}
