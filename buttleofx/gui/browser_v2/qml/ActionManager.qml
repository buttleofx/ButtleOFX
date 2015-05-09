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
        id: action_ended

        Rectangle {
            width: root.width
            height: 40
            color: "transparent"
            opacity: 0.9

            RowLayout {
                anchors.fill: parent

                Rectangle {
                    Layout.preferredWidth: parent.width * 0.8
                    Layout.preferredHeight: parent.height

                    color: "transparent"

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 20
                        spacing: 10

                        Text {
                            id: task_name

                            verticalAlignment: Text.AlignVCenter
                            clip: true
                            font.pointSize: 11
                            color: "white"

                            text: qsTr(model.object.getName() + " of " + model.object.nbTotalActions + " element(s)")
                        }

                        Text {
                            visible: model.object.aborted

                            verticalAlignment: Text.AlignVCenter
                            clip: true
                            font.pointSize: 11
                            color: "red"

                            text: qsTr("aborted")
                        }
                    }
                }

                Button {
                    id: del

                    Layout.preferredWidth: parent.width * 0.2
                    Layout.preferredHeight: parent.height
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    tooltip: "Delete task from history"

                    iconSource:"img/del.png"

                    style:
                    ButtonStyle {
                        background: Rectangle {
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }

                    onClicked: {
                        _actionManager.removeEndedActionFromId(model.object)
                    }
                }
            }
        }
    }

    Component {
        id: action_running

        Rectangle {
            width: root.width
            height: 60
            color: "transparent"

            ColumnLayout {
                anchors.fill: parent
                spacing: 0

                RowLayout {
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: parent.height / 2

                    Rectangle {
                        Layout.preferredWidth: parent.width * 0.8
                        Layout.preferredHeight: parent.height
                        color: "transparent"


                        Text {
                            id: task_name
                            anchors.fill: parent
                            anchors.leftMargin: 20

                            verticalAlignment: Text.AlignVCenter
                            clip: true
                            font.pointSize: 12
                            color: "white"

                            text: qsTr(model.object.getName() + " of " + model.object.nbTotalActions + " file(s)")
                        }
                    }

                    Button {
                        id: abort

                        Layout.preferredWidth: parent.width * 0.2
                        Layout.preferredHeight: parent.height
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                        tooltip: "Abort and reverse task"

                        iconSource:"img/abort.png"

                        style:
                        ButtonStyle {
                            background: Rectangle {
                                anchors.fill: parent
                                color: "transparent"
                            }
                        }

                        onClicked: {
                            model.object.aborted = true
                        }
                    }
                }

                RowLayout {
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: parent.height / 2

                    ProgressBar {
                        Layout.preferredWidth: parent.width * 0.9
                        Layout.alignment: Qt.AlignHCenter
                        value: model.object.progress

                        style: ProgressBarStyle {
                            background: Rectangle {
                                radius: 2
                                color: "#222222"
                                border.color: "#222222"
                                border.width: 1
                                implicitWidth: parent.width
                                implicitHeight: 10
                            }
                            progress: Rectangle {
                                color: "#00b2a1"
                                border.color: "#00b2a1"
                            }
                        }
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

        ColumnLayout {
            width: parent.width

            spacing: 0

            ListView {
                id: actions_running
                Layout.fillWidth: true
                Layout.preferredHeight: count * 60
                verticalLayoutDirection: ListView.BottomToTop

                model: _actionManager.runningActions
                delegate: action_running
            }

            ListView {
                id: actions_ended
                Layout.fillWidth: true
                Layout.preferredHeight: count * 40
                verticalLayoutDirection: ListView.BottomToTop

                model: _actionManager.endedActions
                delegate: action_ended
            }
        }
    }

    onClosing:{
        action_button.isOpen = false
    }
}
