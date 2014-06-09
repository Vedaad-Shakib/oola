###############################################################################
## Copyright (c) 2013-2013 Opticate, Inc.
## All rights reserved.
## This source code is confidential and may not be disclosed.
###############################################################################

###############################################################################
##
## "updateDb.py";  A function to udate django data base.
##
###############################################################################

import  sys
import  MySQLdb

from    apps        import settings
from	subprocess  import Popen, PIPE

#===========================================================================
#
# Errors
#
#===========================================================================

class UpdateDbError( Exception ):
    def __init__( self, value ):
        self.value = "ERROR from updateDb.py module: %s" % value
    def __str__( self ):
        return repr( self.value )

#===========================================================================
# runPyProcess: A function for running the process.
#===========================================================================

def runPyProcess( args = None ):
    """ A function for running Django python modules.
        
        Arguments:
        args    - The process arguments.
        
        Output:
        None
        """
    
    command     = [ "python" ]
    
    if args:
        for arg in args:
            command.append(             arg                             )
    
    proc        = Popen(                args    = command,
                                        stdout	= PIPE,
                                        stderr	= PIPE                  )

    pError	= proc.stderr
    funcError	= pError.readlines(                                     )
    if funcError:
        errorMsg= ""
        for msg in funcError:
            errorMsg += msg
        print
        raise UpdateDbError, errorMsg
    
    
    pOutput	= proc.stdout
    return pOutput.readlines(                                           )

#---------------------------------------------------------------------------
# Check command line to get user data
#---------------------------------------------------------------------------

userData    = sys.argv

try:
    tblName = userData[ userData.index(     "-add"              ) + 1 ]
    colName = userData[ userData.index(     "-col"              ) + 1 ]
    colType = userData[ userData.index(     "-type"             ) + 1 ]
    addData = True
except:
    addData = False
    
try:
    defVal  = userData[ userData.index(     "-default"          ) + 1 ]
except:
    defVal  = None

try:
    tblName = userData[ userData.index(     "-remove"           ) + 1 ]
    colName = userData[ userData.index(     "-col"              ) + 1 ]
    rmvData = True
except:
    rmvData = False

#---------------------------------------------------------------------------
# Define variables
#---------------------------------------------------------------------------

dbName      = settings.DATABASES["default"]["NAME"]
dbUsr       = settings.DATABASES["default"]["USER"]
dbPass      = settings.DATABASES["default"]["PASSWORD"]

#---------------------------------------------------------------------------
# Create the data base connection
#---------------------------------------------------------------------------

try:
    dbConn  = MySQLdb.connect(  host    = "localhost",  user    = dbUsr,
                                passwd  = dbPass,       db      = dbName)
    
except:
    
    #=====================================================================
    #
    # Check if database exist; if not create it
    #
    #=====================================================================

    #---------------------------------------------------------------------
    # Connect to the MySQL as root
    #---------------------------------------------------------------------

    print 'Enter the MySQL "root" password.'
    rootPass= raw_input('Press "Enter" if you have not assigned a password to it: ')
    
    if rootPass:
        dbConn  = MySQLdb.connect(user      = 'root',   passwd  = rootPass)
    else:
        dbConn  = MySQLdb.connect(user      = 'root'                    )
        
    dbCursor    = dbConn.cursor(                                        )

    #---------------------------------------------------------------------
    # Check if database exists 
    #---------------------------------------------------------------------

    cmd         = "SHOW DATABASES LIKE '%s'" %dbName
    retVal      = dbCursor.execute(         cmd                         )

    if retVal:
        raise UpdateDbError, "Can not connect to the data base."
    
    #---------------------------------------------------------------------
    # Create user
    #---------------------------------------------------------------------
    
    cmd         = "CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';"%(dbUsr,dbPass)
    retVal      = dbCursor.execute(         cmd                         )

    #---------------------------------------------------------------------
    # Create the data base and give the user to access it.
    #---------------------------------------------------------------------

    cmd     = "CREATE DATABASE %s" %dbName
    dbCursor.execute(                       cmd                         )
    
    cmd     = "GRANT ALL ON %s.* TO '%s'@'localhost';"%(dbName, dbUsr   )
    dbCursor.execute(                       cmd                         )

    dbConn.close(                                                       )

    #---------------------------------------------------------------------
    # Connect to the database with the setting.py user name and password.
    #---------------------------------------------------------------------

    dbConn  = MySQLdb.connect(  host    = "localhost",  user    = dbUsr,
                                passwd  = dbPass,       db      = dbName)

dbCursor    = dbConn.cursor(                                            )

#---------------------------------------------------------------------------
# Set settings variables
#---------------------------------------------------------------------------

_comnPyCmd  =  'from apps import settings; '
_comnPyCmd  += 'settings.DATABASES["default"]["NAME"]       = "%s"; ' %dbName
_comnPyCmd  += 'settings.DATABASES["default"]["USER"]       = "%s"; ' %dbUsr
_comnPyCmd  += 'settings.DATABASES["default"]["PASSWORD"]   = "%s"; ' %dbPass
_comnPyCmd  += 'import os;'
_comnPyCmd  += 'import sys;'
_comnPyCmd  += 'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.settings");'
_comnPyCmd  += 'from django.core.management import execute_from_command_line; '
_comnPyCmd  += 'execute_from_command_line(sys.argv);'

#---------------------------------------------------------------------------
# Add a new column to a table
#---------------------------------------------------------------------------

if addData:
    addCmd  = 'ALTER TABLE ' + tblName + ' '
    addCmd  +='ADD ' +  colName + ' ' + colType + ';'
    dbCursor.execute(                       addCmd                      )
    
    if defVal != None:
        addCmd  = 'UPDATE ' + tblName + ' SET '
        addCmd  += colName + ' = ' + defVal + ';'
        dbCursor.execute(                   addCmd                      )
        

#---------------------------------------------------------------------------
# Remove a new column to a table
#---------------------------------------------------------------------------

elif rmvData:
    rmvCmd  = 'ALTER TABLE ' + tblName + ' '
    rmvCmd  +='DROP COLUMN ' + colName + ';'
    dbCursor.execute(                       rmvCmd                      )

#---------------------------------------------------------------------------
# Add new tables to data base
#---------------------------------------------------------------------------

else:
    args    = [ "-c",  _comnPyCmd, "sqlall", "ula" ]
    retVal  = runPyProcess(                 args                        )
    execStr = ""
    for i in retVal:
        if i !="\n":
            execStr += i
    execCmd = execStr.split(                ";"                         )
    for i in execCmd:
        try:
            dbCursor.execute(               i                           )
        except:
            pass
