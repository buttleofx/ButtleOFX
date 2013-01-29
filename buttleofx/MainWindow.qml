import QtQuick 1.1
import QtDesktop 0.1
import "gui/graph/qml"
import "gui/viewer/qml"
import "gui/paramEditor/qml"

Rectangle {
    width: 1200
    height: 800

    Keys.onPressed: {
        if (event.key == Qt.Key_Delete) {
            _buttleData.destructionNode();
        }
        if ((event.key == Qt.Key_Z) && (event.modifiers & Qt.ControlModifier)) {
            _buttleData.undo();
        }
        if ((event.key == Qt.Key_Y) && (event.modifiers & Qt.ControlModifier)) {
            _buttleData.redo();
        }
        if ((event.key == Qt.Key_D) && (event.modifiers & Qt.ControlModifier)){
            _buttleData.duplicationNode()
        }
        if ((event.key == Qt.Key_C) && (event.modifiers & Qt.ControlModifier)){
            _buttleData.copyNode()
        }
        if ((event.key == Qt.Key_V) && (event.modifiers & Qt.ControlModifier)){
            _buttleData.pasteNode()
        }
        if ((event.key == Qt.Key_X) && (event.modifiers & Qt.ControlModifier)){
            _buttleData.cutNode()
        }
    }

    Rectangle {
        id:mainMenu
        width: parent.width
        height: 30
        color: "#141414"

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            color: "#00b2a1"
            text: "ButtleOFX"
            font.pointSize: 14
        }
    }

    //this rectangle represents the zone under the menu, it allows to define the anchors.fill and margins for the SplitterRow
    Rectangle {
        id: modulsContainer
        y: mainMenu.height
        width: parent.width
        height: parent.height - y
        color: "#353535"

        SplitterRow {
            anchors.fill: parent
            anchors.margins: 3
            handleWidth: 3

            SplitterColumn {
                width: 0.7*parent.width
                height: parent.height
                handleWidth: 3
                //Splitter.expanding: true // obligatory to allow to have the minimumWidth

                Player {
                    //Splitter.minimumHeight: 0
                    //Splitter.expanding: true
                    id: player
                    width: parent.width
                    height: 0.5*parent.height
                    node: _buttleData.currentViewerNodeWrapper
                }

                GraphEditor {
                    //Splitter.minimumHeight: 0
                    width: parent.width
                    height: 0.5*parent.height
                }
            }

            ParamEditor {
                //Splitter.minimumWidth: 0 
                width: 0.3*parent.width
                params: _buttleData.currentParamNodeWrapper ? _buttleData.currentParamNodeWrapper.params : null
                currentParamNode: _buttleData.currentParamNodeWrapper ? _buttleData.currentParamNodeWrapper : null
            }
        }
    }
}
