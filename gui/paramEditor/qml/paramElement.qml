import Qt 4.7

ListView {
    id: pythonList
    width: 400
    height: 200
 
    model: _paramListModel
 
    delegate: Component {
        Rectangle {
            width: _paramListModel.width; height: 40
            color: ((index % 2 === 0)?"#222":"#111")
            
            Text {
                text: model.object.text // We just want to test on the ParamInt's text for the moment. This syntax is bad so doesn't worth.
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
