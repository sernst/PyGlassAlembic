# AlembicMigratorWindow.py
# (C)2012-2014
# Scott Ernst

from pyglass.windows.PyGlassWindow import PyGlassWindow

from pyGlassAlembic.views.AlembicMainWidget import AlembicMainWidget
from pyGlassAlembic.views.AlembicNewMigrationWidget import AlembicNewMigrationWidget


#___________________________________________________________________________________________________ AlembicMigratorWindow
class AlembicMigratorWindow(PyGlassWindow):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of PyGlassWindow."""
        PyGlassWindow.__init__(
            self, widgets={
                'main':AlembicMainWidget,
                'revision':AlembicNewMigrationWidget},
            **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _initializeImpl
    def _initializeImpl(self, *args, **kwargs):
        self.setActiveWidget('main')
        super(AlembicMigratorWindow, self)._initializeImpl(*args, **kwargs)
