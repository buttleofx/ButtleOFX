import QtQuick 1.1
import QuickMamba 1.0

DropAreaImpl {
    id: dropAreaItem
    anchors.fill: parent
    
    // HACK to expose signal parameters with named params
    signal dragEnter(
        bool hasText, string text,
        bool hasHtml, string html,
        bool hasUrls, string firstUrl,
        variant buttons, variant dropAction,
        variant modifiers, variant pos,
        variant possibleActions, variant proposedAction,
        string source)
        
    signal dragMove(
        bool hasText, string text,
        bool hasHtml, string html,
        bool hasUrls, string firstUrl,
        variant buttons, variant dropAction,
        variant modifiers, variant pos,
        variant possibleActions, variant proposedAction,
        string source)
        
    signal dragLeave(
        bool hasText, string text,
        bool hasHtml, string html,
        bool hasUrls, string firstUrl,
        variant buttons, variant dropAction,
        variant modifiers, variant pos,
        variant possibleActions, variant proposedAction,
        string source)
        
    signal drop(
        bool hasText, string text,
        bool hasHtml, string html,
        bool hasUrls, string firstUrl,
        variant buttons, variant dropAction,
        variant modifiers, variant pos,
        variant possibleActions, variant proposedAction,
        string source)
    
    Component.onCompleted: {
        dropAreaItem.internDragEnter.connect(dragEnter)
        dropAreaItem.internDragMove.connect(dragMove)
        dropAreaItem.internDragLeave.connect(dragLeave)
        dropAreaItem.internDrop.connect(drop)
    }
}


