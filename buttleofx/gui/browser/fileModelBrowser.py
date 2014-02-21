import logging
import os

from quickmamba.models import QObjectListModel

from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtWidgets import QWidget, QFileDialog


class FileItem(QtCore.QObject):
    
    _isSelected = False
    
    class Type():
        """ Enum """
        File = 'File'
        Folder = 'Folder'
        Sequence = 'Sequence'
    
    def __init__(self, folder, fileName, fileType):
        super(FileItem, self).__init__()
        if folder == "/":
            self._filepath = folder + fileName
        else:
            self._filepath = folder + "/" + fileName
        self._fileType = fileType

    def getFilepath(self):
        return self._filepath
    
    def setFilepath(self, newpath):
        import shutil
        shutil.move(self.filepath, newpath + "/" + self.fileName)
    
    def getFileType(self):
        return self._fileType
    
    def getFileName(self):
        return os.path.basename(self._filepath)
    
    def setFileName(self, newName):
        os.rename(self.filepath, os.path.dirname(self._filepath) + "/" + newName)
        
    def getFileSize(self):
        return os.stat(self._filepath).st_size
    
    def getSelected(self):
        return self._isSelected
    
    def setSelected(self, isSelected):
        self._isSelected = isSelected
        self.isSelectedChange.emit()

    filepath = QtCore.pyqtProperty(str, getFilepath, setFilepath, constant=True)
    fileType = QtCore.pyqtProperty(str, getFileType, constant=True)
    fileName = QtCore.pyqtProperty(str, getFileName, setFileName, constant=True)
    fileSize = QtCore.pyqtProperty(float, getFileSize, constant=True)
    isSelectedChange = QtCore.pyqtSignal()
    isSelected = QtCore.pyqtProperty(bool, getSelected, setSelected, notify=isSelectedChange)


class FileModelBrowser(QtQuick.QQuickItem):
    """Class FileModelBrowser"""
    
    _folder = ""
    
    def __init__(self, parent=None):
        super(FileModelBrowser, self).__init__(parent)
        self._fileItemsModel = QObjectListModel(self)
    
    def getFolder(self):
        return self._folder
    
    def setFolder(self, folder):
        self._folder = folder
        self.updateFileItems(folder)
        self.folderChanged.emit()
        
    @QtCore.pyqtSlot(str)
    def createFolder(self, path):
        os.mkdir(path)
        self.updateFileItems(self._folder)
        
    @QtCore.pyqtSlot(int, str)
    def moveItem(self, index, newpath):
        if index < len(self._fileItems):
            self._fileItems[index].filepath = newpath
        self.updateFileItems(self._folder)
    
    def getFolderExists(self):
        import os
        return os.path.exists(self._folder)
    
    def getParentFolder(self):
        return os.path.dirname(self._folder)

    folderChanged = QtCore.pyqtSignal()
    folder = QtCore.pyqtProperty(str, getFolder, setFolder, notify=folderChanged)
    exists = QtCore.pyqtProperty(bool, getFolderExists, notify=folderChanged)
    parentFolder = QtCore.pyqtProperty(str, getParentFolder, constant=True)
    
    def updateFileItems(self, folder):
        self._fileItems = []
        self._fileItemsModel.clear()
        allDirs = []
        allFiles = []
        import os
        try:
            _, dirs, files = next(os.walk(folder))
            for d in dirs:
                if not d.startswith("."):
                    allDirs.append(FileItem(folder, d, FileItem.Type.Folder))
            
            if self._nameFilter == "*":
                for f in files:
                    (shortname, extension) = os.path.splitext(f)
                    extension = extension.split(".")[-1].lower()
                    if extension in ['jpeg', 'jpg', 'jpe', 'jfif', 'jfi', 
                                     'png','mkv', 'mpeg', 'mp4', 'avi', 'mov',
                                     'aac', 'ac3', 'adf', 'adx', 'aea', 'ape',
                                     'apl', 'mac', 'bin', 'bit', 'bmv', 'cdg',
                                     'cdxl', 'xl', '302', 'daud', 'dts', 'dv',
                                     'dif', 'cdata', 'eac3', 'flm', 'flac', 'flv',
                                     'g722', '722', 'tco', 'rco', 'g723_1', 'g729',
                                     'gsm', 'h261', 'h26l', 'h264', '264', 'idf',
                                     'cgi', 'latm', 'm4v', 'mjpg', 'mjpeg', 'mpo',
                                     'mlp', 'mp2', 'mp3', 'm2a', 'mpc', 'mvi', 'mxg',
                                     'v', 'nut', 'ogg', 'oma', 'omg', 'aa3', 'al', 'ul',
                                     'sw', 'sb', 'uw', 'ub', 'yuv', 'cif', 'qcif', 'rgb',
                                     'rt', 'rso', 'smi', 'sami', 'sbg', 'shn', 'vb', 'son',
                                     'mjpg', 'sub', 'thd', 'tta', 'ans', 'art', 'asc',
                                     'diz', 'ice', 'nfo', 'txt', 'vt', 'vc1', 'vqf', 'vql',
                                     'vqe', 'vtt', 'yop', 'y4m','3fr', 'ari', 'arw', 'bay',
                                     'crw', 'cr2', 'cap', 'dng', 'dcs', 'dcr', 'dng', 'drf',
                                     'eip', 'erf', 'fff', 'iiq', 'k25', 'kdc', 'mef', 'mos',
                                     'mrw', 'nef', 'nrw', 'obm', 'orf', 'pef', 'ptx', 'pxn',
                                     'r3d', 'rad', 'raf', 'rw2', 'raw', 'rwl', 'rwz', 'srf',
                                     'sr2', 'srw', 'x3f','aai', 'art', 'arw', 'avi', 'avs',
                                     'bmp', 'bmp2', 'bmp3', 'cals', 'cgm', 'cin', 'cmyk',
                                     'cmyka', 'cr2', 'crw', 'cur', 'cut', 'dcm', 'dcr', 'dcx',
                                     'dib', 'djvu', 'dng', 'dot', 'dpx', 'emf', 'epdf', 'epi',
                                     'eps', 'eps2', 'eps3', 'epsf', 'epsi', 'ept', 'exr', 'fax',
                                     'fig', 'fits', 'fpx', 'gif', 'gplt', 'gray', 'hdr', 'hpgl',
                                     'hrz', 'html', 'ico', 'info', 'inline', 'jbig', 'jng',
                                     'jp2', 'jpc', 'jpg', 'jpeg', 'man', 'mat', 'miff', 'mono',
                                     'mng', 'm2v', 'mpeg', 'mpc', 'mpr', 'mrw', 'msl', 'mtv',
                                     'mvg', 'nef', 'orf', 'otb', 'p7', 'palm', 'pam', 'pbm', 
                                     'pcd', 'pcds', 'pcl', 'pcx', 'pdb', 'pdf', 'pef', 'pfa', 'pfb',
                                     'pfm', 'pgm', 'picon', 'pict', 'pix', 'png', 'png8', 'png16',
                                     'png32', 'pnm', 'ppm', 'ps', 'ps2', 'ps3', 'psb', 'psd', 'ptif',
                                     'pwp', 'rad', 'rgb', 'rgba', 'rla', 'rle', 'sct', 'sfw', 'sgi',
                                     'shtml', 'sid', 'mrsid', 'sun', 'svg', 'tga', 'tiff', 'tim',
                                     'tif', 'txt', 'uil', 'uyvy', 'vicar', 'viff', 'wbmp', 'webp',
                                     'wmf', 'wpg', 'x', 'xbm', 'xcf', 'xpm', 'xwd', 'x3f', 'ycbcr',
                                     'ycbcra', 'yuv','bmp', 'cin', 'dds', 'dpx', 'exr', 'fits', 'hdr',
                                     'ico', 'j2k', 'j2c', 'jp2', 'jpeg', 'jpg', 'jpe', 'jfif', 'jfi',
                                     'pbm', 'pgm', 'png', 'pnm', 'ppm', 'pic', 'psd', 'rgbe', 'sgi',
                                     'tga', 'tif', 'tiff', 'tpic', 'tx', 'webp']:
                        if not f.startswith("."):
                            allFiles.append(FileItem(folder, f, FileItem.Type.File))
                    
            else:
                for f in files:
                    (shortname, extension) = os.path.splitext(f)
                    if extension == self._nameFilter:
                        print("Only ", extension, " files")
                        allFiles.append(FileItem(folder, f, FileItem.Type.File))
                          
        except Exception:
            pass

        allDirs.sort(key=lambda fileItem: fileItem.fileName.lower())
        allFiles.sort(key=lambda fileItem: fileItem.fileName.lower())
        self._fileItems = allDirs + allFiles

        self._fileItemsModel.setObjectList(self._fileItems)
        
    @QtCore.pyqtSlot(str, result=QtCore.QObject)
    def getFilteredFileItems(self, fileFilter):
        suggestions = QObjectListModel(self)

        try:
            _, dirs, files = next(os.walk(os.path.dirname(fileFilter)))
            for d in dirs:
                if not d.startswith(".") and d.startswith(os.path.basename(fileFilter)) and d != os.path.basename(fileFilter):
                    suggestions.append(FileItem(os.path.dirname(fileFilter), d, FileItem.Type.Folder))
            
        except Exception:
            pass
        return suggestions
        #return suggestions.sort(key=lambda fileItem: fileItem.fileName)
    
    _fileItems = []
    _fileItemsModel = None
    
    @QtCore.pyqtSlot(str, int)
    def changeFileName(self, newName, index):
        if index < len(self._fileItems):
            self._fileItems[index].fileName = newName
        self.updateFileItems(self._folder)
            
    @QtCore.pyqtSlot(int)
    def deleteItem(self, index):
        if index < len(self._fileItems):
            if self._fileItems[index].fileType == FileItem.Type.Folder:
                import shutil
                shutil.rmtree(self._fileItems[index].filepath)
            if self._fileItems[index].fileType == FileItem.Type.File:
                os.remove(self._fileItems[index].filepath)
        self.updateFileItems(self._folder)
                
    @QtCore.pyqtSlot(result=QtCore.QObject)
    def getSelectedItems(self):
        selectedList = QObjectListModel(self)
        for item in self._fileItems:
            if item.isSelected == True:
                selectedList.append(item)

        return selectedList
    
    def getFileItems(self):
        return self._fileItemsModel
    
    @QtCore.pyqtSlot(int)
    def selectItem(self, index):
        for item in self._fileItems:
            item.isSelected = False
        if index < len(self._fileItems):
            self._fileItems[index].isSelected = True

    @QtCore.pyqtSlot(int)
    def selectItems(self, index):
        if index < len(self._fileItems):
            self._fileItems[index].isSelected = True
            
    @QtCore.pyqtSlot(int, int)
    def selectItemsByShift(self, begin, end):
        for i in range(begin, end + 1):
            if i < len(self._fileItems):
                self._fileItems[i].isSelected = True
    
    def getFilter(self):
        return self._nameFilter
     
    def setFilter(self, nameFilter):
        self._nameFilter = nameFilter
        self.updateFileItems(self._folder)
        self.nameFilterChange.emit()

    fileItems = QtCore.pyqtProperty(QtCore.QObject, getFileItems, notify=folderChanged)
    nameFilterChange = QtCore.pyqtSignal()
    nameFilter = QtCore.pyqtProperty(str, getFilter, setFilter, notify=nameFilterChange)


