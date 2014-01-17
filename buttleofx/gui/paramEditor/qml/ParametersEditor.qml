import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQml 2.1

import QuickMamba 1.0

Item {
   id: parametersEditor

   /*   ParamEditor {
          id : paramModel
           params: _buttleData.currentParamNodeWrapper ? _buttleData.currentParamNodeWrapper.params : null
           currentParamNode: _buttleData.currentParamNodeWrapper
       }


      Component {
           id: paramsDelegate
           Item {
               width: 200; height: 50
               Text { id: nameField; text: name }
               Text { text: '$' + cost; anchors.left: nameField.right }
               Row {
                   anchors.top: nameField.bottom
                   spacing: 5
                   Text { text: "Attributes:" }
                   Repeater {
                       model: attributes
                       Text { text: description }
                   }
               }
           }

       }

       ListView {
           anchors.fill: parent
           model: 3
           delegate: paramModel
       }

*/
   ///////////////////////// TO SUPPRESS ////////////////////////////
   MouseArea{
       x : 50
       y: 0
       width: 800
       height: 800
       onClicked:   console.log(_buttleData.graphWrapper.nodeWrappers.object)
   }
   ////////////////////////////////////////////////////////////////////


    // for each node we create a ParamEditor
   Repeater{
        model: _buttleData.graphWrapper.nodeWrappers

        /*Text{
            text: model.object.name
        }
        */

        ParamEditor {
            params: model.object ?  model.object.params : null
            currentParamNode: model.object
        }
    }

}
