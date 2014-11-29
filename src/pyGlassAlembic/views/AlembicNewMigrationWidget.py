# AlembicNewMigrationWidget.py
# (C)2012-2014
# Scott Ernst

from pyglass.alembic.AlembicUtils import AlembicUtils
from pyglass.widgets.PyGlassWidget import PyGlassWidget
from pyglass.dialogs.PyGlassBasicDialogManager import PyGlassBasicDialogManager

#___________________________________________________________________________________________________ AlembicNewMigrationWidget
class AlembicNewMigrationWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of AlembicNewMigrationWidget."""
        super(AlembicNewMigrationWidget, self).__init__(parent=parent, **kwargs)

        self.createBtn.clicked.connect(self._handleCreate)
        self.cancelBtn.clicked.connect(self._handleCancel)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: migrationTitle
    @property
    def migrationTitle(self):
        return self.titleLineEdit.text()

#___________________________________________________________________________________________________ GS: migrationInfo
    @property
    def migrationInfo(self):
        return self.detailsText.toPlainText()

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleChangeFocalWidget
    def _handleCancel(self, *args, **kwargs):
        self.mainWindow.setActiveWidget('main')

#___________________________________________________________________________________________________ _handleInitializeAllDatabases
    def _handleCreate(self):
        self.mainWindow.showLoading(self)
        self.refreshGui()

        mainWidget = self.mainWindow.getWidgetFromID('main')

        AlembicUtils.createRevision(
            databaseUrl=mainWidget.currentDatabaseUrl,
            message=self.migrationTitle,
            resourcesPath=mainWidget.currentAppResourcesPath,
            localResourcesPath=mainWidget.currentLocalAppResourcesPath,
            info=self.migrationInfo)

        PyGlassBasicDialogManager.openOk(
            parent=self,
            header='New Revision Created',
            message='New migration revision file has been created.')

        self.mainWindow.hideLoading(self)
        mainWidget.refresh()
        self.mainWindow.setActiveWidget('main')
