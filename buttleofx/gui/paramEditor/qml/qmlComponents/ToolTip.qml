import QtQuick 2.0

Item{	
	id:tooltip
	anchors.fill: parent
	property string paramHelp
	
	Rectangle{
		id:rectangle
		color: "#212121"
		border.width: 1
		border.color: "#333"
		radius: 3
		width:text.contentWidth
		height:text.contentHeight
		x:30
        y:30
	}

	Text{
		id: text
		color: "white"
		text:  paramHelp
		width: 250
		wrapMode:Text.Wrap
		x:rectangle.x
        y:rectangle.y
	}
}
