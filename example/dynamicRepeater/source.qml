import QtQuick 2.0
 
Rectangle {
    width: 400
    height: 200

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        onClicked: {
            if( mouse.button == Qt.LeftButton )
            {
                _mainWrapper.add()
            }
        }
    }
    Repeater {
        id: pythonList
     
        model: _mainWrapper.clips  // Use the QObjectListModel defined in Python as our ListView model
     
        delegate: Component {
            Rectangle {
                width: 400
                height: 10 + 30 * Math.random()
                x: 100 * Math.random()
                y: 150 * Math.random()

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
                    acceptedButtons: Qt.LeftButton | Qt.RightButton
                    onClicked: {
                        if( mouse.button == Qt.LeftButton )
                        {
                            _mainWrapper.insertAt(index)
                        }
                        else
                        {
                            console.log("remove at " + index)
                            _mainWrapper.remove(index)
                        }
                    }
                }
            }
        }
        onItemRemoved: {
            console.log("QML : onItemRemoved " + item)
        }
    }
}
