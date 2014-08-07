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
from django.db.models  import Q

import cookies
import math
import csv
import operator
from datetime import datetime, timedelta
import json

from forms import *
from cookies import *
from email_util import *

import      paginator

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

    user.lastAccess         = datetime.datetime.now(            )
    user.save()

    #----------------------------------------------------------------------
    # Set the recent change
    #----------------------------------------------------------------------

    rcntChg                     = RecentChange(                     )
    rcntChg.userId              = user
    rcntChg.change              = "Balance"
    rcntChg.value               = str( user.balance )
    rcntChg.dateTime            = datetime.datetime.now(            )
    rcntChg.save(                                                   )

    
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
    user.lastAccess         = datetime.datetime.now(            )
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

    #----------------------------------------------------------------------
    # Set the recent change
    #----------------------------------------------------------------------

    rcntChg                     = RecentChange(                     )
    rcntChg.userId              = user
    rcntChg.change              = "Balance"
    rcntChg.value               = str( user.balance )
    rcntChg.dateTime            = datetime.datetime.now(            )
    rcntChg.save(                                                   )

    rcntChg                     = RecentChange(                     )
    rcntChg.userId              = user
    rcntChg.change              = "Attendance (Dancer Number)"
    rcntChg.value               = str( newCount )
    rcntChg.dateTime            = datetime.datetime.now(            )
    rcntChg.save(                                                   )


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
    user.lastAccess         = datetime.datetime.now(            )
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


    #----------------------------------------------------------------------
    # Set the recent change
    #----------------------------------------------------------------------

    rcntChg                     = RecentChange(                     )
    rcntChg.userId              = user
    rcntChg.change              = "Balance"
    rcntChg.value               = str( user.balance )
    rcntChg.dateTime            = datetime.datetime.now(            )
    rcntChg.save(                                                   )

    rcntChg                     = RecentChange(                     )
    rcntChg.userId              = user
    rcntChg.change              = "Attendance (Dancer Number)"
    rcntChg.value               = str( newCount )
    rcntChg.dateTime            = datetime.datetime.now(            )
    rcntChg.save(                                                   )


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
# "history": The attendance and transactions page
#
#==============================================================================

def history( request, search = "" ):
    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)

    return render_to_response( 'history.html',
                               {'userName':	user.name,
                                'userType':	user.userType,
                                'sort':         "date",
                                'filter':       "attendance",
                                'currPage':     1,
                                'search':       search
                                },
                               context_instance=RequestContext(request) )

#==============================================================================
#
# "historyList": The history page
#
#==============================================================================

def historyList( request ):

    # Get "get" values
    sort    = str(request.POST['sort'])
    filter  = str(request.POST['filter'])
    page    = int(request.POST['page'])
    searchVal=str(request.POST['search']).strip()
    dRange  = str(request.POST['range']).split("-")
    try:
        date1   = datetime.datetime.strptime( dRange[0].strip(),'%b %d, %Y')
    except:
        date1   = datetime.datetime.strptime( dRange[0].strip(),'%B %d, %Y')
    try:
        date2   = datetime.datetime.strptime( dRange[1].strip()+" 23:59:59",'%b %d, %Y %H:%M:%S')
    except:
        date2   = datetime.datetime.strptime( dRange[1].strip()+" 23:59:59",'%B %d, %Y %H:%M:%S')    

    chartBYear  = date1.year
    chartBMonth = date1.month - 1
    chartBDay   = date1.day

    if filter == "attendance":
        dispType    = 'Attendance'
        chartTitle  = "Student Attendance"
        chartYTitle = "No. Attendees"
        chartSName  = "Attendees"
        dispList    = []
        chartData   = []

        chkDay      = date1
        while chkDay <= date2:
            strDay1     = chkDay.strftime("%m %d, %Y")
            chkDay2     = datetime.datetime.strptime( strDay1 + " 23:59:59",'%m %d, %Y %H:%M:%S')
            dayData     = 0
            
            if searchVal:
                attndLst= Attendance.objects.filter( userId__name__icontains=searchVal,
                                                     dateTime__range=(chkDay, chkDay2))
            else:
                attndLst= Attendance.objects.filter( dateTime__range=(chkDay, chkDay2) )
                
            for i in attndLst:
                dayData += int( i.DancerNumber )
                dispList.append(   i   )
            chartData.append(   dayData     )
            chkDay      += datetime.timedelta( days=1 )
    else:
        dispType    = 'Purchases'
        chartTitle  = "Student Classes Bought"
        chartYTitle = "Classes Bought"
        chartSName  = "Purchases"
        dispList    = []
        chartData   = []

        chkDay      = date1
        while chkDay <= date2:
            strDay1     = chkDay.strftime("%m %d, %Y")
            chkDay2     = datetime.datetime.strptime( strDay1 + " 23:59:59",'%m %d, %Y %H:%M:%S')
            dayData     = 0

            if searchVal:
                attndLst= Purchase.objects.filter( userId__name__icontains=searchVal,
                                                   date__range=(chkDay, chkDay2))
            else:
                attndLst= Purchase.objects.filter( date__range=(chkDay, chkDay2) )

            for i in attndLst:
                dayData += int( i.numberOfClasses )
                dispList.append(   i   )
            chartData.append(   dayData     )
            chkDay      += datetime.timedelta( days=1 )

    for item in dispList:
        item.name       = item.userId.name
        
    # Sort by
    if sort == "name":
        dispList.sort(key=operator.attrgetter("name"))
    else:
        if filter == "attendance":
            dispList.sort(key=operator.attrgetter("dateTime"))
        else:
            dispList.sort(key=operator.attrgetter("date"))

     
    #---------------------------------------------------------------------
    # Set the paginator object and get the current page data list
    #---------------------------------------------------------------------

    currPage        = page
    pgintObj        = getPgintObj(request,          dispList,
                                  currPage                              )

    dispList        = pgintObj.getDataList(                             )

    return render_to_response( 'historyInfo.html',
                               {'dispType':     dispType,
                                'dispList':     dispList,
                                'currPage':     currPage,
                                'paginator':    pgintObj,
                                'chartTitle':   chartTitle,
                                'chartYTitle':  chartYTitle,
                                'chartSName':   chartSName,
                                'chartData':    chartData,
                                'chartBYear':   chartBYear,
                                'chartBMonth':  chartBMonth,
                                'chartBDay':    chartBDay,
                                'sort':         sort,
                                'filter':       filter,
                                },
                               context_instance=RequestContext(request) )

#==============================================================================
##
## Gets all people with birthdays within given number of days
##
#==============================================================================

def birthdaysWithin(days):

    now = datetime.datetime.now()
    then = now + timedelta(days)

    # Build the list of month/day tuples.
    monthdays = [(now.month, now.day)]
    while now <= then:
        monthdays.append((now.month, now.day))
        now += timedelta(days=1)

    # Tranform each into queryset keyword args.
    monthdays = (dict(zip(("birthday__month", "birthday__day"), t))
                 for t in monthdays)


    # Compose the djano.db.models.Q objects together for a single query.
    query = reduce(operator.or_, (Q(**d) for d in monthdays))

    # Run the query.
    return User.objects.filter(query)

#==============================================================================
#
# "students": The student control page
#
#==============================================================================

def students( request, check=None):
    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)

    return render_to_response( 'students.html',
                               {'userName':	user.name,
                                'userType':	user.userType,
                                'sort':         "name",
                                'filter':       None,
                                'currPage':     1,
                                },
                               context_instance=RequestContext(request) )

#==============================================================================
#
# "studentList": The students page
#
#==============================================================================

def studentList( request ):

    # idle?
    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)

    # Get "get" values
    sort    = str(request.POST['sort'])
    filter  = str(request.POST['filter'])
    page    = int(request.POST['page'])
    search  = str(request.POST['search']).strip()
    dRange  = str(request.POST['range']).split("-")
    
    try:
        date1   = datetime.datetime.strptime( dRange[0].strip(),'%b %d, %Y')
    except:
        date1   = datetime.datetime.strptime( dRange[0].strip(),'%B %d, %Y')
    try:
        date2   = datetime.datetime.strptime( dRange[1].strip()+" 23:59:59",'%b %d, %Y %H:%M:%S')
    except:
        date2   = datetime.datetime.strptime( dRange[1].strip()+" 23:59:59",'%B %d, %Y %H:%M:%S')    

    # Get user list with filters (bday, waiver, balance)
    if filter == "bday":
        userList = birthdaysWithin(7)
    elif filter == "balance":
        userList = User.objects.filter(balance__lte=3)
    elif filter == "waiver":
        userList = User.objects.filter(waiverSigned=False)
    else:
        userList = User.objects.all()

    # Filter user list by search
    if search:
        userList = userList.filter(name__icontains=str(search))
    #print userList

    # Date range
    try:
        if date1.year != 2014 or date1.month != 1 or date1.day != 1:
            attendanceLst   = Attendance.objects.filter(userId__in = userList,
                                                dateTime__range=(date1, date2))
            usrAttenLst     = []
            for i in attendanceLst:
                usrId       = i.userId.userId
                if usrId in usrAttenLst: continue
                usrAttenLst.append( usrId )
            userList = userList.filter(userId__in=usrAttenLst)
    except:
        pass

    # Make userList a list so we can sort
    userList = list(userList)

    # Sort by
    if str(sort) == "name":
        userList.sort(key=operator.attrgetter("name"))
    elif str(sort) == "activity":
        userList.sort(key=operator.attrgetter("lastAccess"))
        userList.reverse()
    else:
        userList.sort(key=operator.attrgetter("balance"))

    # @WIP1@ These lines must be fixed
    now	= datetime.datetime.now()
    for user2 in userList:
	bday			= user2.birthday
	user2.hasBirthday	= (bday.year != 1970 and bday.month != 1 and bday.day != 1)
        lst7Day                 = now - datetime.timedelta(     days = 7    )
        user2.showBirthday	= (bday > lst7Day)	# check Bday within 7 days
        
	user2.recent		= ((now - user2.lastAccess).total_seconds() < 2*24*3600)

    # @WIP1@ These lines must be fixed
    nStudents	= len( userList )
    currPage	= 4
    nPages	= 4
 #   url		= request.get_full_path()[:-1]
    #url     = str(sortBy) + "/" + str(page) + "/" + str(range)


    #---------------------------------------------------------------------
    # Set the paginator object and get the current page data list
    #---------------------------------------------------------------------
    currPage        = page
    pgintObj        = getPgintObj(request,          userList,
                                  currPage                              )

    dataLst         = pgintObj.getDataList(                             )

    return render_to_response( 'studentsInfo.html',
                               {'userName':	user.name,
                                'userType':	user.userType,
                                'userList':	dataLst,
				'nStudents':	nStudents,
				'currPage':	currPage,
                                'paginator':    pgintObj,
				'nPages':	nPages,
				#'url':		url,
                                #'addUserForm':  addUserForm,
                                'sort':         sort,
                                'filter':       filter,
                                },
                               context_instance=RequestContext(request) )


###############################################################################
##
## "addStudent":  Add a new student; using drop down
##
###############################################################################

def addStudent( request, check = None ):
    
    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)

    # Add new user validation and forms
    if check is not None:
        form = AddUserForm(request.GET.copy())
        if form.is_valid():
            user2 = form.save()
            url     = '/students/' # + str(sort) + "/" + str(page) + "/" + str(range) + "/"
            json = util.JsonLoad(               url             )
        else:
            json = util.JsonFormError(form)
        return HttpResponse(json,
                            mimetype='application/json')

    # Make form
    addUserForm = AddUserForm()
   
    return render_to_response(  'dropDownForm.html',
                                {'form':        addUserForm,
                                #'formName':     'addClient',
                                #'actionUrl':    addDrpdnUrl,
                                },
                                context_instance=RequestContext(request))

###############################################################################
##
## "exportStudents": Create a CSV file which contains the users data
##
###############################################################################

def exportStudents( request ):
    today       = datetime.datetime.now(                                )
    response    = HttpResponse(                 mimetype = 'text/csv'   )
    fileName    = "students_%s.csv" %today.strftime(      '%y%m%d%H%M%S'  )
    response['Content-Disposition'] = 'attachment; filename=%s' %fileName
    
    writer      = csv.writer(                   response                )
    writer.writerow(['Name', 'E-mail', 'Address',
                     'Phone', 'Birthday', 'Balance',
                     'Waiver', 'Admin',
                     ])

    for i in User.objects.all():
        address = i.address.replace(         "\r\n",     " "     )

        writer.writerow([i.name, i.email, address, i.phone,
                         str(i.birthday.date()), i.balance,
                         i.waiverSigned, i.userType
                        ])
                         
    return response

###############################################################################
##
## "importStudents": Import a CSV file which contains the users data
##
###############################################################################

def importStudents( request ):
    if request.POST:
        fileName    = request.FILES.copy()['fileName']
        fileData    = fileName.read().split(        '\n'                )

        #----------------------------------------------------------------
        # Check the file data to be correct and save it
        #----------------------------------------------------------------

        fileHeader  = fileData[0].replace(          "\r",       ""      )
        header      = "Name,E-mail,Address,Phone,Birthday,Balance,Waiver,Admin"
        
        if fileHeader != header: return
        
        #----------------------------------------------------------------
        # Save imported file data into data base
        #----------------------------------------------------------------
                    
        for row in fileData[1:]:
            rowData = row.replace("\r", ""  )
            studentData = rowData.split(    ',' )
            if len( studentData ) != 8 : continue

            email = studentData[1]
                        
            try:
                user    = User.objects.get( email__exact = email )
            except User.DoesNotExist:
                user    = None

            if user:
                updateStudent( studentData, update = True)
            else:
                updateStudent(     studentData   )
                            
        
        return HttpResponseRedirect(    "/students/"        )

###############################################################################
##
## "updateStudent": Update student table
##
###############################################################################

def updateStudent( data, update = False ):
    
    if update:
        #----------------------------------------------------------------
        # Update student data
        #----------------------------------------------------------------

        user                    = User.objects.get( email__exact = data[1] )
        user.name               = data[0]
        user.address            = data[2]
        user.phone              = data[3]
        user.birthday           = datetime.datetime.strptime(data[4],'%Y-%m-%d')
        user.balance            = int(data[5])
        user.waiverSigned       = True if data[6] == "True" else False
        user.userType           = int(data[7])
        user.save()
        return 

    #--------------------------------------------------------------------
    # Save New student
    #--------------------------------------------------------------------

    today                   = datetime.datetime.today()
    user                    = User()
    user.name               = data[0]
    user.email              = data[1].lower()
    user.password           = util.encryptPass(str(random.random()))
    user.address            = data[2].lower()
    user.phone              = data[3]
    user.lastAccess         = today
    user.balance            = int(data[5])
    user.waiverSigned       = True if data[6] == "True" else False
    user.facebook           = False
    user.notes              = ""
    user.dateCreated        = today
    user.userType           = int(data[7])
    user.idleTime           = 10
    user.birthday           = datetime.datetime.strptime(data[4],'%Y-%m-%d')
    user.birthdayAssigned   = False
    user.save()

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
# "edit": A page in which Ula can edit a student's information
#
#==============================================================================

def editStudent(request, userId, check=None):

    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)

##    try:
##        userId = request.GET['id']
##    except:
##        return HttpResponseRedirect('/students/name0/1/all/')
##    try:
##        url = request.GET['url']
##    except:
##        url = 'name0/1/all/'

    if check is not None:
        data    = request.GET.copy()
        form    = EditUserForm(data)

        if form.is_valid():
            form.save()
            json = util.JsonLoad( closeSecId = "editSudent" )
        else:
            json = util.JsonFormError(form)
        return HttpResponse(json,
                            mimetype='application/json')

    user2 = User.objects.get(userId = userId )

    if str( user2.birthday.date() ) == "1970-01-01":
        birthVal = ""
    else:
        birthVal = user2.birthday.date()
        
    editUserForm = EditUserForm(initial = {'userId':    user2.userId,
                                           'name':      user2.name,
                                           'email':     user2.email,
                                           'address':   user2.address,
                                           'phone':     user2.phone,
                                           'birth':     birthVal,
                                           'balance':   user2.balance,
                                           'notes':     user2.notes,
                                           'waiver':    user2.waiverSigned
                                           }
                                )

##    return render_to_response('editStudent.html',
##                              {'userId': user2.userId,
##                               'userName': user.name,
##                               'userType': user.userType,
##                               'url': url,
##                               'editUserForm': editUserForm,
##                               },
##                              context_instance=RequestContext(request))
##

    return render_to_response(  'editStudentForm.html',
                                {'form':        editUserForm,
                                 'userType':    user2.userType,
                                 'title':       'Edit Student',
                                 'actionUrl':   "/students/edit/%d/" %int( userId ),
                                 'submitVal':   'Save'
                                },
                                context_instance=RequestContext(request))

#==============================================================================
#
# "purchaseStudent": A purchase student page
#
#==============================================================================

def purchaseStudent(request, userId, check=None):

    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)

    if check is not None:
        data    = request.GET.copy()
        form    = PurchaseUserForm(data)

        if form.is_valid():
            form.save()
            json = util.JsonLoad( closeSecId = "purchaseStudent" )
        else:
            json = util.JsonFormError(form)
        return HttpResponse(json,
                            mimetype='application/json')

    user2 = User.objects.get(userId = userId )

        
    purchaseUserForm = PurchaseUserForm( initial = {'userId':    user2.userId })
    return render_to_response(  'purchaseStudenttForm.html',
                                {'form':        purchaseUserForm,
                                 'title':       'Add classes to "%s"' %user2.name,
                                 'actionUrl':   "/students/purchase/%d/" %int( userId ),
                                 'submitVal':   'Save'
                                },
                                context_instance=RequestContext(request))

#==============================================================================
#
# "rcntActivityStudent": Student recent activity page
#
#==============================================================================

def rcntActivityStudent(request, userId ):

    user, errUrl = GetValidUser(request)
    if errUrl:
        return HttpResponseRedirect(errUrl)

    user2 = User.objects.get(userId = userId )

    recentLst = usrRcntChanges(  user2 )
    return render_to_response(  'recentActivity.html',
                                {'recentLst':        recentLst,
                                 'title':       '"%s" recent activity' %user2.name,
                                },
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
    return render_to_response(  'forgotPassword.html',
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
# "myprofile": Allows students to change their information
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

    if str( user.birthday.date() ) == "1970-01-01":
        birthVal = ""
    else:
        birthVal = user.birthday.date()

    form    = MyprofileForm(initial = {'userId':    user.userId,
                                       'name':      user.name,
                                       'email':     user.email,
                                       'birth':     birthVal,
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

###############################################################################
##
## "getPgintObj": Create paginator object and return it.
##
###############################################################################

def getPgintObj( request, usrLst, currPage = 1, padding = 3 ):
    
 #   currUsr     = getCurrUser(                  request                 )
    pgintObj    = paginator.PaginatorObj(       usrLst,
                                                1 * 4,
                                                currPage,
                                                padding                 )
    return pgintObj

###############################################################################
##
## "usrRcntChanges":
##
###############################################################################

def usrRcntChanges( user ):

    now	= datetime.datetime.now()
    rcnChgs     = RecentChange.objects.filter(userId = user.userId)

    retVal      = []
    for chg in rcnChgs:
        if ((now - chg.dateTime).total_seconds() < 2*24*3600):
            retVal.append( [chg.change, chg.value, chg.dateTime.strftime('%Y-%m-%d') ] )

        else:
            chg.delete()

    return retVal

