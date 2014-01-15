import QtQuick 2.1
import ButtleFileModel 1.0

Rectangle {
    id: headerBar
    color : "#141414"

    property string folder
    signal changeFolder(string folder)
    property string parentFolder


	Row{
		spacing: 10;

		Image{
			id: previous;
            source: "../../img/buttons/browser/previous.png"
			sourceSize.width : parent.width
			sourceSize.height : 40

			MouseArea{
				anchors.fill: parent
                onClicked: {
                    console.debug("Undo")
                }
			}
		}
		Image{
			id: next
            source: "../../img/buttons/browser/next.png"
			sourceSize.width: parent.width
			sourceSize.height: 40

            MouseArea {
				anchors.fill: parent
                onClicked: console.log("Redo")
			}
		}
        Image {
			id: folder
            source: "../../img/buttons/browser/Folder-icon.png"
			sourceSize.width: parent.width
			sourceSize.height: 40

			MouseArea{
				anchors.fill: parent
                onClicked: {
                    changeFolder(parentFolder)
                }
			}
		}

        Rectangle{
            height: parent.height - 5
            width: 600
            y: 2
            color: "black"
            border.color: "grey"
            radius: 5

            TextInput {
                id : texteditPath
                y: 10
                x: 5
                height: parent.height
                width: parent.width

                text: headerBar.folder
                color: suggestion.exists ? "white" : "red"
                selectByMouse: true
                selectionColor: "blue"
                onAccepted: {
                    changeFolder(text)
                    texteditPath.focus = false
                }
                onFocusChanged:{
                    console.debug("Focus changed")
                    texteditPath.focus ? selectAll() : deselect()
                }
                onTextChanged: {
                    suggestion.folder = text

                }
            }
        }

        //console.debug("Suggestion: " + model.object.dirName)

        Column {
            Repeater {
                id: list

                model: suggestion.suggestionItems
                Text {
                    text: model.object.dirName
                    color: "blue"

                    onTextChanged: console.debug("suggestion: " + model.object.dirName)
                }
            }

        }

        FileModelBrowser {
            id: suggestion

            folder: headerBar.folder
            /*onFolderChanged: {
                console.debug("Folder of suggestion :" + suggestion.folder)
            }*/
        }
		
	}

}
