import QtQuick 2.0
import FolderListViewItem 1.0
import QtQuick.Dialogs 1.0

/*ParamString is an input field*/

Item {
    id: containerParamString
    implicitWidth: 300
    implicitHeight: 30
    y:10

    property variant paramObject: model.object
    property bool isReader: currentParamNode ? currentParamNode.pluginContext=="OfxImageEffectContextReader": false

    // Is this param secret ?
    visible: !paramObject.isSecret
    height: paramObject.isSecret ? 0 : implicitHeight

  /*  FolderListView {
        id: finder
        property bool isReader: _buttleData.currentParamNodeWrapper.pluginContext=="OfxImageEffectContextReader":false
        typeDialog: isReader ? "OpenFile" : "SaveFile"
        messageDialog: isReader ? "Open file" : "Save file as"
    }
*/

    Row{
        id: paramStringInputContainer
        spacing: 10

        /*Title of the paramString */
        Text {
            id: paramStringTitle
            text: paramObject.text + " : "
            color: "white"
            elide: Text.ElideRight
            clip: true
            // if param has been modified, title in bold font
            font.bold: paramObject.hasChanged ? true : false
            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton
                onClicked: {
                    paramObject.value = paramObject.getDefaultValue()
                }
            }
        }

        /*Input field limited to 50 characters*/
        Rectangle{
            id: stringInput
            height: 20
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            clip: true

            /*Container of the textInput*/
            Loader {
                sourceComponent: containerParamString.paramObject.stringType == "OfxParamStringIsMultiLine" ? paramStringMultiline : paramStringNotMultiline
                anchors.fill : parent
                Component{
                    id : paramStringMultiline
                    // we need a multi line input
                    Flickable { 
                        id: flick
                        width: parent.width - 10
                        height: parent.height
                        contentWidth: paramStringMultilines.paintedWidth
                        contentHeight: paramStringMultilines.paintedHeight
                        clip: true

                        function ensureVisible(r) 
                        { 
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
                            text: containerParamString.paramObject.value
                            width: flick.width
                            height: flick.height
                            color: activeFocus ? "white" : "grey"
                            font.pointSize: 10
                            onCursorRectangleChanged: flick.ensureVisible(cursorRectangle)
                            onTextChanged: { 
                               containerParamString.paramObject.value = paramStringMultilines.text
                               containerParamString.paramObject.pushValue(containerParamString.paramObject.value)
                            } 
                            focus: true 
                        } 
                    }
                }
                Component{
                    id : paramStringNotMultiline
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
                           containerParamString.paramObject.value = paramStringInput.text 
                           containerParamString.paramObject.pushValue(containerParamString.paramObject.value)
                        } 
                        focus: true
                    }
                }
            }

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.RightButton
                onClicked: {
                    paramObject.value = paramObject.getDefaultValue()
                    paramObject.pushValue(paramObject.value)
                }
            }

            // state which enable us to update display, depend on what type of String we have on TuttleOFX
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
        }//Rectangle

        // hidden by default
        Image {
            id: folderforFileOrDirectory
            source: "file:///" + _buttleData.buttlePath + "/gui/img/buttons/params/folder.png"
            width: (paramObject.stringType == "OfxParamStringIsFilePath" || paramObject.stringType == "OfxParamStringIsDirectoryPath") ? 20 : 0
            y: 2

            MouseArea{
                anchors.fill: parent

                onPressed: {
                    if(isReader){finderLoadFile.open()}else{finderSaveFile.open()}
                }

                // open a file dialog to select a file
                /*FileDialog {

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
                }*/

                FileDialog {
                    id: finderLoadFile
                    title: "Open"
                    folder: _buttleData.buttlePath
                    nameFilters: [ "All files (*)" ]
                    selectedNameFilter: "All files (*)"
                    onAccepted: {
                        if (finderLoadFile.fileUrl){
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
                        if (finderSaveFile.fileUrl){
                            paramObject.value = finderSaveFile.fileUrl
                            paramObject.pushValue(paramObject.value)
                        }
                    }
                    selectExisting: false
                }
            }//MouseArea
        }//Image
    }//Row
}
