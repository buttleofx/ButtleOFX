from PySide import QtCore


class ListModel(QtCore.QAbstractListModel):

    """
        Class ListModel defined by:
        - elements : list of QObjects

        Creates a QObject ListModel from a given list of QObjects
    """

    #One column with one object per row
    COLUMNS = ['element']

    def __init__(self, elements):
        QtCore.QAbstractListModel.__init__(self)
        self._elements = elements
        self.setRoleNames(dict(enumerate(ListModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._elements)

    def data(self, index, role):
        if index.isValid() and role == ListModel.COLUMNS.index('element'):
            return self._elements[index.row()]
        return None
