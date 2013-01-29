import QtQuick 1.1

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

        /*Title of the paramInt */
        Text {
            id: paramStringTitle
            text: paramObject.text + " : "
            color: "white"
        }

        /*Input field limited to 50 characters*/
        Rectangle{
            id: stringInput
            height: 20
            implicitWidth: 200 
            width: paramStringInput.width
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
                selectByMouse : true
                color: activeFocus ? "white" : "grey"
                onAccepted: paramObject.value = paramStringInput.text
                
            }
            states: [
                    State {
                        name: "singleLine"
                        when: paramObject.stringType != "OfxParamStringIsMultiLine"
                        PropertyChanges {
                            target: stringInput
                            height: 20
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
                    }
                ]
        }
        //if(paramObject.stringType == "OfxParamStringIsFilePath" || paramObject.stringType == "OfxParamStringIsDirectoryPath") {
            Rectangle {
                id: fileButton
                height:20
                width: 20
                color: "grey"
                radius: 3
                Image {
                    id: folder
                    source: "img/folder.png"
                    anchors.centerIn: parent
                    height: parent.height - 1
                    width: parent.width - 2
                }
                states: [
                    State {
                        name: "shown"
                        when: paramObject.stringType == "OfxParamStringIsFilePath" || paramObject.stringType == "OfxParamStringIsDirectoryPath"
                        PropertyChanges {
                            target: fileButton
                            opacity: 1
                        }
                    },
                    State {
                        name: "hidden"
                        when: paramObject.stringType != "OfxParamStringIsFilePath" && paramObject.stringType != "OfxParamStringIsDirectoryPath"
                        PropertyChanges {
                            target: fileButton
                            opacity: 0
                        }
                    }
                ]

            }
        //}
    }
}
