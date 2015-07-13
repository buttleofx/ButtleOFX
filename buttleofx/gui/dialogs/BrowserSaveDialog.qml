import QtQuick 2.2
import QtQuick.Layouts 1.1
import QtQml 2.1
import QtQuick 2.0
import QtQuick.Window 2.1
import QtQuick.Dialogs 1.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0


import "../browser_v2/qml/"

// BrowserSave dialog: used to save a comp.
// the connecitons are done MainWindow.qml (i.e the Component which use this dialog)

BrowserDialog{
    id: root
    title: 'Save the Graph'
    signal saveButtonClicked(string absoluteFilePath)
    property variant idBrowserOpenDialog: undefined
    property string action

    function show(doAction) {
        root.action = doAction
        root.visible = true
    }


    onSaveButtonClicked: {
        if (absoluteFilePath != "") {
            _buttleData.urlOfFileToSave = absoluteFilePath
            _buttleData.saveData(_buttleData.urlOfFileToSave)

            root.visible = false

            if (root.action == "open" && idBrowserOpenDialog)
                idBrowserOpenDialog.visible = true
            else if (root.action == "new")
                _buttleData.newData()
            else if (root.action == "close")
                Qt.quit()
        }
    }

    RowLayout {
        id: bottomRow
        Layout.fillWidth: true
        Layout.fillHeight: true
        anchors.bottom: parent.bottom
        width: root.width - 8
        spacing: 0

        TextField {
            id: entryBar
            Layout.fillWidth: true
            style:
                TextFieldStyle {
                    selectionColor: "#00b2a1"
                    textColor: "#2E2E2E"
                    background: Rectangle {
                        id: entryStyle
                        color: "#DDDDDD"
                        border.color: "#00b2a1"
                        radius: 3
                        border.width: 1
                        states: [
                            State {
                                name: "out"
                                when: !entryBar.focus
                                PropertyChanges {
                                    target: entryStyle
                                    border.width: 0
                                }
                            }
                        ]
                    }
                }
        }

        Button{
            text: "Save"
            onClicked: saveButtonClicked(entryBar.text)

            style: ButtonStyle {
                background: Rectangle {
                    id: buttonRectangle
                    radius: 3
                    implicitWidth: 100
                    implicitHeight: 25

                    border.color: "#9F9C99";
                    border.width: 1;

                    gradient: Gradient {
                        GradientStop { position: 0; color: control.pressed ? "#EFEBE7" : "#EFEBE7" }
                        GradientStop { position: .5; color: control.pressed ? "#D9D9D9" : "#EFEBE7" }
                        GradientStop { position: 0; color: control.pressed ? "#EFEBE7" : "#EFEBE7" }
                    }
                }
            }
        }
    }

    Connections{
        target: root.browser.fileWindow
        onItemClicked: {
            entryBar.text = absolutePath + (isFolder ? '/buttleSave_now.bofx' : '')
        }
    }
    Component.onCompleted: entryBar.text = root.browser.bModel.currentPath + 'buttleSave_now.bofx'
}
