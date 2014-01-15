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

    Rectangle{
        id: contentParamEditor
        height: parent.height
        width: parent.width
        y: paramTitle.height
        color: "#141414"



        // for each node we create a ParamEditor
        ScrollView {
            anchors.fill: parent
            anchors.topMargin: 5
            anchors.bottomMargin: 5
            height: 110
            width: 110

            // repeater of the node parameters
            Repeater{
                model: _buttleData.graphWrapper.nodeWrappers
                id: repeaterParamEditor


                Rectangle{
                    //// to modify ////
                    height: contentParamEditor.height / 2
                    y: (index) * height
                    /////

                    ParamEditor {
                        //height: contentParamEditor.height
                        width: contentParamEditor.width
                        params: model.object ?  model.object.params : null
                        currentParamNode: model.object
                    }
                }
            }

        }

    }
}
