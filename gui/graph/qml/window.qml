import Qt 4.7

Rectangle {
    id: graphWindow
    property int nodeSelected : 0
    signal addNode
    signal deleteNode (int index)
    width: 850
    height: 350


    Tools {}

    Graph {}

}
