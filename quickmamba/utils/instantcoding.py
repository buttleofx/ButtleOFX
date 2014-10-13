from PyQt5 import QtCore

import os
import time


class ReloadComponent:
    '''
    Functor to reload a QML component.
    Will destroy and recreate the component.
    '''
    
    def __init__(self, qmlFile, component, topLevelItem):
        self._qmlFile = qmlFile
        self._component = component
        self._topLevelItem = topLevelItem

    def __call__(self):
        self._topLevelItem.deleteLater()
        # To reload the view, re-set the source
        self._component.loadUrl(QtCore.QUrl(self._qmlFile))
        self._topLevelItem = self._component.create()
        self._topLevelItem.show()


class ReloadView:
    
    def __init__(self, view):
        '''
        Functor to reload a QQuickView.
        '''
        self._view = view
    
    def __call__(self):
        source = self._view.source()
        self._view.setSource(QtCore.QUrl(source))


class AskQmlItemToReload:
    '''
    Functor to ask the top QML item to reload all the content.
    '''
    
    def __init__(self, topLevelItem):
        self._topLevelItem = topLevelItem
    
    def __call__(self):
        QtCore.QMetaObject.invokeMethod(self._topLevelItem, "reload")


class QmlInstantCoding(QtCore.QObject):
    """
    QmlInstantCoding is an utility class helping developing QML applications.
    It reloads its attached QQuickView whenever one of the watched source file is modified.
    As it consumes resources, make sure to disable file watching in production mode.
    """
    def __init__(self, engine, reloadFunc, watching=True, verbose=False):
        """
        Build a QmlInstantCoding instance.

        engine -- QML engine
        reloadFunc -- The functor that will be called to reload.
                      Will be something like "instantcoding.ReloadComponent(qmlFile, component, topLevelItem)"
        watching -- Defines whether the watcher is active (default: True)
        verbose -- if True, output log infos (default: False)
        """
        super(QmlInstantCoding, self).__init__()

        self._fileWatcher = QtCore.QFileSystemWatcher()  # Internal Qt File Watcher
        self._engine = engine
        self._reload = reloadFunc
        self._watchedFiles = []  # Internal watched files list
        self._verbose = verbose  # Verbose bool
        self._watching = False  # 
        self._extensions = ["qml", "js"]  # File extensions that defines files to watch when adding a folder

        # Update the watching status
        self.setWatching(watching)

    def setWatching(self, watchValue):
        """
        Enable (True) or disable (False) the file watching.

        Tip: file watching should be enable only when developing.
        """
        if self._watching is watchValue:
            return

        self._watching = watchValue
        # Enable the watcher
        if self._watching:
            # 1. Add internal list of files to the internal Qt File Watcher
            self.addFiles(self._watchedFiles)
            # 2. Connect 'filechanged' signal
            self._fileWatcher.fileChanged.connect(self.onFileChanged)

        # Disabling the watcher
        else:
            # 1. Remove all files in the internal Qt File Watcher
            self._fileWatcher.removePaths(self._watchedFiles)
            # 2. Disconnect 'filechanged' signal
            self._fileWatcher.fileChanged.disconnect(self.onFileChanged)

    def setRemarkableExtensions(self, extensions):
        """ Set the list of extensions to search for when using addFilesFromDirectory. """
        self._extensions = extensions

    def getRemarkableExtensions(self):
        """ Returns the list of extensions used when using addFilesFromDirectory. """
        return self._extensions

    def setVerbose(self, verboseValue):
        """ Activate (True) or desactivate (False) the verbose. """
        self._verbose = verboseValue

    def addFile(self, filename):
        """
        Add the given 'filename' to the watched files list.
        'filename' can be an absolute or relative path (str and QUrl accepted)
        """
        # Deal with QUrl type
        # NOTE: happens when using the source() method on a QQuickView
        if isinstance(filename, QtCore.QUrl):
            filename = filename.path()

        # Make sure the file exists
        if not os.path.isfile(filename):
            raise ValueError("addFile: file %s doesn't exist." % filename)

        # Return if the file is already in our internal list
        if filename in self._watchedFiles:
            return

        # Add this file to the internal files list
        self._watchedFiles.append(filename)
        # And, if watching is active, add it to the internal watcher as well
        if self._watching:
            if self._verbose:
                print("instantcoding: addPath", filename)
            self._fileWatcher.addPath(filename)

    def addFiles(self, filenames):
        """
        Add the given 'filenames' to the watched files list.

        filenames -- a list of absolute or relative paths (str and QUrl accepted)
        """
        # Convert to list
        if not isinstance(filenames, list):
            filenames = [filenames]

        for filename in filenames:
            self.addFile(filename)

    def addFilesFromDirectory(self, dirname, recursive=False):
        """
        Add files from the given directory name 'dirname'.

        dirname -- an absolute or a relative path
        recursive -- if True, will search inside each subdirectories recursively.
        """
        if not os.path.isdir(dirname):
            raise RuntimeError("addFilesFromDirectory : %s is not a valid directory." % dirname)

        if recursive:
            for dirpath, dirnames, filenames in os.walk(dirname):
                for filename in filenames:
                    # Removing the starting dot from extension
                    if os.path.splitext(filename)[1][1:] in self._extensions:
                        self.addFile(os.path.join(dirpath, filename))
        else:
            filenames = os.listdir(dirname)
            filenames = [os.path.join(dirname, filename) for filename in filenames if os.path.splitext(filename)[1][1:] in self._extensions]
            self.addFiles(filenames)

    def removeFile(self, filename):
        """
        Remove the given 'filename' from the watched file list.

        Tip: make sure to use relative or absolute path according to how you add this file.
        """
        if filename in self._watchedFiles:
            self._watchedFiles.remove(filename)
        if self._watching:
            self._fileWatcher.removePath(filename)

    def getRegisteredFiles(self):
        """ Returns the list of watched files """
        return self._watchedFiles

    @QtCore.pyqtSlot(str)
    def onFileChanged(self, sourceFile):
        """ Handle changes in a watched file. """
        if self._verbose:
            print("Source file changed : ", sourceFile)
        # Retrieve source file from attached view
        # source = self._component.source()
        # Clear the QQuickEngine cache
        self._engine.clearComponentCache()
        # Remove the modified file from the watched list
        self.removeFile(sourceFile)
        cptTry = 0

        # Make sure file is available before doing anything
        # NOTE: useful to handle editors (Qt Creator) that deletes the source file and
        #       creates a new one when saving
        while not os.path.exists(sourceFile) and cptTry < 10:
            time.sleep(0.1)
            cptTry += 1
        
        print("Reloading ", sourceFile)
        self._reload()
        
        # Finally, read the modified file to the watch system
        self.addFile(sourceFile)
