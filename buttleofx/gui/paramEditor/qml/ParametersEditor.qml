import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQml 2.1

import QuickMamba 1.0

Item {
    id: parametersEditor


    implicitWidth: 325
    implicitHeight: parent.height



   SplitView {
       width: parent.width
       height: parent.height
       //handleWidth: 3
       orientation: Qt.Vertical


        Rectangle{
           id: paramTitle
           width: parent.width
           height: 40
           color: "#141414"

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
          color: "#010101"


        // for each node we create a ParamEditor
           Repeater{
                model: _buttleData.graphWrapper.nodeWrappers
                id: repeaterParamEditor

                ParamEditor {
                    height: contentParamEditor.height
                    width: contentParamEditor.width
                    params: model.object ?  model.object.params : null
                    currentParamNode: model.object
                }
            }
        }
    }
}
