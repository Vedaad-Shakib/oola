##########################################################################
##
## "cookies.py": Cookie processing functions
##
##########################################################################

from django.http import HttpResponse, HttpResponseRedirect

import datetime
import time
import util
from models import *

##########################################################################
##
## "SetUserCookies": Sets the user information in a cookie
##
##########################################################################

def SetUserCookies(request, user):
    if user.autoLogin == 'Y':
        request.session['permUserId']   = user.userId
    else:
        try:
            if request.session['permUserId'] == user.userId:
                del request.session['permUserId']
        except: pass
    #request.session['userType']  = user.userType
    request.session['userId']    = user.userId
    request.session['idleTime']  = user.idleTime
    request.session['fullName']  = user.name
    request.session['lastCheck'] = time.time()

##########################################################################
##
## "GetCurrentUser": Gets the current  user
##
##########################################################################

def GetValidUser( request ):
    errUrl	= '/signin/'
    try:
        userId          = request.session['userId']
        idleTime        = request.session['idleTime']
        lastCheck       = request.session['lastCheck']
    except:
        return None, errUrl

    currTime            = time.time()
    if currTime - lastCheck > idleTime * 60:
        return None, errUrl

    try:
        user            = User.objects.get( userId = userId )
    except:
        return None, errUrl

    request.session['lastCheck']        = currTime
    user.lastActOn                      = datetime.datetime.today()
    user.save()

    return user, None

##########################################################################
##
## "DelUserCookies": deletes the user cookies
##
##########################################################################

def DelUserCookies( request ):
    try:
        #del request.session['userType']
        del request.session['userId']
        del request.session['idleTime']
        del request.session['fullName']
        del request.session['lastCheck']
    except:
        pass

##########################################################################
##
## "GetPermUserId": Gets the perm user id from the cookies
##
##########################################################################

