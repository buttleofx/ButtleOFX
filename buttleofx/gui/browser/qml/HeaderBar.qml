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
                    texteditPath.focus ? selectAll() : deselect()
                }
                onTextChanged: {
                    suggestion.folder = text
                }
            }
        }

        FileModelBrowser {
            id: suggestion

            folder: headerBar.folder
        }

        SuggestionBox {
            id: suggestionBox

            y: 40
            x: 150
            width: texteditPath.width
            visible: texteditPath.focus

            model: suggestion.getFilteredFileItems(suggestion.folder)
            onItemSelected: {
                texteditPath.text = item
            }

        }

	}

}
