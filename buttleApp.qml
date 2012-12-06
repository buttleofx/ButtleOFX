import QtQuick 1.1
import "gui/graph/qml"
import "gui/viewer"
import "gui/paramEditor/qml"

Rectangle {
    id: buttleWindow
    width: 1280
    height: 800
    color: "#252525"

    Column {
		spacing: 10
	    Text {
	    	color: "#fff"
	    	text: "Menu of ButtleOFX"
	    }
	    Column {
	    	x: 10; y: 10
	        spacing: 10
	    	Player{}
	    	GraphEditor{}
	    }
	}
}
