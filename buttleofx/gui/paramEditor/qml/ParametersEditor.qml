import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQml 2.1

import QuickMamba 1.0

Item {
    id: parametersEditor
    implicitWidth: 325
    implicitHeight: parent.height

    Rectangle{
        id: paramTitle
        width: parent.width
        height: 40
        color: "#141414"
        /*gradient: Gradient {
               GradientStop { position: 0.0; color: "#141414" }
               GradientStop { position: 0.85; color: "#141414" }
               GradientStop { position: 0.86; color: "#010101" }
               GradientStop { position: 1; color: "#010101" }
        }*/

        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.leftMargin: 10
            color: "white"
            font.pointSize: 11
            text: "Parameters"
            clip: true
        }


    }


    // Container of the paramEditors
    Rectangle{
        id: contentParamEditor
        height: parent.height
        width: parent.width
        y: paramTitle.height
        color: "#141414"

        // scroll all the parameditors
        ScrollView {
            anchors.fill: parent
            anchors.topMargin: 5
            anchors.bottomMargin: 5
            height: 20
            width: 20

            // for each node we create a ParamEditor
            ListView{
                anchors.fill: parent
                model: _buttleData.editedNodesWrapper
                delegate: paramDelegate
            }
        }

        // delegate of the list of ParamEditor
        Component {
            id: paramDelegate
            Rectangle{
                height: paramEditor_multiple.height + 40


                ParamEditorForParametersEditor {
                    id: paramEditor_multiple
                    width: contentParamEditor.width - 10 // -10 to let place for the general scrollbar
                    params: model.object ?  model.object.params : null
                    currentParamNode: model.object
                }

            }
        }

    }
}
