import QtQuick 2.1
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0

Rectangle {
	id: footer
	color: "yellow"

	property string fileName: "Default file"
    property string fileType: "File"
    property string filter: "*"
    signal changeFilter(string filter)
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
            model: [ "*", ".jpg", ".png" ]

            onCurrentIndexChanged: {
                footer.changeFilter(currentText)
                console.log("nameFilter = " + currentIndex)
            }
        }

		Button{
			id: openButton
			text: "Open"
			Layout.fillHeight: true

            onClicked: {
                console.debug("It's a " + fileType)
                footer.fileType == "Folder" ? footer.openFolder(fileName) : Qt.openUrlExternally(fileName)
                console.debug("Open " + fileName)
            }
		}
		Button{
			id: cancelButton
			text: "Cancel"
			Layout.fillHeight: true

            onClicked: Qt.quit()
        }
	}
}

