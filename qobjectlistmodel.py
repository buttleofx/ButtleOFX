from PySide import QtCore


class QObjectListModel(QtCore.QAbstractListModel):
    """
    QObjectListModel provides a more powerful, but still easy to use, alternative to using
    QObjectList lists as models for QML views. As a QAbstractListModel, it has the ability to
    automatically notify the view of specific changes to the list, such as adding or removing
    items. At the same time it provides QList-like convenience functions such as append, at,
    and removeAt for easily working with the model from Python.

    This class is the Python port of the C++ QObjectListModel class.
    """
    def __init__(self, parent):
        """ Constructs an object list model with the given parent. """
        super(QObjectListModel, self).__init__(parent)

        self._objects = list()      # Internal list of objects
        roles = dict()
        self.ObjectRole = QtCore.Qt.UserRole + 1
        roles[self.ObjectRole] = "object"
        self.setRoleNames(roles)

    def __iter__(self):
        """ Enables iteration over the list of objects. """
        return iter(self._objects)

    def __len__(self):
        return self.size()

    def __nonzero__(self):
        return self.size() > 0

    def data(self, index, role):
        """ Returns data for the specified role, from the item with the
        given index. The only valid role is ObjectRole.

        If the view requests an invalid index or role, an invalid variant
        is returned.
        """
        if index.row() < 0 or index.row() >= len(self._objects):
            return None

        if role == self.ObjectRole:
            return self._objects[index.row()]

        return None

    def rowCount(self, parent):
        """ Returns the number of rows in the model. This value corresponds to the
        number of items in the model's internal object list.
        """
        return self.size()

    def objectList(self):
        """ Returns the object list used by the model to store data. """
        return self._objects

    def setObjectList(self, objects):
        """ Sets the model's internal objects list to objects. The model will
        notify any attached views that its underlying data has changed.
        """
        self.beginResetModel()
        self._objects = objects
        self.endResetModel()
        self.dataChanged.emit(self.index(0), self.index(self.size()))

    ############
    # List API #
    ############
    def append(self, toAppend):
        """ Inserts object(s) at the end of the model and notifies any views.
        Accepts both QObject and list of QObjects.
        """
        if not isinstance(toAppend, list):
            toAppend = [toAppend]
        self.beginInsertRows(QtCore.QModelIndex(), self.size(), self.size() + len(toAppend))
        self._objects.extend(toAppend)
        self.endInsertRows()
        self.countChanged.emit()

    def insert(self, i, toInsert):
        """  Inserts object(s) at index position i in the model and notifies
        any views. If i is 0, the object is prepended to the model. If i
        is size(), the object is appended to the list.
        Accepts both QObject and list of QObjects.
        """
        if not isinstance(toInsert, list):
            toInsert = [toInsert]
        self.beginInsertRows(QtCore.QModelIndex(), i, i + len(toInsert))
        for obj in reversed(toInsert):
            self._objects.insert(i, obj)
        self.endInsertRows()
        self.countChanged.emit()

    def at(self, i):
        return self._objects[i]

    def replace(self, i, obj):
        """ Replaces the item at index position i with object and
        notifies any views. i must be a valid index position in the list
        (i.e., 0 <= i < size()).
        """
        self._objects[i] = obj
        self.countChanged.emit()

    def move(self, fromIndex, toIndex):
        """ Moves the item at index position from to index position to
        and notifies any views.
        This function assumes that both from and to are at least 0 but less than
        size(). To avoid failure, test that both from and to are at
        least 0 and less than size().
        """
        value = toIndex
        if toIndex > fromIndex:
            value += 1
        if not self.beginMoveRows(QtCore.QModelIndex(), fromIndex, fromIndex, QtCore.QModelIndex(), value):
            return
        self._objects.insert(toIndex, self._objects.pop(fromIndex))
        self.endMoveRows()

    def removeAt(self, i, count=1):
        """  Removes count number of items from index position i and notifies any views.
        i must be a valid index position in the model (i.e., 0 <= i < size()), as
        must \c{i + count - 1}.
        """
        self.beginRemoveRows(QtCore.QModelIndex(), i, i + count)
        for cpt in range(count):
            self._objects.pop(i)
        self.endRemoveRows()
        self.countChanged.emit()

    def takeAt(self, i):
        """  Removes the item at index position i (notifying any views) and returns it.
        i must be a valid index position in the model (i.e., 0 <= i < size()).
        """
        self.beginRemoveRows(QtCore.QModelIndex(), i, i)
        obj = self._objects.pop(i)
        self.endRemoveRows()
        self.countChanged.emit()
        return obj

    def clear(self):
        """ Removes all items from the model and notifies any views. """
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.size())
        self._objects = []
        self.endRemoveRows()
        self.countChanged.emit()

    def contains(self, obj):
        """ Returns true if the list contains an occurrence of object;
        otherwise returns false.
        """
        return obj in self._objects

    def indexOf(self, matchObj, fromIndex=0):
        """ Returns the index position of the first occurrence of object in
        the model, searching forward from index position from.
        """
        return self._objects[fromIndex:].index(matchObj) + fromIndex

    def lastIndexOf(self, matchObj, fromIndex=-1):
        """    Returns the index position of the last occurrence of object in
        the list, searching backward from index position from. If
        from is -1 (the default), the search starts at the last item.
        """
        r = list(self._objects)
        r.reverse()
        return - r[-fromIndex - 1:].index(matchObj) + fromIndex

    def size(self):
        """ Returns the number of items in the model. """
        return len(self._objects)

    def isEmpty(self):
        """ Returns true if the model contains no items; otherwise returns false. """
        return len(self._objects) == 0

    @QtCore.Slot(int)
    def get(self, i):
        """ For usage from QML. """
        return self._objects[i]

    countChanged = QtCore.Signal()
    count = QtCore.Property(int, size, notify=countChanged)
