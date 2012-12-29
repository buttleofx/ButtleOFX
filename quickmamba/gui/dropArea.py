from PySide import QtCore
from PySide import QtDeclarative

class DropArea(QtDeclarative.QDeclarativeItem):
    # QGraphicsSceneDragDropEvent:
    #Qt::MouseButtons buttons, Qt::DropAction dropAction, const QMimeData mimeData, Qt::KeyboardModifiers modifiers, QPointF pos, Qt::DropActions possibleActions, Qt::DropAction proposedAction, QWidget source
    internDragEnter = QtCore.Signal(
        bool, str, # text
        bool, str, # html
        bool, str, # urls
        QtCore.Qt.MouseButtons, QtCore.Qt.DropAction,
        QtCore.Qt.KeyboardModifiers, QtCore.QPointF,
        QtCore.Qt.DropActions, QtCore.Qt.DropAction,
        str)
    internDragMove = QtCore.Signal(
        bool, str, # text
        bool, str, # html
        bool, str, # urls
        QtCore.Qt.MouseButtons, QtCore.Qt.DropAction,
        QtCore.Qt.KeyboardModifiers, QtCore.QPointF,
        QtCore.Qt.DropActions, QtCore.Qt.DropAction,
        str)
    internDragLeave = QtCore.Signal(
        bool, str, # text
        bool, str, # html
        bool, str, # urls
        QtCore.Qt.MouseButtons, QtCore.Qt.DropAction,
        QtCore.Qt.KeyboardModifiers, QtCore.QPointF,
        QtCore.Qt.DropActions, QtCore.Qt.DropAction,
        str)
    internDrop = QtCore.Signal(
        bool, str, # text
        bool, str, # html
        bool, str, # urls
        QtCore.Qt.MouseButtons, QtCore.Qt.DropAction,
        QtCore.Qt.KeyboardModifiers, QtCore.QPointF,
        QtCore.Qt.DropActions, QtCore.Qt.DropAction,
        str)

    def __init__(self, parent = None):
        QtDeclarative.QDeclarativeItem.__init__(self, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if self._acceptDropValue:
            #print 'dragEnterEvent acceptDrop'
            event.setAccepted(True)
            event.acceptProposedAction()
            self.setCursor(QtCore.Qt.DragMoveCursor)
            
            urls = event.mimeData().urls()
            firstUrl = urls[0].toLocalFile() if len(urls) else ""
            self.internDragEnter.emit(
                event.mimeData().hasText(), event.mimeData().text(),
                event.mimeData().hasHtml(), event.mimeData().html(),
                event.mimeData().hasUrls(), firstUrl,
                #event.mimeData().hasImage(), event.mimeData().imageData(),
                #event.mimeData().hasColor(), event.mimeData().colorData(),
                
                event.buttons(), event.dropAction(),
                event.modifiers(), event.pos(),
                event.possibleActions(), event.proposedAction(),
                event.source().accessibleName() if event.source() else "")

    def dragMoveEvent(self, event):
        if self._acceptDropValue:
            #print 'dragMoveEvent'
            urls = event.mimeData().urls()
            firstUrl = urls[0].toLocalFile() if len(urls) else ""
            self.internDragMove.emit(
                event.mimeData().hasText(), event.mimeData().text(),
                event.mimeData().hasHtml(), event.mimeData().html(),
                event.mimeData().hasUrls(), firstUrl,
                #event.mimeData().hasImage(), event.mimeData().imageData(),
                #event.mimeData().hasColor(), event.mimeData().colorData(),
                
                event.buttons(), event.dropAction(),
                event.modifiers(), event.pos(),
                event.possibleActions(), event.proposedAction(),
                event.source().accessibleName() if event.source() else "")

    def dragLeaveEvent(self, event):
        if self._acceptDropValue:
            #print 'dragLeaveEvent'
            urls = event.mimeData().urls()
            firstUrl = urls[0].toLocalFile() if len(urls) else ""
            self.internDragLeave.emit(
                event.mimeData().hasText(), event.mimeData().text(),
                event.mimeData().hasHtml(), event.mimeData().html(),
                event.mimeData().hasUrls(), firstUrl,
                #event.mimeData().hasImage(), event.mimeData().imageData(),
                #event.mimeData().hasColor(), event.mimeData().colorData(),
                
                event.buttons(), event.dropAction(),
                event.modifiers(), event.pos(),
                event.possibleActions(), event.proposedAction(),
                event.source().accessibleName() if event.source() else "")
            
            self.unsetCursor()

    def dropEvent(self, event):
        #print 'dropEvent'
        if self._acceptDropValue:
            #print 'dropEvent acceptDrop'
            event.setAccepted(True)
            event.acceptProposedAction()
            #print 'text:', event.mimeData().hasText(), event.mimeData().text()
            #print 'html:', event.mimeData().hasHtml(), event.mimeData().html()
            #print 'url:', event.mimeData().hasUrls(), [u.toLocalFile() for u in event.mimeData().urls()]
            
            # hasText()  text()      text/plain
            # hasHtml()  html()      text/html
            # hasUrls()  urls()      text/uri-list
            # hasImage() imageData() image/ *
            # hasColor() colorData() application/x-color
            
            urls = event.mimeData().urls()
            firstUrl = urls[0].toLocalFile() if len(urls) else ""
            self.internDrop.emit(
                event.mimeData().hasText(), event.mimeData().text(),
                event.mimeData().hasHtml(), event.mimeData().html(),
                event.mimeData().hasUrls(), firstUrl,
                #event.mimeData().hasImage(), event.mimeData().imageData(),
                #event.mimeData().hasColor(), event.mimeData().colorData(),
                
                event.buttons(), event.dropAction(),
                event.modifiers(), event.pos(),
                event.possibleActions(), event.proposedAction(),
                event.source().accessibleName() if event.source() else "")
            
            self.unsetCursor()


    def getAcceptDrop(self):
        return self._acceptDropValue
    def setAcceptDrop(self, acceptDrop):
        self._acceptDropValue = acceptDrop
        self.update()
        self.acceptDropChanged.emit()
    acceptDropChanged = QtCore.Signal()
    _acceptDropValue = True
    acceptDrop = QtCore.Property(bool, getAcceptDrop, setAcceptDrop, notify=acceptDropChanged)

