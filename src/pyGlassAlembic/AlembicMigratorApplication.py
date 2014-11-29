# AlembicMigratorApplication.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyglass.app.PyGlassApplication import PyGlassApplication

#*************************************************************************************************** AlembicMigratorApplication
class AlembicMigratorApplication(PyGlassApplication):
    """A class for..."""

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: debugRootResourcePath
    @property
    def debugRootResourcePath(self):
        return ['..', '..', 'resources']

#___________________________________________________________________________________________________ GS: appID
    @property
    def appID(self):
        return 'AlembicMigrator'

#___________________________________________________________________________________________________ GS: appGroupID
    @property
    def appGroupID(self):
        return 'pyglassAlembic'

#___________________________________________________________________________________________________ GS: mainWindowClass
    @property
    def mainWindowClass(self):
        from pyGlassAlembic.AlembicMigratorWindow import AlembicMigratorWindow
        return AlembicMigratorWindow

####################################################################################################
####################################################################################################

if __name__ == '__main__':
    AlembicMigratorApplication().run()
