import QtQuick 1.1
import QtDesktop 0.1
import QuickMamba 1.0

import "gui/graph/qml"
import "gui/viewer/qml"
import "gui/paramEditor/qml"

Item {
    width: 1200
    height: 800

    TopFocusHandler {
        //anchors.fill: parent
    }

    Keys.onPressed: {
        if (event.key == Qt.Key_Delete) {
            _buttleManager.destructionNode();
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
        height: 32
        color: "#141414"
        Row {
            spacing: 7
            x: 3
            Rectangle{
                height: 24
                width: 24
                color: "#222"
                border.width: 1
                border.color: "#252525"
                y: 4
                Image {
                    id: mosquito
                    source: "gui/graph/img/mosquito.png"
                    x: 2
                }
            }
            Text {
                color: "#00b2a1"
                text: "ButtleOFX"
                y: 7
                font.pointSize: 14
            }
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
                currentParamNode: _buttleData.currentParamNodeWrapper
            }
        }
    }
}
