import QtQuick 2.1

Rectangle {
    id: container

    property QtObject model
    property int selectedIndex: -1
    //property alias currentIndex
    //property alias currentItem
    signal itemSelected(string item)

    width: parent.width

    Column {
        id: popup

        Repeater {
            id: list

            model: container.model
            delegate: Item {
                id: delegateItem

                height: 30
                width: container.width

                Rectangle {
                    height: parent.height
                    width: parent.width - 7
                    border {
                        color: "black"
                        width: 1
                    }
                    radius: 3
                    color: "#141414FF"

                    Text {
                        id: textComponent
                        color: "lightblue"
                        text: model.object.fileName
                        y: 5
                        x: 10

                        MouseArea {
                            anchors.fill : parent
                            hoverEnabled: true
                            onClicked: {
                                container.itemSelected(model.object.filepath)
                            }
                        }
                    }
                }//end Rectangle
            }//end Item delegateItem
        }//end Repeater

    }//end Column popup
}//end Rectangle container

