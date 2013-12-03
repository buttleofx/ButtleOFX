import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

Rectangle {
	id: browser
	width: 1000
	height : 600

    QtObject {
        id: m
        property string directory: "/"
        property string filepath: ""
    }

	ColumnLayout {
	    anchors.fill: parent

	    HeaderBar {
		    //anchors.top: parent.top
		    id: headerBar
		    Layout.fillWidth: true
		    Layout.preferredHeight: 40

            folder: m.directory
            onChangeFolder: {
                m.directory = folder
            }
	    }

	    CheckBox {
	    	id: check
	    	text: "Viewer"
	    }

        SplitView {
	        Layout.fillWidth: true
	        Layout.fillHeight: true
            orientation: Qt.Horizontal

		    LeftCol {
                id: left
                Layout.minimumWidth: 50
                Layout.preferredWidth: 100
	            Layout.fillHeight: true
		    }

		    WindowFiles {
			    id: files
		        Layout.fillWidth: true
	            Layout.fillHeight: true
			    
                folder: m.directory

		    }

		    Viewer {
		    	id: viewer

		    	Layout.fillWidth: check.checked
                Layout.fillHeight: true

		    	Layout.preferredWidth: 1

                filepath: m.filepath
		    }
	    }

	    FooterBar {
		    id: footerBar
	        Layout.fillWidth: true
		    Layout.preferredHeight: 40

            fileName: m.filepath
	    }
    }
}

