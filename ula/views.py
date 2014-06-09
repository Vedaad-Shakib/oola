###############################################################################
## Copyright (c) 2013-2014 Bogt, Inc.
## All rights reserved.
## This source code is confidential and may not be disclosed.
###############################################################################

###############################################################################
##
## "views.py":  create the web pages
##
###############################################################################

from django.shortcuts  import render_to_response
from django.conf       import settings
from django.template   import RequestContext
from django.http       import HttpResponseRedirect
from django.http       import HttpResponse

import cookies
import math
import operator
import datetime
import json

from forms import *
from cookies import *
from email_util import *

#==============================================================================
#
# "mainPage": display the home page
#
#==============================================================================

def mainPage(request, checkSignup=None, checkSignin=None):

    # if checking for signup
    if checkSignup is not None:
	form = SignupForm(request.GET.copy())
	if form.is_valid():
	    user = form.save()
	    email = form.data['email']
	    user = User.objects.get(email=email)
	    SetUserCookies(request, user)
	    url     = '/myprofile/'
	    if user.userType:
                url = '/students/'
	    json = util.JsonLoad(               url             )
	else:
	    json = util.JsonFormError(form)
	return HttpResponse(json,
			    mimetype='application/json')

    # if checking for signin
    if checkSignin is not None:
	form = SigninForm(request.GET.copy())
	if form.is_valid():
	    user = User.objects.get(email=form.data['email'])
	    SetUserCookies(request, user)
	    url     = '/myprofile/'
	    if user.userType:
                url = '/students/'
	    json = util.JsonLoad(               url             )
	else:
	    json = util.JsonFormError(form)
	return HttpResponse(json,
			    mimetype='application/json')

    # normal call
    try:
        userName = request.session['fullName']
        userId   = request.session['userId']
        user     = User.objects.get(userId=userId)
        userType = user.userType
        return render_to_response( 'home.html',
                                      {'userName': userName,
                                       'userType': userType,
                                       },
                                      context_instance=RequestContext(request))
    except:
	forup = SignupForm()
	forin = SigninForm()
	return render_to_response( 'home.html',
                                      {'forup':  forup,
                                       'forin':  forin,
                                       'userName': None,
                                       'userType': None,
                                      # 'actionUrl':"/mainPage/"
                                       },
                                      context_instance=RequestContext(request))

#==============================================================================
#
# "signout":
#
#==============================================================================

def signout(request, check=None):
    DelUserCookies(request)
    return HttpResponseRedirect('/home/')

#==============================================================================
#
# "signin":
#
#==============================================================================

def signin(request, check=None):
    if check is not None:
        data    = request.GET.copy(                                     )
        form    = SigninForm(   data                                    )

	if form.is_valid():
	    user = User.objects.get(email=form.data['email'])
	    SetUserCookies(request, user)
	    url     = '/myprofile/'
	    if user.userType:
                url = '/students/'
	    json = util.JsonLoad(               url             )
	else:
	    json = util.JsonFormError(form)
	return HttpResponse(json,
			    mimetype='application/json')

    form                        = SigninForm(                           )

    return render_to_response(  'signin.html',
                                {'form': form},
                                context_instance=RequestContext(request))

#==============================================================================
#
# "classPage": The main class page in which dancers can check in
#
#==============================================================================

def classPage(request):
    DelUserCookies(request)
    #form = ClassName()
    userList = list(User.objects.all())
    userNames = []
    for i in userList:
        userNames.append(str(i.name))
    return render_to_response('class.html',
                              {'userNames': userNames},
                              context_instance=RequestContext(request))

#==============================================================================
#
# "classCheckRecent": Check if the student has recently checked in
#
#==============================================================================

def classCheckRecent(request):
    jdata       = {}
    jdata["recent"] = False
    try:
        user    = User.objects.get(name = request.GET["name"] )
        currTime= datetime.datetime.now()
        lst10Min= currTime - datetime.timedelta(minutes = 10)        
        lstAttendance = Attendance.objects.get(userId = user.userId,
                                              dateTime__gt = lst10Min
                                              )
        if lstAttendance:
            jdata["recent"] = True
            jdata["name"]   = user.name
            jdata["userId"] = user.userId
            jdata["attendanceId"] = lstAttendance.attendanceId
    except: pass

    jsonData            = json.dumps( jdata )
    return HttpResponse(    jsonData,   mimetype    = 'application/json')

#==============================================================================
#
# "classCancel": The cancellation page
#
# Reason for this page: more secure than doing this on the main class page
#
#==============================================================================

def classCancel(request, totalGuests, userId, attendanceId):
    Attendance.objects.filter(attendanceId = attendanceId).delete()
    user = User.objects.get(userId=userId)
    user.balance = user.balance + 1 + int(str(totalGuests))
    user.save()
    return HttpResponseRedirect('/class/')

#==============================================================================
#
# "classSave": The save page
#
# Reason for this page: more secure than doing this on the main class page
#
#==============================================================================

def classSave(request, guests, userId, oldCount):
    guests      = int(str(guests))
    oldCount    = int(str(oldCount))

    user = User.objects.get(userId=userId)
    # update the counts and balance
    newCount = guests + 1
    user.balance = user.balance - newCount + oldCount
    user.save()
    # remove old records
    attendanceList = list(Attendance.objects.filter(userId = user.userId))
    today = datetime.datetime.today()
    for i in attendanceList:
        if i.dateTime.year == today.year and i.dateTime.month == today.month \
	    and i.dateTime.day == today.day:
            Attendance.objects.filter(attendanceId = i.attendanceId).delete()
    # create an attendance record
    attendance = Attendance()
    attendance.userId = User.objects.get(userId = user.userId)
    attendance.dateTime = datetime.datetime.today()
    attendance.DancerNumber = newCount
    attendance.save()

    return HttpResponseRedirect('/class/')

#==============================================================================
#
# "classCheckin": redirects to if the user is not in the database
#
#==============================================================================

def classCheckin(request, userId = None):

    if userId != None:
        # get the parameters; come from signup (new student)
        user        = User.objects.get(userId=userId)
        name        = user.name
        guests      = 0
        oldCount    = user.balance

    else:
        # get the parameters;
        try:
            name = request.POST['name']
            guests = int(str(request.POST['guests']))
            oldCount = int(str(request.POST['oldCount']))
        except:
            return render_to_response('classInvalid.html',
                                   {"redirect": "/class/"},
                                  context_instance=RequestContext(request))
        # redirect if the user not found
        try:
            user = User.objects.get(name=name)
        except:
            request.session['name'] = name
            return HttpResponseRedirect('/class/signup/')

        # cancel the previous checkin
        try:
            lstAttendanceId = request.POST['attendanceId']
            lstAttendance   = Attendance.objects.get(attendanceId = lstAttendanceId)
            savedCount      = lstAttendance.DancerNumber
            lstAttendance.delete()
            user.balance    = user.balance + savedCount
            user.save()
        except:
            pass
        
    # update the counts and balance
    newCount = guests + 1
    user.balance = user.balance - newCount + oldCount
    user.save()
    # remove old records
    attendanceList = list(Attendance.objects.filter(userId = user.userId))
    today = datetime.datetime.today()
    for i in attendanceList:
        if i.dateTime.year == today.year and i.dateTime.month == today.month \
	    and i.dateTime.day == today.day:
            Attendance.objects.filter(attendanceId = i.attendanceId).delete()
    # create an attendance record
    attendance = Attendance()
    attendance.userId = User.objects.get(userId = user.userId)
    attendance.dateTime = datetime.datetime.today()
    attendance.DancerNumber = newCount
    attendance.save()
    # confirm
    return render_to_response("classCheckin.html",
                              {"name": user.name,
                               "balance": user.balance,
                               "guests": guests,
                               "userId": user.userId,
			       "oldCount": newCount,
                               "waiver": user.waiverSigned},
                              context_instance=RequestContext(request))

#==============================================================================
#
# "classSignup": signup page if the user is not in the database
#
#==============================================================================

def classSignup(request, check=None):
    if check is not None:
      form = ClassSignup(request.GET.copy())
      if form.is_valid():
          user = form.save()
          SetUserCookies(request, user)
          json = util.JsonLoad('/class/checkin/' + str( user.userId ) + "/")
      else:
          json = util.JsonFormError(form)
      return HttpResponse(json,
			  mimetype='application/json')
    else:
        try:
            name = request.session['name'].title()
        except:
            name = ""
        form = ClassSignup( initial = {'name': name } )
        return render_to_response('classSignup.html',
                                  {'form': form,
                                   'name': name},
                                  context_instance=RequestContext(request))

#==============================================================================
#
# "students": The admin landing page
#
#==============================================================================

def students( request, sortBy="name0", page="1", range="all"):

    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)

    userList = list(User.objects.all())

    now	= datetime.datetime.now()
    for user in userList:
	bday			= user.birthday
	user.hasBirthday	= (bday.year != 1970)
	user.showBirthday	= (user.userId == 1)	# check Bday within 2 days
	user.recent		= ((now - user.lastAccess).total_seconds() < 2*24*3600)

    currPage	= 4
    nPages	= 4
    nStudents	= len( userList )
    url		= request.get_full_path()

    return render_to_response( 'students.html',
                               {'userName':	user.name,
                                'userType':	user.userType,
                                'userList':	userList,
				'nStudents':	nStudents,
				'currPage':	currPage,
				'nPages':	nPages,
				'url':		url,
                                },
                               context_instance=RequestContext(request) )

#==============================================================================
#
# "students": The admin landing page
#
#==============================================================================

def xstudents( request, sortBy="name0", page="1", range="all"):

    #if request.session['userType'] == 0:
    #    return HttpResponseRedirect('/clearance/')

    try:
        userName = request.session['fullName']
        #userType = request.session['userType']
        userId   = request.session['userId']
        user     = User.objects.get(userId=userId)
        userType = user.userType
    except:
        return HttpResponseRedirect('/')

    # if was redirected from "save" button in extra notes page
    if request.POST:
        userId = request.POST['userId']
        user = User.objects.get(userId=userId)
        if request.POST['birthday'] != '':
            birthday = datetime.date(int(str(request.POST['birthday'])[:4]), int(str(request.POST['birthday'])[5:7]),int(str(request.POST['birthday'])[8:]))
        else:
            birthday = ''
        user.name = request.POST['name']
        name = request.POST['name']
        try:
            waiverSigned = request.POST['waiverSigned']
            user.waiverSigned = True
        except:
            user.waiverSigned = False

        try:
            facebookConnected = request.POST['facebookConnected']
            user.facebook = True
        except:
            user.facebook = False

        user.address = request.POST['address']
        if user.birthday != birthday:
            user.birthdayAssigned = True
        if birthday != '':
            user.birthday = birthday
        user.email = request.POST['email']
        user.notes = request.POST['notes']
        user.balance = request.POST['balance']
        user.save()

    range = str(range)
    tEnd = datetime.datetime.now()
    if range == "year":
        tBeg = datetime.datetime(tEnd.year - 1, tEnd.month, tEnd.day)
    if range == "all":
        tBeg = datetime.datetime(1970, 1, 1)
    if range == "month":
        if tEnd.month == 1:
            tBeg = datetime.datetime(tEnd.year, tEnd.month+11, tEnd.day)
        else:
            tBeg = datetime.datetime(tEnd.year, tEnd.month-1, tEnd.day)
    if range == "day":
        try:
            tBeg = datetime.datetime(tEnd.year, tEnd.month, tEnd.day - 1)
        except:
            tBeg = datetime.datetime(tEnd.year, tEnd.month, 1)

    if range == "week":
        if tEnd.day - 7 < 1:
            if str(tEnd.month) in "2468911":
                tBeg = datetime.datetime(tEnd.year, tEnd.month-1, 31-(7-tEnd.day))
            else:
                tBeg = datetime.datetime(tEnd.year, tEnd.month-1, 30-(7-tEnd.day))
        else:
            tBeg = datetime.datetime(tEnd.year, tEnd.month, tEnd.day - 7)

    if tEnd.day - 7 < 1:
        if str(tEnd.month) in "2468911":
            lastWeek = datetime.datetime(tEnd.year, tEnd.month-1, 31-(7-tEnd.day))
        else:
            lastWeek = datetime.datetime(tEnd.year, tEnd.month-1, 30-(7-tEnd.day))
    else:
        lastWeek = datetime.datetime(tEnd.year, tEnd.month, tEnd.day - 7)

    today = datetime.datetime.now()

    attendance = list(Attendance.objects.filter(dateTime__range=[tBeg, tEnd]))
    cnt = {}
    for i in attendance:
        cnt[i.userId.userId] = 1

    if request.GET:
        searchFilled = True
        form = SearchForm( request.GET.copy() )
        searchTerm = form.data['search'].title()
    else:
        form = SearchForm()
        searchFilled = False
        searchTerm = None

    usersPerPage = 4
    page = int(page)
    sortBy = str(sortBy)
    if sortBy[:-1] == "waiver":
        sortBy = "waiverSigned" + sortBy[-1]
    if sortBy[:-1] == "bday":
        sortBy = "birthdayAssigned" + sortBy[-1]

    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)

    if searchFilled:
        userList = list(User.objects.filter(name__contains=searchTerm))
    else:
        userList = list(User.objects.all())

    userList2 = []
    for i in userList:
        if cnt.has_key(i.userId):
            userList2.append( i )

    if range != "all":
        userList = userList2

    numUsers = len(userList)
    maxPages = int(math.ceil((numUsers+0.0)/usersPerPage))
    if maxPages < 1:
        maxPages = 1

    userList.sort(key=operator.attrgetter('name'))
    if sortBy[-1] == "0":
        rev = False
    else:
        rev = True
    userList.sort(key=operator.attrgetter(sortBy[:-1]), reverse=rev)

    if sortBy[:-1] == "waiverSigned":
        sortBy = "waiver" + sortBy[-1]
    if sortBy[:-1] == "birthdayAssigned":
        sortBy = "bday" + sortBy[-1]

    if maxPages < page:
        return HttpResponseRedirect('/students/'+sortBy+'/'+ str(int(maxPages)) + '/all/')

    startNum = (page-1)*usersPerPage
    endNum   = (page)*usersPerPage
    userList = userList[startNum:endNum]

    if page != 1:
        prevPage = page - 1
    else:
        prevPage = -1

    if page > 2:
        prevPrevPage = page - 2
    else:
        prevPrevPage = -1

    if page < maxPages:
        nextPage = page + 1
    else:
        nextPage = -1

    if (page+1) < maxPages:
        nextNextPage = page + 2
    else:
        nextNextPage = -1

    lastPage = maxPages

    if sortBy[:-1] == "waiver":
        waiver = "waiver"+str(int(sortBy[-1])^1)
        bday = "bday0"
        name = "name0"
        balance = "balance0"
    if sortBy[:-1] == "name":
        name = "name"+str(int(sortBy[-1])^1)
        bday = "bday0"
        waiver = "waiver0"
        balance= "balance0"
    if sortBy[:-1] == "balance":
        balance = "balance"+str(int(sortBy[-1])^1)
        bday = "bday0"
        name = "name0"
        waiver = "waiver0"
    if sortBy[:-1] == "bday":
        bday = "bday"+str(int(sortBy[-1])^1)
        waiver = "waiver0"
        name = "name0"
        balance= "balance0"

    if searchTerm:
        search = searchTerm
        if search.find(" ") != -1:
            i = search.find(" ")
            search = search[:i]+"+"+search[i+1:]
        search = "?search=" + search
    else:
        search = ""

    range = str(range) + "/"

    url = str(sortBy) + "/" + str(page) + "/" + str(range)

    return render_to_response( 'Admin-landing.html',
                               {'userName': userName,
                                'userType': userType,
                                'userList': userList,
                                'page': str(page),
                                'prevPage': str(prevPage),
                                'prevPrevPage':str(prevPrevPage),
                                'nextNextPage':str(nextNextPage),
                                'nextPage':str(nextPage),
                                'lastPage':str(lastPage),
                                'waiver':waiver,
                                'name':name,
                                'bday':bday,
                                'balance':balance,
                                'sortBy':sortBy,
                                'form':form,
                                'search':search,
                                'range':range,
                                'lastWeek': lastWeek,
                                'today': today,
                                'url': url,
                                },
                               context_instance=RequestContext(request) )

#==============================================================================
#
# "clearance": A user does not have permission to be somewhere
#
#==============================================================================

def clearance(request):
    try:
        userName = request.session['fullName']
        #userType = request.session['userType']
        userId   = request.session['userId']
        user     = User.objects.get(userId=userId)
        userType = user.userType

        return render_to_response('clearance.html',
                                      {'userName': userName,
                                       'userType': userType,
                                       },
                                      context_instance=RequestContext(request))
    except:
        if checkSignup is not None:
            form = SignupForm(request.GET.copy())
            if form.is_valid():
                user = form.save()
                email = form.data['email']
                user = User.objects.get(email=email)
                SetUserCookies(request, user)
                json = util.JsonLoad('/students/name0/1/all')
            else:
                json = util.JsonFormError(form)
            return HttpResponse(json,
                                mimetype='application/json')
        elif checkSignin is not None:
            form = SigninForm(request.GET.copy())
            if form.is_valid():
                user = User.objects.get(email=form.data['email'])
                SetUserCookies(request, user)
                json = util.JsonLoad('/students/name0/1/all')
            else:
                json = util.JsonFormError(form)
            return HttpResponse(json,
                                mimetype='application/json')
        else:
            forup = SignupForm()
            forin = SigninForm()
            return render_to_response('clearance.html',
                                      {'forup':  forup,
                                       'forin':  forin,
                                       'userName': None,
                                       'userType': None,
                                       },
                                      context_instance=RequestContext(request))

#==============================================================================
#
# "userPage": The more information page
#
#==============================================================================

def userPage(request):
    try:
        userId = request.GET['id']
    except:
        return HttpResponseRedirect('/students/name0/1/all/')

    try:
        url = request.GET['url']
    except:
        url = 'name0/1/all/'

    user = User.objects.get(userId=userId)

    name = user.name
    birthday = ''  if user.birthdayAssigned == False else str(user.birthday.date())
    balance = user.balance
    email = user.email
    address = user.address
    waiverSigned = "1" if user.waiverSigned else "-1"
    facebookConnected = "1" if user.facebook else "-1"
    notes = user.notes if user.notes else "Extra Notes"
    userId = user.userId

    return render_to_response('notes.html',
                                      {'name': name,
                                       'birthday': birthday,
                                       'email': email,
                                       'address': address,
                                       'waiverSigned': waiverSigned,
                                       'facebookConnected': facebookConnected,
                                       'notes': notes,
                                       'balance': balance,
                                       'userId': userId,
                                       'url': url,
                                       },
                                      context_instance=RequestContext(request))

#==============================================================================
#
# "dateRagnePicker": Date Range Picker Tester
#
#==============================================================================

def dateRangePicker(request):
    return render_to_response('dateSelector.html',
                             {},
                             context_instance=RequestContext(request))

#==============================================================================
#
# "forgotPassword": Forgot password page
#
#==============================================================================

def forgotPassword( request, check = None ):
    if check is not None:
	data	= request.GET.copy()
	form	= ForgotPasswordForm( data )
	if form.is_valid():
            email	= form.data['email']
            user	= User.objects.get( email__exact = email        )
            forgotPasswd= form.save(                                    )
            emailBody   = "Dear %s" %user.name
            emailBody   +="<br/><br/>To reset your account passowrd, please click on the following link:"
            emailBody   +="<br/>"
            emailBody   += settings.PROJECT_URL + "forgotCode/" + forgotPasswd.forgotCode

            util.emailNotification(             "Forgot password",
                                                user,
                                                emailBody                 )

	    json	= util.JsonLoad(        '/forgotPdSentEmail/'    )
	else:
	    json	= util.JsonFormError(   form                    )
	return HttpResponse(json, mimetype =    'application/json'      )

    form	= ForgotPasswordForm()
    extraInformation  = "Please enter the e-mail address registered with your account.<br/>An e-mail containing a password reset link will be sent to your email."

    forup = SignupForm()
    forin = SigninForm()
    return render_to_response(  'forgot_password.html',
                                {'form': form,
                                 'forup':  forup,
                                 'forin':  forin,
                                 'extraInformation': extraInformation
                                 },
                                context_instance=RequestContext(request))

def forgotPdSentEmail( request ):
    forup = SignupForm()
    forin = SigninForm()
    return render_to_response(  'forgotPwdSentEmail.html',
                                {'forup':  forup,
                                 'forin':  forin,
                                },
				context_instance=RequestContext(request) )

##############################################################################
##
## "changePassword":  Change Password page
##
###############################################################################

def changePassword( request, forgotCode = None, check = None ):
    if check is not None:
	data	= request.GET.copy(                                     )
	form	= ChangePasswordForm(           data                    )
	form.forgotCode = forgotCode
	if form.is_valid():
            user	= form.save(                                    )

##	    SetUserCookies(                     request,        user    )

            emailBody   = "Dear %s" %user.name
            emailBody   +="<br/><br/>Your passowrd has been reset on www.Ula.com."
            emailBody   +="<br/>"
	
            util.emailNotification(             "Change password",
                                               user,
                                                emailBody           )
            json	= util.JsonLoad( '/passwordChanged/'     )
	else:
            json	= util.JsonFormError(   form                    )
	return HttpResponse(json, mimetype = 'application/json')

    today	        = datetime.datetime.today(                      )
    ( validFlag, msg )  = chkValidForgotCode(   forgotCode              )
    if validFlag:
        form	        = ChangePasswordForm(                           )
        return render_to_response('changePassword.html',
                               {
                                'form':     form,
                                'actionUrl':"/forgotCode/" + forgotCode + "/"
                                },
                  context_instance=RequestContext(request) )

    else:
        forup = SignupForm()
        forin = SigninForm()
        return render_to_response('denyAccess.html',
    				{
                                  'message':    msg,
                                  'forup':  forup,
                                  'forin':  forin,
				},
				  context_instance=RequestContext(request))


def passwordChanged( request ):
    forup = SignupForm()
    forin = SigninForm()
    return render_to_response(  'passwordChanged.html',
                                {'forup':  forup,
                                 'forin':  forin,
                                },
				context_instance=RequestContext(request) )


###############################################################################
##
## "chkValidForgotCode": Check forgot code validation
##
###############################################################################

def chkValidForgotCode( forgotCode ):
    today	        = datetime.datetime.today(                      )
    validFlag           = False
    retMsg              = ""
    try:
        forgotPasswd    = ForgotPassword.objects.get(
                                               forgotCode__exact = forgotCode)
        if forgotPasswd.active == 'Y':
            chkTime     = ( today - forgotPasswd.forgotTime ).seconds
            if chkTime > 21600:
                retMsg  = "Your time has been expired. You have only 6 hours"
                retMsg  +=" to change your password."
            else:
                validFlag= True
                forgotPasswd.active = 'N'
                forgotPasswd.save(                                      )
        else:
            retMsg      = "Sorry, the forgot code had been used before and "
            retMsg      +="is not valid."

    except:
        retMsg          = "Sorry, the user info is invalid."

    return ( validFlag, retMsg )

#==============================================================================
#
# "myprofile":
#
#==============================================================================

def myprofile(request, check=None):

    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)
    if check is not None:
        data    = request.GET.copy(                                     )
        form    = MyprofileForm(   data                                 )

	if form.is_valid():
            form.save(                                                  )
	    json = util.JsonLoad('/home/')
	else:
	    json = util.JsonFormError(form)
	return HttpResponse(json,
			    mimetype='application/json')

    form    = MyprofileForm(initial = {'userId':    user.userId,
                                       'name':      user.name,
                                       'email':     user.email,
                                       'birth':     user.birthday.date(),
                                       'phone':     user.phone,
                                       'address':   user.address,
                                       'idleTime':  user.idleTime,
                                    }
                                 )

    return render_to_response(  'myProfile.html',
                                {'form':    form,
                                 'userName':user.name,
                                 'userType':user.userType,
                                },
                                context_instance=RequestContext(request))

#==============================================================================
#
# "test":
#
#==============================================================================

def test(request):
    for i in range(100):
        sendEmailBasic('vedaad799@gmail.com')
    return HttpResponseRedirect('/')
