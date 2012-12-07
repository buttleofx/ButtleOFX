import Qt 4.7

Rectangle {
    id: paramEditor
    width: 300
    height: 700
    color: "#212121"

    ListView {
        id: paramElementList
        anchors.fill: parent
        model: _paramListModel.paramElmts

        delegate: Component {
                Loader {
                    id: param
                    source : model.object.paramType
                    height: 50
                }

        }

    }
}


        /*
        Rectangle {
            width: parent.width
            height: 40
            color: ((index % 2 === 0)?"#222":"#111")
            
            Loader {
                id: param
               source: ((index % 2 === 0)? "ParamInt.qml":"ParamString.qml")
            }*/
/*
            Text {
                text: model.object.defaultValue
                anchors {
                    left: parent.left; leftMargin: 10
                    verticalCenter: parent.verticalCenter
                }
                color: "white"
                font.bold: true
                elide: Text.ElideRight
            }*/
//}

