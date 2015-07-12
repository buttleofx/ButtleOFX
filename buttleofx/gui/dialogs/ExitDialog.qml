import QtQuick 2.1
import QtQuick.Window 2.1
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Window {
    id: exitDialog
    width: 470
    height: 120
    title: "Save Changes?"
    color: "#272727"
    flags: Qt.Dialog
    modality: "ApplicationModal"

    property string dialogText: "Do you want to save before exiting?<br>If you don't, all unsaved changes will be lost."

    signal saveButtonClicked
    signal discardButtonClicked

    Component {
        id: buttonStyle

        ButtonStyle {
            background: Rectangle {
                id: buttonRectangle
                radius: 6
                implicitWidth: 100
                implicitHeight: 25

                border.color: "#9F9C99";
                border.width: 1;
                opacity: 0.7

                gradient: Gradient {
                    GradientStop { position: 0; color: control.pressed ? "#EFEBE7" : "#EFEBE7" }
                    GradientStop { position: .5; color: control.pressed ? "#D9D9D9" : "#EFEBE7" }
                    GradientStop { position: 0; color: control.pressed ? "#EFEBE7" : "#EFEBE7" }
                }

                states:
                    State {
                        name: "mouse-over";
                        when: control.hovered
                        PropertyChanges {
                            target: buttonRectangle;
                            border.color: "#00B2A1";
                            opacity: 1}
                    }
                transitions: Transition {
                    NumberAnimation {
                        properties: "opacity, border.width";
                        easing.type: Easing.InOutQuad;
                        duration: 200
                    }
                }
            }
        }
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 15

        RowLayout {
            spacing: 20

            Image { source: "../img/icons/cropped-buttle.png" }

            Text {
                text: dialogText
                color: "#FEFEFE"
            }
        }

        RowLayout {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 6

            Button {
                id: saveButton
                text: "Save"
                style: buttonStyle
                isDefault: true

                onClicked: {
                    exitDialog.saveButtonClicked()
                    exitDialog.visible = false
                }
            }

            Button {
                id: discardButton
                text: "Discard"
                style: buttonStyle

                onClicked: {
                    exitDialog.discardButtonClicked()
                    exitDialog.visible = false
                }
            }

            Button {
                id: abortButton
                text: "Abort"
                style: buttonStyle
                onClicked: exitDialog.visible = false
            }
        }
    }
}
