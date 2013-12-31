import QtQuick 2.1
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0

Rectangle {
	id: footer
	color: "yellow"

	property string fileName: "Default file"
    property string filter: "*"
    signal changeFilter(string newFilter)

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

            onCurrentTextChanged: {
                changeFilter(currentText)
                console.log("currentText = " + currentText)
            }
            onCurrentIndexChanged: {
                console.log("nameFilter = " + currentIndex)
            }
        }

		Button{
			id: openButton
			text: "Open"
			Layout.fillHeight: true

            onClicked: console.log("Open " + fileName)
		}
		Button{
			id: cancelButton
			text: "Cancel"
			Layout.fillHeight: true

            onClicked: Qt.quit()
        }
	}
}

