import Qt 4.7

ListView {
    id: pythonList
    width: 200
    height: 240
    model: _paramListModel.paramElmts

    delegate: Component {
        Rectangle {
            width: parent.width
            height: 40
            color: ((index % 2 === 0)?"#222":"#111")
            
            Text {
                text: model.object.defaultValue
                anchors {
                    left: parent.left; leftMargin: 10
                    verticalCenter: parent.verticalCenter
                }
                color: "white"
                font.bold: true
                elide: Text.ElideRight
            }
       }
    }
}

