import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

ApplicationWindow {

    property color gradian1: "#010101"
    property color gradian2: "#141414"
    property string currentShortcutContext

    id: shortcutWindow
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

        property string lastGroupParam: "No Group."

        ScrollView {
            height: parent.height-20
            width: parent.width
            y:40

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
                        x:4
                        y:4
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
                        x:4
                        y:4
                    }
                }
            }

            ListView {
                id: shorcutContextList
                height: count ? contentHeight : 0
                interactive: false
                focus: true
                model: _buttleData.getlistOfContext()

                delegate: Component {
                    Rectangle {
                        id: grayRect
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
                                grayRect.color = grayRect.color == "#333" ? "#333" : "#242424"
                                grayRect.border.color = "#343434"
                            }
                            onExited: {
                                grayRect.color= grayRect.color == "#333" ? "#333" : "#141414"
                                grayRect.border.color = "transparent"
                            }
                            onClicked: {
                                shorcutContextList.currentItem.color = "#141414"
                                shorcutContextList.currentItem.border.color = "transparent"
                                shorcutContextList.currentIndex = index
                                shorcutContextList.currentItem.color = "#333"
                                shorcutContextList.currentItem.border.color = "#343434"
                                currentShortcutContext = object
                            }
                        }

                        Text{
                            text: object
                            color: "white"
                            y: 6
                            x: 15
                            width: 170
                            elide:Text.ElideRight
                        }
                    }
                }
            }
        }

        Rectangle {
            id: shortcutContextRect
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
                text: "Context "
            }
        }
    }

    Rectangle {
        id: hint
        height: parent.height
        width: parent.width-list.width
        color: "#141414"
        x: list.width

        ScrollView {
            height: parent.height-38
            width: parent.width
            y: 40

            style: ScrollViewStyle {
                scrollBarBackground: Rectangle {
                    id: scrollBar2
                    width: 15
                    color: "#212121"
                    border.width: 1
                    border.color: "#333"
                }
                decrementControl : Rectangle {
                    id: scrollLower2
                    width: 15
                    height: 15
                    color: styleData.pressed? "#212121" : "#343434"
                    border.width: 1
                    border.color: "#333"
                    radius: 3

                    Image {
                        id: arrow
                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow2.png"
                        x:4
                        y:4
                    }
                }
                incrementControl : Rectangle {
                    id: scrollHigher2
                    width: 15
                    height: 15
                    color: styleData.pressed? "#212121" : "#343434"
                    border.width: 1
                    border.color: "#333"
                    radius: 3

                    Image {
                        id: arrow
                        source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/arrow.png"
                        x:4
                        y:4
                    }
                }
            }

            ListView {
                id: shorcutList
                height: count ? contentHeight : 0
                interactive: false
                focus: true
                model: _buttleData.getlistOfShortcutByContext(currentShortcutContext)

                delegate: Component {
                    Rectangle {
                        id: shortcutRect
                        color: "#141414"
                        border.color: "transparent"
                        border.width: 1
                        radius: 3
                        width: 598
                        height: shortcutDoc.height + 10
                        x: 1
                        y: 10

                        Key {
                            id: firstKey
                            key: object.shortcutKey1
                            x: parent.x + 15
                        }

                        Key {
                            id: secondKey
                            key: object.shortcutKey2
                            x: firstKey.x + firstKey.width + 10
                        }

                        Text {
                            id: shortcutName
                            text: object.shortcutName
                            color: "#00b2a1"
                            width: contentWidth
                            height: parent.height-15
                            wrapMode: Text.Wrap
                            x: secondKey.x + secondKey.width + 20
                            y: 5
                        }

                        Text {
                            id: shortcutDoc
                            text: object.shortcutDoc
                            color: "white"
                            width: shortcutRect.width - x - 20
                            height: lineCount * 15 + 15
                            wrapMode: Text.Wrap
                            x: shortcutName.x + shortcutName.width + 30
                            y: 5
                        }
                    }
                }
            }
        }

        Rectangle {
            id: shortcutListRect
            width: 598
            height: 40
            color: "#141414"

            Text {
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                color: "white"
                font.pointSize: 11
                text: currentShortcutContext
            }
        }
    }
}
