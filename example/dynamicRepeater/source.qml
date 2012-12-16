import QtQuick 1.1
 
Column {
    Repeater {
        id: pythonList
        width: 400
        height: 200
     
        model: _mainWrapper.clips  // Use the QObjectListModel defined in Python as our ListView model
     
        delegate: Component {
            Rectangle {
                width: pythonList.width; height: 40
                color: ((index % 2 == 0)?"#222":"#111")
                
                Text {
                    text: model.object.name  // Get the clip name property through the "object" role
                    anchors {
                        left: parent.left;  leftMargin: 10
                        verticalCenter: parent.verticalCenter
                    }
                    color: "white"
                    font.bold: true
                    elide: Text.ElideRight
                }

                Text {
                    text: model.object.duration  // Same here for the duration property
                    anchors {
                        right: parent.right; rightMargin: 10
                        verticalCenter: parent.verticalCenter
                    }
                    color: "white"
                    elide: Text.ElideRight
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: { _mainWrapper.clicked(index) }
                }
            }
        }
        onItemRemoved:{
            console.log("QML : onItemRemoved")
        }
    }
}