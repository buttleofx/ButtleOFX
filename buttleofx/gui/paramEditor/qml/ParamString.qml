import QtQuick 1.1
import FolderListViewItem 1.0

/*ParamString is an input field*/

Item {
    id: containerParamString
    implicitWidth: 300
    implicitHeight: 30

    property variant paramObject: model.object

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
            TextInput{
                id: paramStringInput
                text: paramObject.value
                anchors.left: parent.left
                anchors.leftMargin: 5
                maximumLength: 100
                width: parent.width - 10
                height: parent.height
                color: activeFocus ? "white" : "grey"
                onAccepted: paramObject.value = paramStringInput.text
                focus: true
            }
            states: [
                State {
                    name: "singleLine"
                    when: paramObject.stringType == "OfxParamStringIsSingleLine"
                    PropertyChanges {
                        target: stringInput
                        width: 50
                    }
                },
                State {
                    name: "multiLine"
                    when: paramObject.stringType == "OfxParamStringIsMultiLine"
                    PropertyChanges {
                        target: stringInput
                        height: 60
                        width: 200
                    }
                },
                State {
                    name: "filePath"
                    when: paramObject.stringType == "OfxParamStringIsFilePath"
                    PropertyChanges {
                        target: stringInput
                        width: 200
                    }
                },
                State {
                    name: "directoryPath"
                    when: paramObject.stringType == "OfxParamStringIsDirectoryPath"
                    PropertyChanges {
                        target: stringInput
                        width: 200
                    }
                    PropertyChanges {
                        target: folderforDirectory
                        width: 50
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
        FolderListView {id: finder}
        // hidden by default
        Image {
            id: folderforFileOrDirectory
            source: "img/folder.png"
            height: containerParamString.height - 8
            width: (paramObject.stringType == "OfxParamStringIsFilePath" || paramObject.stringType == "OfxParamStringIsDirectoryPath") ? 25 : 0

            MouseArea {
                id: buttonmousearea
                anchors.fill: parent   
                onPressed: {
                    finder.browseFile(_buttleData.currentParamNodeWrapper);
                    paramObject.value = finder.propFile
                }
            }
        }
    }
}
