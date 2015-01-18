import QtQuick 2.0
import QtQuick.Dialogs 1.0
import FolderListViewItem 1.0

// ParamString is an input field
Item {
    id: containerParamString
    implicitWidth: 300
    implicitHeight: 30
    y: paramObject.stringType == "OfxParamStringIsMultiLine" ? -10 : 10

    property variant paramObject: model.object
    property bool existPath: paramObject.filePathExist

    // Is this param secret?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

    /*
    FolderListView {
        id: finder
        property bool existPath: _buttleData.currentParamNodeWrapper.pluginContext=="OfxImageEffectContextReader":false
        typeDialog: existPath ? "OpenFile" : "SaveFile"
        messageDialog: existPath ? "Open file" : "Save file as"
    }
    */

    Row {
        id: paramStringInputContainer
        spacing: 10

        // Input field limited to 50 characters
        Rectangle {
            id: stringInput
            height: 20
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            clip: true

            // Container of the textInput
            Loader {
                sourceComponent: paramObject.stringType == "OfxParamStringIsMultiLine" ?
                    paramObject.stringType == "OfxParamStringIsLabel" ? paramStringLabel : paramStringMultiline : paramStringNotMultiline
                anchors.fill: parent

                Component {
                    id: paramStringMultiline

                    // We need a multi line input
                    Flickable {
                        id: flick
                        width: parent.width - 10
                        height: parent.height
                        contentWidth: paramStringMultilines.paintedWidth
                        contentHeight: paramStringMultilines.paintedHeight
                        clip: true

                        function ensureVisible(r) {
                            if (contentX >= r.x)
                                contentX = r.x
                            else if (contentX+width <= r.x+r.width)
                                contentX = r.x+r.width-width

                            if (contentY >= r.y)
                                contentY = r.y
                            else if (contentY+height <= r.y+r.height)
                                contentY = r.y+r.height-height
                        }

                        TextEdit {
                            id: paramStringMultilines
                            text: paramObject.value
                            width: flick.width
                            height: flick.height
                            color: activeFocus ? "white" : "grey"
                            font.pointSize: 10
                            onCursorRectangleChanged: flick.ensureVisible(cursorRectangle)

                            Keys.onEnterPressed: {
                                paramObject.changeValue(paramStringMultilines.text)
                            }

                            focus: true
                        }
                    }
                }

                Component {
                    id: paramStringNotMultiline

                    TextInput{
                        id: paramStringInput
                        text: paramObject.value
                        anchors.left: parent.left
                        anchors.leftMargin: 5
                        anchors.rightMargin: 5
                        width: parent.width - 10
                        height: parent.height
                        color: activeFocus ? "white" : "grey"
                        selectByMouse: true

                        onAccepted: {
                            // Calling paramObject twice here in qml doesn't work, so we add a function which does both of them in python
                            // paramObject.value = paramStringInput.text
                            // paramObject.pushValue(paramObject.value)
                            paramObject.changeValue(paramStringInput.text)
                        }

                        focus: true
                    }
                }

                Component{
                    id: paramStringLabel

                    Text {
                        id: paramStringLabelText
                        text: paramObject.value
                        anchors.left: parent.left
                        anchors.leftMargin: 5
                        anchors.rightMargin: 5
                        width: parent.width - 10
                        height: parent.height
                    }
                }
            }

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton

                onClicked: {
                    paramObject.resetValue()
                }
            }

            // State which enables us to update display, depending on what type of String we have on TuttleOFX
            states: [
                State {
                    name: "singleLine"
                    when: paramObject.stringType == "OfxParamStringIsSingleLine"

                    PropertyChanges {
                        target: stringInput
                        width: 200
                    }
                },
                State {
                    name: "multiLine"
                    when: paramObject.stringType == "OfxParamStringIsMultiLine"

                    PropertyChanges {
                        target: stringInput
                        width: 280
                        height: 30
                    }
                },
                State {
                    name: "filePath"
                    when: paramObject.stringType == "OfxParamStringIsFilePath"

                    PropertyChanges {
                        target: stringInput
                        width: 180
                    }
                },
                State {
                    name: "directoryPath"
                    when: paramObject.stringType == "OfxParamStringIsDirectoryPath"

                    PropertyChanges {
                        target: stringInput
                        width: 180
                    }
                },
                State {
                    name: "label"
                    when: paramObject.stringType == "OfxParamStringIsLabel"
                    PropertyChanges {
                        target: stringInput
                        width: 200
                    }
                }
            ]
        }

        // Hidden by default
        Image {
            id: folderforFileOrDirectory
            source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/folder.png"
            width: (paramObject.stringType == "OfxParamStringIsFilePath" || paramObject.stringType == "OfxParamStringIsDirectoryPath") ? 20 : 0
            y: 2

            MouseArea{
                anchors.fill: parent

                onPressed: {
                    if (existPath){
                        finderLoadFile.open()
                    } else {
                        finderSaveFile.open()
                    }
                }

                // Open a file dialog to select a file
                /*
                FileDialog {
                    id: folderfiledialog
                    title: "Open"
                    folder: _buttleData.buttlePath
                    nameFilters: [ "All files (*)" ]
                    selectedNameFilter: "All files (*)"

                    onAccepted: {
                        if (folderfiledialog.fileUrl){
                            paramObject.value = folderfiledialog.fileUrl
                            paramObject.pushValue(paramObject.value)
                        }
                    }
                }
                */

                FileDialog {
                    id: finderLoadFile
                    title: "Open"
                    folder: _buttleData.buttlePath
                    nameFilters: [ "All files (*)" ]
                    selectedNameFilter: "All files (*)"

                    onAccepted: {
                        if (finderLoadFile.fileUrl) {
                            paramObject.value = finderLoadFile.fileUrl
                            paramObject.pushValue(paramObject.value)
                        }
                    }
                }

                FileDialog {
                    id: finderSaveFile
                    title: "Save"
                    folder: _buttleData.buttlePath
                    nameFilters:  [ "All files (*)" ]
                    selectedNameFilter: "All files (*)"

                    onAccepted: {
                        if (finderSaveFile.fileUrl) {
                            paramObject.value = finderSaveFile.fileUrl
                            paramObject.pushValue(paramObject.value)
                        }
                    }
                    selectExisting: false
                }
            }
        }
    }
}
