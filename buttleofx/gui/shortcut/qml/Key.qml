import QtQuick 2.0

Item{	
	id:keyRect
	property string key
	width: rect.width
	height: rect.height
	
	Rectangle{
		id:rect
        color: "#010101"
        border.width: 1
		border.color: "black"
		radius: 3
		width:text.contentWidth==0? 0:text.contentWidth+10
		height:text.contentHeight==0? 0:text.contentHeight+10
	}

	Text{
		id: text
        color: "#00b2a1"
		text: key
		width: 40
		wrapMode:Text.Wrap
		x:rect.x+5
        y:rect.y+5
	}
}
