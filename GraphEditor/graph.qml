import Qt 4.7

Rectangle {
    id: graph
    width: 850
    height: 350
    color: "#212121"

    Tools {}

    Item {
        Repeater {
            model : nodeListModel
            Node {}

        }
    }
}
