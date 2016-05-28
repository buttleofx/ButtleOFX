import QtQuick 2.0
import Qt.labs.folderlistmodel 1.0

ListView {
     width: 200
     height: 400

     FolderListModel {
         id: folderModel
         folder:"/home/jordi"
         nameFilters: ["*"]
     }

     Component {
         id: fileDelegate
         Text { text: fileName }
     }

     model: folderModel
     delegate: fileDelegate
 }
