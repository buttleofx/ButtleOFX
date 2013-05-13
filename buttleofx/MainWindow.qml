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

        // Graph toolbar
        if (event.key == Qt.Key_Delete) {
            if(_buttleData.currentConnectionWrapper) {
                _buttleManager.connectionManager.disconnect(_buttleData.currentConnectionWrapper);
            }
            else {
                _buttleManager.nodeManager.destructionNodes();
            }
        }
        if ((event.key == Qt.Key_Z) && (event.modifiers & Qt.ControlModifier)) {
            _buttleManager.undo();
        }
        if ((event.key == Qt.Key_Y) && (event.modifiers & Qt.ControlModifier)) {
            _buttleManager.redo();
        }
        if ((event.key == Qt.Key_D) && (event.modifiers & Qt.ControlModifier)){
            _buttleManager.nodeManager.duplicationNode()
        }
        if ((event.key == Qt.Key_C) && (event.modifiers & Qt.ControlModifier)){
            _buttleManager.nodeManager.copyNode()
        }
        if ((event.key == Qt.Key_V) && (event.modifiers & Qt.ControlModifier)){
            _buttleManager.nodeManager.pasteNode()
        }
        if ((event.key == Qt.Key_X) && (event.modifiers & Qt.ControlModifier)){
            _buttleManager.nodeManager.cutNode()
        }

        // Viewer
        if ((event.key == Qt.Key_1) && (event.modifiers & Qt.KeypadModifier)){
            _buttleData.currentViewerIndex = 1
            _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(1)
            _buttleEvent.emitViewerChangedSignal()
        }
        if ((event.key == Qt.Key_2) && (event.modifiers & Qt.KeypadModifier)){
            _buttleData.currentViewerIndex = 2
            _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(2)
            _buttleEvent.emitViewerChangedSignal()
        }
        if ((event.key == Qt.Key_3) && (event.modifiers & Qt.KeypadModifier)){
            _buttleData.currentViewerIndex = 3
            _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(3)
            _buttleEvent.emitViewerChangedSignal()
        }
        if ((event.key == Qt.Key_4) && (event.modifiers & Qt.KeypadModifier)){
            _buttleData.currentViewerIndex = 4
            _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(4)
            _buttleEvent.emitViewerChangedSignal()
        }
        if ((event.key == Qt.Key_5) && (event.modifiers & Qt.KeypadModifier)){
            _buttleData.currentViewerIndex = 5
            _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(5)
            _buttleEvent.emitViewerChangedSignal()
        }
        if ((event.key == Qt.Key_6) && (event.modifiers & Qt.KeypadModifier)){
            _buttleData.currentViewerIndex = 6
            _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(6)
            _buttleEvent.emitViewerChangedSignal()
        }
        if ((event.key == Qt.Key_7) && (event.modifiers & Qt.KeypadModifier)){
            _buttleData.currentViewerIndex = 7
            _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(7)
            _buttleEvent.emitViewerChangedSignal()
        }
        if ((event.key == Qt.Key_8) && (event.modifiers & Qt.KeypadModifier)){
            _buttleData.currentViewerIndex = 8
            _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(8)
            _buttleEvent.emitViewerChangedSignal()
        }
        if ((event.key == Qt.Key_9) && (event.modifiers & Qt.KeypadModifier)){
            _buttleData.currentViewerIndex = 9
            _buttleData.currentViewerNodeWrapper = _buttleData.getNodeWrapperByViewerIndex(9)
            _buttleEvent.emitViewerChangedSignal()
        }
    }

    Rectangle {
        id: mainMenu
        width: parent.width
        height: 32
        color: "#141414"
        Row {
            spacing: 10
            x: 3

            Image {
                id: mosquito
                source: _buttleData.buttlePath + "/gui/img/icons/logo_icon.png"
                y: 5
            }

            Text {
                color: "white"
                text: "File"
                y: 11
                font.pointSize: 10

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        _fileMenu.showMenu(parent.x, mainMenu.height)
                    }
                }
            }

            Text {
                color: "white"
                text: "Edit"
                y: 11
                font.pointSize: 10

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        _editMenu.showMenu(parent.x, mainMenu.height)
                    }
                }
            }

            Text {
                color: "white"
                text: "Add"
                y: 11
                font.pointSize: 10

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        _addMenu.showMenu(parent.x, mainMenu.height)
                    }
                }
            }

            Text {
                color: "white"
                text: "Render"
                y: 11
                font.pointSize: 10

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        _renderMenu.showMenu(parent.x, mainMenu.height)
                    }
                }
            }

            Text {
                color: "white"
                text: "Window"
                y: 11
                font.pointSize: 10

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        _windowMenu.showMenu(parent.x, mainMenu.height)
                    }
                }
            }

            Text {
                color: "white"
                text: "Help"
                y: 11
                font.pointSize: 10

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        _helpMenu.showMenu(parent.x, mainMenu.height)
                    }
                }
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
