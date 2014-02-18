import QtQuick 2.1

Rectangle {
	id: button;
	
	width: 150; height : 35;
	radius: 2;

	property color buttonColor: "lightblue";
	property color onHoverColor: "blue";
	property color borderColor: "white";

	property string text: "Button";

	signal buttonClick();

	onButtonClick: {
        console.log(buttonLabel.text + " clicked");
	}

	border {
		color : button.borderColor;
	}
	
	Text {
		id: buttonLabel;
		anchors.centerIn: parent;
		text: button.text;
	}

	MouseArea {
		id: buttonMouseArea

		// Anchor all sides of the mouse area to the rectangle's anchors
		anchors.fill: parent
	
		onClicked: buttonClick();
		hoverEnabled: true;
		onEntered: parent.color = onHoverColor;
		onExited: parent.color = buttonColor;
	}

	color: buttonMouseArea.pressed ? Qt.darker(buttonColor, 1.5): buttonColor;
}
