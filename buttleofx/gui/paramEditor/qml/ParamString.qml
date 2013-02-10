import QtQuick 1.1
import FolderListViewItem 1.0

/*ParamString is an input field*/

Item {
    id: containerParamString
    implicitWidth: 300
    implicitHeight: 30

    property variant paramObject: model.object

    FolderListView {id: finder}

    /*Container of the textInput*/

    Row{
        id: paramStringInputContainer
        spacing: 10

        /*Title of the paramString */
        Text {
            id: paramStringTitle
            text: paramObject.text + " : "
            color: "white"
        }

        /*Input field limited to 50 characters*/
        Rectangle{
            id: stringInput
            height: 20
            color: "#212121"
            border.width: 1
            border.color: "#333"
            radius: 3
            // this text input is hidden if we need multiline
            TextInput{
                id: paramStringInput
                text: paramObject.value
                anchors.left: parent.left
                anchors.leftMargin: 5
                anchors.rightMargin: 5
                //maximumLength: 100
                width: (paramObject.stringType != "OfxParamStringIsMultiLine") ? parent.width - 10 : 0
                height: parent.height
                color: activeFocus ? "white" : "grey"
                onAccepted: paramObject.value = paramStringInput.text
                focus: true
            }

            // this text input is visible if we need multiline
            Flickable {
                id: flick
                width: (paramObject.stringType == "OfxParamStringIsMultiLine") ? parent.width - 10 : 0 
                height: parent.height
                contentWidth: paramStringMultilines.paintedWidth
                contentHeight: paramStringMultilines.paintedHeight
                clip: true

                function ensureVisible(r)
                {
                    if (contentX >= r.x)
                        contentX = r.x;
                    else if (contentX+width <= r.x+r.width)
                        contentX = r.x+r.width-width;
                    if (contentY >= r.y)
                        contentY = r.y;
                    else if (contentY+height <= r.y+r.height)
                        contentY = r.y+r.height-height;
                }

                TextEdit {
                    id: paramStringMultilines
                    width: flick.width
                    height: flick.height
                    color: activeFocus ? "white" : "grey"
                    font.pointSize: 10
                    //wrapMode: TextEdit.Wrap
                    onCursorRectangleChanged: flick.ensureVisible(cursorRectangle)
                    onTextChanged: paramObject.value = paramStringMultilines.text
                    focus: true
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
        }
        // hidden by default
        Image {
            id: folderforFileOrDirectory
            source: "img/folder.png"
            width: (paramObject.stringType == "OfxParamStringIsFilePath" || paramObject.stringType == "OfxParamStringIsDirectoryPath") ? 20 : 0
            y: 2

            MouseArea {
                id: buttonmousearea
                anchors.fill: parent   
                onPressed: {
                    finder.browseFile(_buttleData.currentParamNodeWrapper)
                    if( finder.propFile )
                    {
                        paramObject.value = finder.propFile
                    }
                }
            }
        }
    }
}
