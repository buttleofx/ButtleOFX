import QtQuick 2.1
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0

Rectangle {
	id: footer
    color: "#141414"

	property string fileName: "Default file"
    property string fileType: "File"
    property string filter: "*"
    property variant selected

    signal changeFilter(string newFilter)
    signal openFolder(string newFolder)

	RowLayout {
		anchors.fill: parent
		spacing: 6

        Item {
			Layout.fillHeight: true
			Layout.fillWidth: true
        }

       ComboBox {
            width: 200
            model: [ "*", ".jpg", ".png", ".raw" ]


            onCurrentTextChanged: {
                changeFilter(currentText)
                console.log("currentText = " + currentText)
            }
        }

		Button{
			id: openButton
			text: "Open"
            height: parent.height

            onClicked: {
                for(var i=0; i< selected.count; ++i)
                {
                    console.debug("selected: " + i + " -> " + selected.get(i).fileName)
                    footer.fileType == "Folder" ? footer.openFolder(fileName) : Qt.openUrlExternally("file:///" + selected.get(i).filepath)
                    console.debug("Open " + fileName)
                }
            }
		}
	}
}

