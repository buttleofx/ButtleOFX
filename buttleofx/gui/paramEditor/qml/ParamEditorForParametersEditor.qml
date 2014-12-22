import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQuick.Controls.Styles 1.0

// Parent of the ParamEditor is the Row of the ButtleApp
Item {
    id: paramEditor

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
    height: tuttleParamContent.height

    // Tuttle params
    Rectangle {
        id: tuttleParams
        Layout.minimumHeight: tuttleParamTitle.height
        width: parent.width
        color: paramEditor.background

        // Title of the node
        Button {
            id: tuttleParamTitle
            height: 40

            style: ButtonStyle {
                background: Rectangle {
                    implicitWidth: paramEditor.width
                    implicitHeight: 40
                    color: paramEditor.background

                    gradient: Gradient {
                        GradientStop { position: 0.0; color: gradian2 }
                        GradientStop { position: 0.85; color: gradian2 }
                        GradientStop { position: 0.86; color: gradian1 }
                        GradientStop { position: 1; color: gradian2 }
                    }
                }

                label: Text {
                    color: textColor
                    text: currentParamNode.name
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    font.pointSize: 11
                    clip: true
                }
            }

            onClicked: {
                if (tuttleParamContent.visible == true) {
                    tuttleParamContent.visible = false
                    tuttleParamContent.height = 0
                } else {
                    // tuttleParamContent.height = newHeight
                    tuttleParamContent.height = tuttleParam.contentHeight + 20
                    tuttleParamContent.visible = true
                }
            }
        }

        // Params depend on the node type (Tuttle data)
        Rectangle {
            id: tuttleParamContent

            y: tuttleParamTitle.height
            height: tuttleParam.contentHeight + 20
            width: parent.width

            visible: true

            color: "transparent"

            property string lastGroupParam: "No Group."


            ListView {
                id: tuttleParam
                y: 10
                anchors.topMargin: 10
                anchors.bottomMargin: 10
                width: parent.width
                height: count ? contentHeight : 0
                spacing: 6

                interactive: false

                model: params

                delegate: Component {
                    Loader {
                        id: param
                        source: model.object.paramType + ".qml"
                        width: parent.width
                        x: 15 // Here is the distance to the left of the listview
                    }
                }
            }
        }
    }
}
