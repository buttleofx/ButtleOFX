import QtQuick 1.1

Rectangle {
    id: graphEditor
    implicitWidth: 850
    implicitHeight: 350
    z: 0
    clip: true


    Graph {
        //y used to place the graph at the good place
        y: 9/100 * parent.height;
        width : parent.width;
        height: 91/100*parent.height
    }
    Tools {
        width : parent.width;
        height: 9/100*parent.height
    }
}
