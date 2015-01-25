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
        name: !_buttleData.currentParamNodeWrapper ? "Parameters" : "Parameters:    "
                                                     + _buttleData.currentParamNodeWrapper.nameUser
        onCloseClicked: paramEditor.buttonCloseClicked(true)
        onFullscreenClicked: paramEditor.buttonFullscreenClicked(true)
    }

    Component {
        id: paramComponent

        Rectangle {
            // TODO: we loose the access to the "model" variable if we use a Loader.
            // So we use an item with "visible" and "height: 0".
            property variant modelObject: model.object

            x: 5
            width: parent.width
            height: modelObject.isSecret ? 0 : param.height
            visible: !modelObject.isSecret

            color: paramEditor.background

            Text {
                id: paramTitle
                text: modelObject.paramText
                width: columnHeader1.width
                height: parent.height
                // If param has been modified, title in bold font
                font.bold: Boolean(modelObject.hasChanged)

                color: paramEditor.textColor
                verticalAlignment: Text.AlignVCenter

                ToolTip {
                    id: tooltip
                    visible: false
                    paramHelp: modelObject.doc
                    z: 3
                }

                // TODO : For the moment we catch an error: "pyqtSignal must be bound to QObject not StringWrapper"
                // although Stringwrapper inherite from QObject
                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.RightButton

                    onClicked: {
                        // Reinitialise the value of the param to her default value
                        modelObject.hasChanged = false
                        modelObject.value = modelObject.getDefaultValue()
                        modelObject.pushValue(modelObject.value)
                    }
                }
            }
            Rectangle {
                x: paramTitle.width
                width: columnHeader2.width
                height: childrenRect.height
                color: paramEditor.background

                Loader {
                    id: param
                    x: 5
                    source: modelObject.paramType + ".qml"
                    width: parent.width


                    MouseArea {
                        anchors.fill: parent
                        acceptedButtons: Qt.RightButton
                        hoverEnabled: true

                        onClicked: {
                            modelObject.hasChanged = false
                            modelObject.value = modelObject.getDefaultValue()
                            modelObject.pushValue(modelObject.value)
                        }
                        onEntered: tooltip.visible = true
                        onExited: tooltip.visible = false
                    }
                }
            }
        }
    }

    // Tuttle params
    Rectangle {
        id: tuttleParams
        y: tabBar.height
        height: parent.height
        width: parent.width

        color: paramEditor.background

        // Params depend on the node type (Tuttle data)
        Rectangle {
            id: tuttleParamContent
            y: 5
            height: parent.height
            width: parent.width

            color: paramEditor.background

            Item {
                id: header
                z: 1
                width: parent.width

                Item {
                    id: columnHeader1
                    width: resizeBar.x
                }

                Rectangle {
                    id: resizeBar
                    x: 110
                    width: 50
                    height: 20
                    color: paramEditor.background

                    Rectangle {
                        id: dragLeft
                        width: 2
                        height: 15
                        color: paramEditor.backgroundInput
                        radius: 1
                    }

                    Rectangle {
                        id: dragRight
                        width: 2
                        height: 15
                        color: paramEditor.backgroundInput
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
                        cursorShape: Qt.SplitHCursor
                    }

                    // Allow to resize the columns
                    Rectangle {
                        y: tabBar.height + 2
                        width: 1
                        height: paramEditor.height - 5
                        anchors.left: dragLeft.right

                        color: paramEditor.backgroundInput

                        MouseArea {
                            height: parent.height
                            //larger zone for easier drag
                            width: parent.width + 5
                            drag.target: resizeBar
                            drag.axis: Drag.XAxis
                            drag.minimumX: 0
                            drag.maximumX: tuttleParams.width
                            cursorShape: Qt.SplitHCursor
                        }
                    }
                }

                Rectangle {
                    id: columnHeader2
                    width: header.width - columnHeader1.width
                    anchors.left: resizeBar.right
                    color: paramEditor.background
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
                            x: 4
                            y: 4
                            source: "file:///" + _buttleData.buttlePath
                                    + "/gui/img/buttons/params/arrow.png"
                        }
                    }
                }

                ListView {
                    id: tuttleParam
                    y: 10
                    width: parent.width
                    height: count ? contentHeight : 0
                    spacing: 6
                    interactive: false
                    model: params

                    delegate: paramComponent
                }
            }
        }
    }
}
