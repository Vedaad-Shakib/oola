##########################################################################
##  Copyright (c) 2012-2012 Opticate, Inc.
##  All rights reserved.
##  This source code is confidential and may not be disclosed.
##########################################################################

##########################################################################
##
## "util.py":
##
##########################################################################

import time
import datetime
import random
import hashlib
import types
import json

from django.conf        import settings
#from django.utils       import simplejson
from django.core.mail   import EmailMultiAlternatives

##########################################################################
## 
## "log": output to log
##
#########################################################################

def log( msg ):
    f = open( '/var/tmp/opticate_log', 'a' )
    f.write( "%s: %s\n" % (time.ctime(),msg) )

##########################################################################
## 
## "randomStr": generate a random string
##
#########################################################################

def randomStr( strLen ):
    alpha	= 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKHLMOPQRSTUVWXYZ'
    alphaNum	= alpha + '0123456789'
    nAs		= len(alpha)
    nAns	= len(alphaNum)
    idx 	= int(random.random()*nAs) % nAs
    str		= alpha[idx]
    for i in range(1,strLen):
	idx 	= int(random.random()*nAns) % nAns
	str	+= alphaNum[idx]
    return str

##########################################################################
## 
## "encryptPass": encrypt a password
##
#########################################################################

def encryptPass( password, algo='', salt='' ):
    if algo == '': algo = 'sha1'
    if salt == '': salt = hashlib.new(algo,str(random.random())).hexdigest()[:5]
    hsh = hashlib.new(algo, salt+password).hexdigest()
    encPass = '%s$%s$%s' % (algo, salt, hsh)
    return encPass

###############################################################################
##
## "JsonLoad":  Build the json load return data
##
###############################################################################

def JsonLoad( url = "", closeSecId = "", loadUrl = "", loadSecId = "" ):
    jdata		= {}
    jdata["load"]       = True
    jdata["url"]        = url

    if loadUrl:
        jdata["loadUrl"]    = loadUrl

    if closeSecId:
        if closeSecId[0] == "#":
            jdata["closeSecId"] = closeSecId
        else:
            jdata["closeSecId"] = "#" + closeSecId

    if loadSecId:
        if loadSecId[0] == "#":
            jdata["loadSecId"] = loadSecId
        else:
            jdata["loadSecId"] = "#" + loadSecId
        
    jsonData            = json.dumps( jdata )
    return jsonData

###############################################################################
##
## "JsonFormError":  Build the json form error return data
##
###############################################################################

def JsonFormError( form ):
    
    errors		= {}
    for field in form:
	if len(field.errors) > 0:
	    errors[field.name]	= field.errors[0]
    jdata		= {}
    jdata["load"]	= False
    jdata["errors"]	= errors
    jsonData 		= json.dumps( jdata )
    return jsonData

###############################################################################
##
## "emailNotification":  Set the email message for the notification
##
###############################################################################

def emailNotification( subject, user, htmlMsg):
    
    sender      = settings.EMAIL_FROM
    txtMsg      = ""
    msg         = EmailMultiAlternatives(   subject,   txtMsg,
                                            sender,
                                            [user.email]                )
    msg.attach_alternative(                 htmlMsg,    "text/html"     )

    msg.send(                                                           )

