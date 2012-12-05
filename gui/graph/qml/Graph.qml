import QtQuick 1.1

Rectangle {
    width: 850
    height: 350 - 30
    y: 30
    gradient: Gradient {
        GradientStop { position: 0.0; color: "#111111" }
        GradientStop { position: 0.015; color: "#212121" }
    }

    Keys.onPressed: {
        if (event.key==Qt.Key_Delete) {
            if (node.focus == true){
                deleteNode()
            }
        }
    }
}
