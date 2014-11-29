# AlembicMainWidget.py
# (C)2012-2014
# Scott Ernst

import os

from PySide import QtCore
from PySide import QtGui
from pyaid.OsUtils import OsUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.string.StringUtils import StringUtils
from pyaid.time.TimeUtils import TimeUtils

from pyglass.alembic.AlembicUtils import AlembicUtils
from pyglass.elements.DataListWidgetItem import DataListWidgetItem
from pyglass.widgets.PyGlassWidget import PyGlassWidget
from pyglass.dialogs.PyGlassBasicDialogManager import PyGlassBasicDialogManager

#___________________________________________________________________________________________________ AlembicMainWidget
class AlembicMainWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of AlembicMainWidget."""
        super(AlembicMainWidget, self).__init__(parent=parent, **kwargs)

        self._currentApp      = None
        self._currentDatabase = None
        self._currentRevision = None

        self.initializeBtn.clicked.connect(self._handleInitializeDatabase)
        self.initializeAllBtn.clicked.connect(self._handleInitializeAllDatabases)
        self.createRevisionBtn.clicked.connect(self._handleCreateRevision)
        self.addDatabaseBtn.clicked.connect(self._handleAddDatabase)
        self.removeDatabaseBtn.clicked.connect(self._handleRemoveDatabase)
        self.addAppBtn.clicked.connect(self._handleAddApp)
        self.removeAppBtn.clicked.connect(self._handleRemoveApp)

        self.appsListWidget.itemSelectionChanged.connect(self._handleAppChanged)
        self.databasesListWidget.itemSelectionChanged.connect(self._handleDatabaseChanged)
        self.revisionsListWidget.itemSelectionChanged.connect(self._handleRevisionChanged)

        self.refresh()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: currentAppID
    @property
    def currentAppID(self):
        return self._currentApp.ident if self._currentApp else None

#___________________________________________________________________________________________________ GS: currentAppPath
    @property
    def currentAppPath(self):
        return self._currentApp.itemData['path'] if self._currentApp else None

#___________________________________________________________________________________________________ GS: currentAppResourcesPath
    @property
    def currentAppResourcesPath(self):
        if not self.currentAppPath:
            return None
        return FileUtils.makeFolderPath(self.currentAppPath, 'resources', isDir=True)

#___________________________________________________________________________________________________ GS: currentLocalAppResourcesPath
    @property
    def currentLocalAppResourcesPath(self):
        if not self.currentAppPath:
            return None
        return FileUtils.makeFolderPath(self.currentAppPath, 'resources', 'local', isDir=True)

#___________________________________________________________________________________________________ GS: currentDatabaseID
    @property
    def currentDatabaseID(self):
        return self._currentDatabase.ident if self._currentDatabase else None

#___________________________________________________________________________________________________ GS: currentAppItem
    @property
    def currentAppItem(self):
        return self._currentApp

#___________________________________________________________________________________________________ GS: currentDatabaseItem
    @property
    def currentDatabaseItem(self):
        return self._currentDatabase

#___________________________________________________________________________________________________ GS: currentAppName
    @property
    def currentAppName(self):
        return self._currentApp.text() if self._currentApp else ''

#___________________________________________________________________________________________________ GS: currentDatabaseUrl
    @property
    def currentDatabaseName(self):
        return self._currentDatabase.itemData['name'] if self._currentDatabase else None

#___________________________________________________________________________________________________ GS: currentDatabaseUrl
    @property
    def currentDatabaseUrl(self):
        item = self._currentDatabase
        if not item:
            return ''
        return '%s://%s' % (self.currentAppName, self.currentDatabaseName)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ refresh
    def refresh(self):
        self._refreshAppList()
        self._refreshAppDisplay()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _refreshAppDisplay
    def _refreshAppDisplay(self):
        prevDB = self.currentDatabaseID

        if self.currentAppItem is None:
            self.appLabel.setText('')
            self.operationsWidget.setEnabled(False)
            return
        else:
            self.operationsWidget.setEnabled(True)

        self.appLabel.setText(self.currentAppItem.text())

        w = self.databasesListWidget
        w.clear()

        items   = []
        selected = None
        app = self.currentAppItem.itemData
        for databaseID, data in app['databases'].items():
            items.append(DataListWidgetItem(data['label'], w, ident=databaseID, data=data))
            if databaseID == prevDB:
                selected = items[-1]

        w.setSortingEnabled(True)
        w.sortItems()
        w.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        if not items:
            self._refreshDatabaseDisplay()
            return

        if not selected:
            selected = items[0]
        self._currentDatabase = selected
        self._currentDatabase.setSelected(True)

        self._refreshDatabaseDisplay()

#___________________________________________________________________________________________________ _refreshAppDisplay
    def _refreshDatabaseDisplay(self):
        w = self.revisionsListWidget
        w.clear()

        if self.databasesListWidget.count() == 0:
            w.setEnabled(False)
            self.createRevisionBtn.setEnabled(False)
            self.initializeBtn.setEnabled(False)
            return
        else:
            w.setEnabled(True)
            self.createRevisionBtn.setEnabled(True)
            self.initializeBtn.setEnabled(True)

        revisions = AlembicUtils.getRevisionList(
            databaseUrl=self.currentDatabaseUrl,
            resourcesPath=self.currentAppResourcesPath)

        for rev in revisions:
            name = StringUtils.toText(rev.revision) + (' (HEAD)' if rev.is_head else '')
            DataListWidgetItem(name, w, data=rev)

#___________________________________________________________________________________________________ _refreshAppList
    def _refreshAppList(self):
        prevID   = self.currentAppID
        appsList = self.appsListWidget
        appsList.clear()

        apps = self.appConfig.get('APPLICATIONS')
        if not apps:
            return

        items    = []
        selected = None
        for appID, appData in apps.items():
            items.append(DataListWidgetItem(
                appData['label'], appsList, ident=appID, data=appData))
            if appData['id'] == prevID:
                selected = items[-1]

        appsList.setSortingEnabled(True)
        appsList.sortItems()
        appsList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        if not items:
            return

        if not selected:
            selected = items[0]
        self._currentApp = selected
        self._currentApp.setSelected(True)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleChangeFocalWidget
    def _handleChangeApp(self):
        self.refresh()

#___________________________________________________________________________________________________ _handleCreateRevision
    def _handleCreateRevision(self):
        self.mainWindow.setActiveWidget('revision')
        self.refreshGui()

#___________________________________________________________________________________________________ _handleInitializeAllDatabases
    def _handleInitializeAllDatabases(self):
        self.mainWindow.showLoading(self)
        self.refreshGui()

        AlembicUtils.initializeAppDatabases(
            appName=self.currentAppItem.text(),
            resourcesPath=self.currentAppResourcesPath,
            localResourcesPath=self.currentLocalAppResourcesPath)

        self.mainWindow.hideLoading(self)
        self.refreshGui()

#___________________________________________________________________________________________________ _handleInitializeDatabase
    def _handleInitializeDatabase(self):
        self.mainWindow.showLoading(self)
        self.refreshGui()
        if AlembicUtils.initializeDatabase(
                databaseUrl=self.currentDatabaseUrl,
                resourcesPath=self.currentAppResourcesPath,
                localResourcesPath=self.currentLocalAppResourcesPath):
            PyGlassBasicDialogManager.openOk(
                self,
                'Initialization Complete',
                'Alembic migration environment created.')
        else:
            PyGlassBasicDialogManager.openOk(
                self,
                'Initialization Aborted',
                'Alembic migration already exists.')

        self.mainWindow.hideLoading(self)

#___________________________________________________________________________________________________ _handleAddDatabase
    def _handleAddDatabase(self):
        result = PyGlassBasicDialogManager.openTextQuery(
            parent=self,
            header='Enter Database Name',
            message='Enter the name of the database as it would appear in the Database URL, e.g. '
                    +'"activity" or "employees/artists"')
        if not result:
            return

        data = {
            'id':TimeUtils.getUidTimecode('DATABASE', StringUtils.slugify(result)),
            'label':StringUtils.toText(result).title(),
            'name':result }

        apps = self.appConfig.get('APPLICATIONS')
        app  = apps[self.currentAppID]
        app['databases'][data['id']] = data
        self.appConfig.set('APPLICATIONS', apps)

        self._refreshAppDisplay()
        resultItem = self.databasesListWidget.findItems(result, QtCore.Qt.MatchExactly)
        if resultItem:
            resultItem[0].setSelected(True)

#___________________________________________________________________________________________________ _handleAddDatabase
    def _handleRemoveDatabase(self):
        result = PyGlassBasicDialogManager.openYesNo(
            parent=self,
            header='Confirm Delete',
            message='Are you sure you want to remove the "%s" database from this app?'
                    % self.currentDatabaseName,
            defaultToYes=False)

        if not result:
            return

        apps = self.appConfig.get('APPLICATIONS')

        appData   = apps[self.currentAppID]
        databases = appData['databases']
        del databases[self.currentDatabaseID]
        self.appConfig.set('APPLICATIONS', apps)

        self._refreshAppDisplay()

#___________________________________________________________________________________________________ _handleAppChanged
    def _handleAppChanged(self):
        items = self.appsListWidget.selectedItems()
        self._currentApp = items[0] if items else None
        self._refreshAppDisplay()

#___________________________________________________________________________________________________ _handleDatabaseChanged
    def _handleDatabaseChanged(self):
        items = self.databasesListWidget.selectedItems()
        self._currentDatabase = items[0] if items else None
        self._refreshDatabaseDisplay()

#___________________________________________________________________________________________________ _handleRevisionChanged
    def _handleRevisionChanged(self):
        items = self.revisionsListWidget.selectedItems()
        self._currentRevision = items[0] if items else None

#___________________________________________________________________________________________________ _handleAddApp
    def _handleAddApp(self):
        defaultPath = self.appConfig.get('LAST_APP_PATH', OsUtils.getDocumentsPath())

        path = PyGlassBasicDialogManager.browseForDirectory(
            parent=self,
            caption=StringUtils.dedent("""
                Specify the root path to a PyGlass application, in which a resource folder
                resides"""),
            defaultPath=defaultPath)
        if not path:
            return

        label = PyGlassBasicDialogManager.openTextQuery(
            parent=self,
            header='Enter Application Name',
            message='Specify the name of this application for display within Alembic Migrator',
            defaultText=os.path.basename(path.rstrip(os.sep)) )

        apps = self.appConfig.get('APPLICATIONS', dict())
        appData = {
            'label':label,
            'path':path,
            'databases':dict(),
            'id':TimeUtils.getUidTimecode('App', StringUtils.slugify(label))}
        apps[appData['id']] = appData
        self.appConfig.set('APPLICATIONS', apps)

        self.refresh()
        resultItem = self.appsListWidget.findItems(appData['id'], QtCore.Qt.MatchExactly)
        if resultItem:
            resultItem[0].setSelected(True)

#___________________________________________________________________________________________________ _handleRemoveApp
    def _handleRemoveApp(self):
        item = self.currentAppItem
        if not item:
            return

        result = PyGlassBasicDialogManager.openYesNo(
            parent=self,
            header='Remove Application?',
            message='Are you sure you want to remove the "%s" app?' % self.currentAppName,
            defaultToYes=False)

        if not result:
            return

        apps = self.appConfig.get('APPLICATIONS', dict())
        for appID, appData in apps.items():
            if appID == item.ident:
                del apps[appID]
                break
        self.appConfig.set('APPLICATIONS', apps)
        self.refresh()
