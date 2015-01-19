import QtQuick 2.0
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0
import "../../../gui"
import "qmlComponents"


// Parent of the ParamEditor is the Row of the ButtleApp
Item {
    id: paramEditor

    signal buttonCloseClicked(bool clicked)
    signal buttonFullscreenClicked(bool clicked)

    property variant params
    property variant currentParamNode

    property color background: "#141414"
    property color backgroundInput: "#343434"
    property color gradian1: "#010101"
    property color gradian2: "#141414"
    property color borderInput: "#444"

    property color textColor: "white"
    property color activeFocusOn: "white"
    property color activeFocusOff: "grey"

    implicitWidth: 300
    implicitHeight: 500

    Tab {
        id: tabBar
        name: !_buttleData.currentParamNodeWrapper ? "Parameters" : "Parameters of :    "
                                                     + _buttleData.currentParamNodeWrapper.nameUser
        onCloseClicked: paramEditor.buttonCloseClicked(true)
        onFullscreenClicked: paramEditor.buttonFullscreenClicked(true)
    }

    // Tuttle params
    Rectangle {
        id: tuttleParams
        height: parent.height - 5
        width: parent.width
        y: tabBar.height
        color: paramEditor.background

        // Params depend on the node type (Tuttle data)
        Item {
            id: tuttleParamContent
            height: parent.height
            width: parent.width
            y: 5

            property string lastGroupParam: "No Group."

            Rectangle {
                id: header
                color: paramEditor.background
                height: 21
                width: parent.width
                z: 20

                Item {
                    id: columnHeader1
                    width: resizeBar.x

                    Text {
                        text: "Param Title"
                        color: "white"
                    }
                }

                Rectangle {
                    id: resizeBar
                    width: 50
                    height: 20
                    x: 150
                    color: paramEditor.background

                    Rectangle {
                        id: dragLeft
                        width: 2
                        height: 15
                        color: "#eee"
                        radius: 1
                    }

                    Rectangle {
                        id: dragRight
                        width: 2
                        height: 15
                        color: "#eee"
                        anchors.left: dragLeft.right
                        anchors.margins: 2
                        radius: 1
                    }

                    MouseArea {
                        anchors.fill: parent
                        drag.target: resizeBar
                        drag.axis: Drag.XAxis
                        drag.minimumX: 0
                        drag.maximumX: tuttleParams.width
                    }
                }

                Item {
                    id: columnHeader2
                    Layout.fillWidth: true
                    anchors.left: resizeBar.right

                    Rectangle {
                        width: header.width
                        height: header.height
                        color: paramEditor.background
                        Text {
                            text: "Param Value"
                            color: "white"
                        }
                    }
                }
            }

            ScrollView {
                anchors.fill: parent
                anchors.topMargin: 30
                anchors.bottomMargin: 15
                height: 110
                width: 110
                z: 0

                style: ScrollViewStyle {
                    scrollBarBackground: Rectangle {
                        id: scrollBar
                        width: 15
                        color: "#212121"
                        border.width: 1
                        border.color: "#333"
                    }
                    decrementControl: Rectangle {
                        id: scrollLower
                        width: 15
                        height: 15
                        color: styleData.pressed ? "#212121" : "#343434"
                        border.width: 1
                        border.color: "#333"
                        radius: 3

                        Image {
                            id: arrow
                            source: "file:///" + _buttleData.buttlePath
                                    + "/gui/img/buttons/params/arrow2.png"
                            x: 4
                            y: 4
                        }
                    }
                    incrementControl: Rectangle {
                        id: scrollHigher
                        width: 15
                        height: 15
                        color: styleData.pressed ? "#212121" : "#343434"
                        border.width: 1
                        border.color: "#333"
                        radius: 3

                        Image {
                            id: arrow
                            source: "file:///" + _buttleData.buttlePath
                                    + "/gui/img/buttons/params/arrow.png"
                            x: 4
                            y: 4
                        }
                    }
                }

                // frame: false
                // frameWidth: 0
                ListView {
                    id: tuttleParam
                    height: count ? contentHeight : 0
                    y: parent.y + 10
                    spacing: 6

                    interactive: false

                    model: params

                    delegate: Component {

                        RowLayout {

                            Text {
                                id: paramTitle
                                text: model.object.paramText
                                color: "white"
                                Layout.preferredWidth: columnHeader1.width
                                // If param has been modified, title in bold font
                                font.bold: model.object.hasChanged ? true : false

                                ToolTip {
                                    id: tooltip
                                    visible: false
                                    paramHelp: model.object.doc
                                    z: param.z + 1
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    acceptedButtons: Qt.RightButton

                                    onClicked: {
                                        // Reinitialise the value of the param to her default value
                                        model.object.hasChanged = false
                                        model.object.value = model.object.getDefaultValue()
                                        model.object.pushValue(
                                                    model.object.value)
                                    }
                                }
                            }

                            Loader {
                                id: param
                                source: model.object.paramType + ".qml"
                                Layout.fillWidth: true

                                Rectangle {
                                    width: parent.width
                                    height: parent.height
                                    color: paramEditor.background
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    acceptedButtons: Qt.RightButton
                                    hoverEnabled: true

                                    onClicked: {
                                        model.object.hasChanged = false
                                        model.object.value = model.object.getDefaultValue()
                                        model.object.pushValue(
                                                    model.object.value)
                                    }
                                    onEntered: {
                                        tooltip.visible = true
                                    }
                                    onExited: {
                                        tooltip.visible = false
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
