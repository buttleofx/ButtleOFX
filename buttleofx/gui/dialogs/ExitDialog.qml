import QtQuick 2.1
import QtQuick.Window 2.1
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Window {
    id: exitDialog
    width: 425
    height: 100
    title: "Save Changes?"
    color: "#141414"
    flags: Qt.Dialog
    modality: Qt.WindowModal
    visible: false

    Component {
        id: buttonStyle

        ButtonStyle {
            background: Rectangle {
                radius: 6
                implicitWidth: 100
                implicitHeight: 25

                border.color: control.hovered ? "#00B2A1" : "#9F9C99"
                border.width: control.hovered ? 3 : 2

                gradient: Gradient {
                    GradientStop { position: 0; color: control.pressed ? "#EFEBE7" : "#EFEBE7" }
                    GradientStop { position: .5; color: control.pressed ? "#D9D9D9" : "#EFEBE7" }
                    GradientStop { position: 0; color: control.pressed ? "#EFEBE7" : "#EFEBE7" }
                }
            }
        }
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 15

        RowLayout {
            spacing: 20

            Image {
                source: "/home/james/git/ButtleOFX/buttleofx/gui/img/icons/logo_icon.png"
            }

            Text {
                text: "Do you want to save before exiting?<br>If you don't, all unsaved changes will be lost"
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

                onClicked: {
                    if (urlOfFileToSave != "") {
                        _buttleData.saveData(urlOfFileToSave)
                    } else {
                        finderSaveGraph.open()
                        finderSaveGraph.close()
                        finderSaveGraph.open()
                    }
                }
            }

            Button {
                id: discardButton
                text: "Discard"
                style: buttonStyle
                onClicked: Qt.quit()
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
