import QtQuick 2.0
import QtQuick.Window 2.1
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.0


Window {
    id: root
    width: 400
    height: 600
    color: "#353535"
    title: "Buttle OFX Action Manager"

    Component {
        id: action

        Rectangle {
            width: parent.width
            height: 60
            color: "transparent"

            ColumnLayout {
                anchors.fill: parent
                spacing: 0

                RowLayout {
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: parent.height / 2

                    Rectangle {
                        Layout.preferredWidth: parent.width * 0.9
                        Layout.preferredHeight: parent.height
                        color: "#FF0000"

                        Text {
                            id: task_name
                            text: qsTr("Action titre")
                        }
                    }

                    Button {
                        id: abort

                        Layout.preferredWidth: parent.width * 0.1
                        Layout.preferredHeight: parent.height
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                        tooltip: "Parent folder"

                        iconSource:"img/refresh_hover.png"

                        style:
                        ButtonStyle {
                            background: Rectangle {
                                anchors.fill: parent
                                color: "transparent"
                            }
                        }

    //                    onClicked: {

    //                    }
                    }
                }

                RowLayout {
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: parent.height / 2

                    ProgressBar {
                        Layout.preferredWidth: parent.width
                        value: 0.5
                    }
                }

            }
        }
    }


    ScrollView {
        anchors.fill: parent

        style: ScrollViewStyle {
            scrollBarBackground: Rectangle {
                id: scrollBar
                width: styleData.hovered ? 8 : 4
                color: "transparent"

                Behavior on width { PropertyAnimation { easing.type: Easing.InOutQuad ; duration: 200 } }
            }

            handle: Item {
                implicitWidth: 15
                Rectangle {
                    color: "#00b2a1"
                    anchors.fill: parent
                }
            }

            decrementControl : Rectangle {
                visible: false
            }

            incrementControl : Rectangle {
                visible: false
            }
        }

//        Item {
//            id: action



//        }

//        ListView {
//            anchors.fill: parent
//        }
    }

    onClosing:{
        action_button.isOpen = false
    }
}
