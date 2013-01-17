import QtQuick 1.1

Rectangle {
    id: graphEditor
    width: 850
    height: 350
    z: 0
    clip: true

    Keys.onPressed: {
        if (event.key == Qt.Key_Delete) {
            console.log("destruction");
            _buttleData.getGraphWrapper().destructionNode(_cmdManager);
        }
        if (event.key == Qt.Key_U) {
                console.log("U");
                _cmdManager.undo();
            }
            if (event.key == Qt.Key_R) {
                console.log("R");
                _cmdManager.redo();
            }
    }

    Graph {
        y: 30
        width : parent.width
        height: parent.height
    }

    Tools {
        width : parent.width
        height: 30
    }
}
