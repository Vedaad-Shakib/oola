###############################################################################
## Copyright (c) 2013-2014 Bogt, Inc.
## All rights reserved.
## This source code is confidential and may not be disclosed.
###############################################################################

###############################################################################
##
## "forms.py":
##
###############################################################################

from	django import forms
from	django.forms.util import ValidationError
import  sys
import  datetime
import  util
import	random
from    forms_util import *
from    models import *

###############################################################################
##
## "SignupForm": Form for signup page
##
###############################################################################

class SignupForm(forms.Form):
    name    	= FieldText(            label           = '* Full name',
                                        max_length      = 128,
                                        placeholder     = 'Enter full name'         )

    email       = FieldEmail(           label           = '* E-mail',
                                        max_length      = 128,
					placeholder     = 'Enter e-mail address'    )

    password    = FieldPassword(        label           = '* Password',
                                        max_length      = 128,
					placeholder     = 'Enter password'          )

    password2   = FieldPassword2(       label           = '* Confirm password',
                                        max_length      = 128,
					placeholder     = 'Enter password again'    )

#------------------------------------------------------------------------------
# Check for email address
#------------------------------------------------------------------------------

    def clean_email( self ):
        email           = self.data['email'].lower()
        try:
            user        = User.objects.get( email__exact = email )
            raise forms.ValidationError( 'Email address already exists' )
        except User.DoesNotExist:
            pass

###------------------------------------------------------------------------------
### Check if password and password2 match
###------------------------------------------------------------------------------
##
##    def clean_password( self ):
##        password           = self.data['password']
##        password2          = self.data['password2']
##        if password != password2:
##            raise forms.ValidationError( 'Passwords do not match' )

#------------------------------------------------------------------------------
# Save the information in the data base
#------------------------------------------------------------------------------

    def save( self ):
        today                   = datetime.datetime.today()
        userId                  = -1
        user                    = User()
        user.name               = self.data['name'].title()
        user.email              = self.data['email'].lower()
        user.password           = util.encryptPass(self.data['password'])
        user.address           	= ""
        user.phone              = ""
        user.lastAccess         = today
        user.balance            = 0
        user.waiverSigned       = False
        user.facebook           = False
        user.notes              = ""
        user.dateCreated        = today
        user.userType           = 0
        user.idleTime           = 10
        user.birthday           = datetime.date(1970, 1, 1)
        user.birthdayAssigned   = False
        user.save()
        return user

###############################################################################
##
## SigninForm: Form for signin page
##
###############################################################################

class SigninForm(forms.Form):
    email      = FieldEmail(   		label      	= '* E-mail',
                                	max_length 	= 128,
					placeholder	= 'Enter e-mail address' )
    password   = FieldPassword( 	label      	= '* Password',
                                	max_length 	= 128,
					placeholder	= 'Enter password' )

#------------------------------------------------------------------------------
# Check for email address
#------------------------------------------------------------------------------

    def clean_email( self ):
        email		= self.data['email'].lower()
        try:
            user	= User.objects.get( email = email )
        except User.DoesNotExist:
            raise ValidationError( 'Invalid email address')

#------------------------------------------------------------------------------
# Check for password
#------------------------------------------------------------------------------

    def clean_password( self ):
	email		= self.data['email'].lower()
	try:
	    user	= User.objects.get( email__exact = email )
	except User.DoesNotExist:
	    return
	try:
	    password	= self.data['password']
	    algo,salt,hsh = user.password.split('$')
	    if util.encryptPass(password,algo,salt) != user.password:
		raise ValidationError( 'Invalid password' )
	except User.DoesNotExist:
	    raise ValidationError( 'Invalid email address' )


###############################################################################
##
## SearchForm: Form for admin landingpage search function
##
###############################################################################

class SearchForm(forms.Form):
    search     = FieldText(     	label      	= 'Search',
                                	max_length	= 128,
                                	required	= True		)

###############################################################################
##
## ClassName: Class signin form
##
###############################################################################

class ClassName(forms.Form):
    name	= FieldText(		label		= "Name"	)

#------------------------------------------------------------------------------
# Check for name
#------------------------------------------------------------------------------

    def clean_name(self):
	name		= self.data['name']
	try:
	    user	= User.objects.get(name=name)
	except User.DoesNotExist:
	    raise ValidationError('User does not exist')

###############################################################################
##
## ClassSignup: Class signup form
##
###############################################################################

class ClassSignup(forms.Form):
    name    	= FieldText(            label           = '* Full name',
					extraClass	= "class-signin-input",
                                        max_length      = 128,
                                        placeholder     = 'Enter full name',
                                        attrs           = {"onkeypress": "resetActivityTimer()"})

    email       = FieldEmail(           label           = '* E-mail',
					extraClass	= "class-signin-input",
                                        max_length      = 128,
					placeholder     = 'Enter e-mail address',
                                        attrs           = {"onkeypress": "resetActivityTimer()"})

    balance	= FieldInteger(		label		= 'Number of Classes Left',
					extraClass	= "class-signin-input",
					placeholder     = 'Enter # of classes, excluding today',
                                        attrs           = {"onkeypress": "resetActivityTimer()"})

#------------------------------------------------------------------------------
# Check for email
#------------------------------------------------------------------------------

    def clean_email(self):
        email           = self.data['email'].lower()
        try:
            user        = User.objects.get( email__exact = email )
            raise forms.ValidationError( 'Email address already exists' )
        except User.DoesNotExist:
            pass

#------------------------------------------------------------------------------
# Save the form
#------------------------------------------------------------------------------

    def save(self):
	today			= datetime.datetime.today()
	userId			= -1
	user			= User()
        user.name               = self.data['name'].title()
        user.email              = self.data['email'].lower()
        user.password           = util.encryptPass(str(random.random()))
	user.address		= ""
	user.phone		= ""
	user.lastAccess		= today
	try:
            user.balance       	= int(str(self.data['balance'])) 
        except:
            user.balance        = 0
        user.waiverSigned       = False
	user.facebook		= False
	user.notes		= ""
	user.dateCreated	= today
	user.userType		= 0
	user.idleTime		= 10
	user.birthday		= datetime.date(1970, 1, 1)
	user.birthdayAssigned	= False
	user.save()
	return user

###############################################################################
##
## "ForgotPasswordForm":  Form for forgot password page
##
###############################################################################

class ForgotPasswordForm(forms.Form):

    email	= FieldEmail(		label		= '* e-mail',
    					max_length	= 128,
                                        placeholder     = 'Enter e-mail address')

#------------------------------------------------------------------------------
# Check for email address
#------------------------------------------------------------------------------

    def clean_email( self ):
	email		= self.data['email'].lower()
	try:
	    user	= User.objects.get( email__exact = email )
	except User.DoesNotExist:
	    raise ValidationError( 'Invalid email address' )

#------------------------------------------------------------------------------
# Save the information in the data base
#------------------------------------------------------------------------------

    def save( self ):
        email	                    = self.data['email'].lower()
        user	                    = User.objects.get(email__exact = email)
	forgotPassword		    = ForgotPassword(                   )
	forgotPassword.userId       = user
	forgotPassword.forgotCode   = util.randomStr(   32              )
	forgotPassword.forgotTime   = datetime.datetime.today(          )
	forgotPassword.active	    = 'Y'
	forgotPassword.save(                                            )

	#----------------------------------------------------------------------
	# Set the recent change
	#----------------------------------------------------------------------

        user.lastAccess             = datetime.datetime.now(            )
        user.save()
        
        rcntChg                     = RecentChange(                     )
        rcntChg.userId              = user
        rcntChg.change              = "Forgot Password"
        rcntChg.value               = "Forgot code sent"
        rcntChg.dateTime            = datetime.datetime.now(            )
        rcntChg.save(                                                   )
	
	return forgotPassword

###############################################################################
##
## "ChangePasswordForm":  Form for change password page
##
###############################################################################

class ChangePasswordForm(forms.Form):
    password    = FieldPassword(        label           = '* New Password',
                                        max_length      = 128,
					placeholder     = 'Enter new password'          )

    password2   = FieldPassword2(       label           = '* Confirm password',
                                        max_length      = 128,
					placeholder     = 'Enter new password again'    )

#------------------------------------------------------------------------------
# Save the information in the data base
#------------------------------------------------------------------------------

    def save( self ):
	today			= datetime.datetime.today()
	forgotCode              = self.forgotCode
        forgtPasswd             = ForgotPassword.objects.get(
                                        forgotCode__exact = forgotCode)
	user	                = forgtPasswd.userId
	userId			= user.userId
	user.password		= util.encryptPass(self.data['password'])
	user.updatedOn		= today
	user.updatedBy		= userId
	user.lastAccess         = datetime.datetime.now(            )

	user.save(                                                              )

	#----------------------------------------------------------------------
	# Set the recent change
	#----------------------------------------------------------------------

        rcntChg                     = RecentChange(                     )
        rcntChg.userId              = user
        rcntChg.change              = "Password"
        rcntChg.value               = "Password changed"
        rcntChg.dateTime            = datetime.datetime.now(            )
        rcntChg.save(                                                   )

	return user

###############################################################################
##
## "MyprofileForm":  Form for MyProfile page
##
###############################################################################

class MyprofileForm(forms.Form):

    userId      = FieldInteger(         label           = 'User Id',
                                        visible         = False             )

    name    	= FieldText(            label           = '* Full name',
                                        max_length      = 128,
                                        placeholder     = 'Enter full name' )

    email       = FieldEmail(           label           = '* E-mail',
                                        max_length      = 128,
					placeholder     = 'Enter e-mail address'    )

    birth    	= FieldDate(            label           = 'Birthday',
                                        placeholder     = 'Enter birthday: yyyy-mm-dd',
                                        attrs           = {"id":"datePik"})

    phone       = FieldPhone(           label           = 'Phone',
                                        placeholder     = 'Enter phone number',
                                        max_length      = 16                )

    address     = FieldTextarea(        label           = 'Address',
                                        placeholder     = 'Enter address',
                                        attrs           = { "rows": "2"}        )

    idleTime    = FieldInteger(         label           = '* Idle Time',
                                        placeholder     = 'Enter idle time'     )

#------------------------------------------------------------------------------
# Check for email address
#------------------------------------------------------------------------------

    def clean_email( self ):
	userId		= self.data['userId']
	email		= self.data['email'].lower()
	try:
	    user	= User.objects.get( email__exact = email )
	    if int( user.userId ) != int( userId ):
		raise ValidationError( 'Email address already exists' )
	except User.DoesNotExist:
	    pass

#------------------------------------------------------------------------------
# Save the information in the data base
#------------------------------------------------------------------------------

    def save( self ):
	today			= datetime.datetime.today()
	userId			= int( self.data['userId'] )
	user			= User.objects.get( userId = userId )

	lstVals                 = [user.name, user.email, user.birthday.date(),
                                   user.address, user.phone, user.idleTime,
                                   user.userType]
                                   
	user.name	        = self.data['name'].strip().title()
        user.email		= self.data['email'].strip().lower()
        birth                   = self.data['birth'].strip()
        if birth:
            birth               = birth.replace(".","-")
            birth               = birth.replace("/","-")
            user.birthday       = datetime.datetime.strptime(birth,'%Y-%m-%d')

	user.address	        = self.data['address'].strip()
        user.phone		= self.data['phone'].strip()
	user.idleTime           = int( self.data['idleTime'].strip() )

	if self.data.has_key( "adminType" ):
            if self.data['adminType'] == "Y":
                user.userType   = 1
            else:
                user.userType   = 0

	user.updatedOn		= today
	user.updatedBy		= userId
	user.lastAccess         = datetime.datetime.now(            )

	user.save()

	#----------------------------------------------------------------------
	# Set the recent change
	#----------------------------------------------------------------------

	newVals                 = [user.name, user.email, user.birthday.date(),
                                   user.address, user.phone, user.idleTime,
                                   user.userType]

        for i in xrange( len(newVals) ):
            if newVals[i] != lstVals[i]:
                rcntChg         = RecentChange(                     )
                rcntChg.userId  = user
                
                if i == 0:
                    rcntChg.change= "Name"
                if i == 1:
                    rcntChg.change= "E-mail"
                if i == 2:
                    rcntChg.change= "Birthday"
                if i == 3:
                    rcntChg.change= "Address"
                if i == 4:
                    rcntChg.change= "Phone"
                if i == 5:
                    rcntChg.change= "Idle Time"
                if i == 6:
                    rcntChg.change= "Type"
                
                rcntChg.value   = str( newVals[i] )
                rcntChg.dateTime= datetime.datetime.now(            )
                rcntChg.save(                                       )

	return user

###############################################################################
##
## AddUserForm: Add a new user
##
###############################################################################

class AddUserForm(forms.Form):
    name        = FieldText(            label           = '* Full name',
                                        max_length      = 128,
                                        placeholder     = 'Enter full name'         )

    email       = FieldEmail(           label           = '* E-mail',
                                        max_length      = 128,
                                        placeholder     = 'Enter e-mail address'    )

    address     = FieldTextarea(        label           = 'Address',
                                        placeholder     = 'Enter address',
                                        attrs           = { "rows": "2"}            )

    phone       = FieldPhone(           label           = 'Phone',
                                        max_length      = 128,
                                        placeholder     = 'Enter phone number'      )

    birth       = FieldDate(            label           = 'Birthday',
                                        placeholder     = 'Enter birthday: yyyy-mm-dd',
                                        attrs           = {"id":"datePikAdd"}          )
    balance     = FieldInteger(         label           = '* Number of classes left',
                                        placeholder     = 'Enter balance'           )
    waiver      = FieldCheckBox(        label           = 'Waiver'                  )
    admin       = FieldCheckBox(        label           = 'Admin'                   )


#------------------------------------------------------------------------------
# Check for email address
#------------------------------------------------------------------------------

    def clean_email( self ):
        email           = self.data['email'].lower()
        try:
            user        = User.objects.get( email__exact = email )
            raise forms.ValidationError( 'Email address already exists' )
        except User.DoesNotExist:
            pass

#------------------------------------------------------------------------------
# Save the information in the data base
#------------------------------------------------------------------------------

    def save( self ):
        today                   = datetime.datetime.today()
        user                    = User()
        user.name               = self.data['name'].title()
        user.email              = self.data['email'].lower()
        user.password           = util.encryptPass(str(random.random()))
        user.address            = self.data['address'].lower()
        user.phone              = self.data['phone']
        user.lastAccess         = today
        user.balance            = int(str(self.data['balance']))
        user.waiverSigned       = True if self.data.has_key("waiver")  else False
        user.facebook           = False
        user.notes              = ""
        user.dateCreated        = today
        user.userType           = 1 if self.data.has_key("admin") else 0
        user.idleTime           = 10
        birth                   = self.data['birth'].strip()
        if birth:
            birth               = birth.replace(".","-")
            birth               = birth.replace("/","-")
            user.birthday       = datetime.datetime.strptime(birth,'%Y-%m-%d')
        else:
            user.birthday       = datetime.date(1970, 1, 1)

        user.birthdayAssigned   = False
        user.save()

        #------------------------------------------------------------------------
        # If the balance is  non-zero, then record it in "Purchase" table
        #------------------------------------------------------------------------

        if user.balance > 0:
            purchase = Purchase()
            purchase.userId = user
            purchase.amount = user.balance  #???
            purchase.discount = 0 #???
            purchase.numberOfClasses = user.balance
            purchase.date = datetime.datetime.now()
            purchase.save()

        return user

###############################################################################
##
## EditUserForm: A form for editing students
##
###############################################################################

class EditUserForm(forms.Form):
    userId      = FieldInteger(         label           = 'User Id',
                                        visible         = False             )

    name        = FieldText(            label           = '* Full name',
                                        max_length      = 128,
                                        placeholder     = 'Enter full name')

    email       = FieldEmail(           label           = '* E-mail',
                                        max_length      = 128,
                                        placeholder     = 'Enter e-mail address')

    address     = FieldTextarea(        label           = 'Address',
                                        placeholder     = 'Enter address',
                                        attrs           = {"rows": 2})

    phone       = FieldPhone(           label           = 'Phone',
                                        max_length      = 128,
                                        placeholder     = 'Enter phone number')

    birth    	= FieldDate(            label           = 'Birthday',
                                        placeholder     = 'Enter birthday: yyyy-mm-dd',
                                        attrs           = {"id":"datePik"})

    balance     = FieldNumber(          label           = '* Number of classes left',
                                        placeholder     = 'Enter balance')

    notes       = FieldTextarea(        label           = 'Notes',
                                        max_length      = 1024,
                                        placeholder     = 'Enter notes',
                                        attrs           = { "rows": "2"})

    waiver      = FieldCheckBox(        label           = 'Waiver'      )
    
#------------------------------------------------------------------------------
# Check for email address
#------------------------------------------------------------------------------

    def clean_email( self ):
        email           = self.data['email'].lower()
        userId          = int( self.data['userId'] )
        try:
            user        = User.objects.get( email__exact = email )
            if int( user.userId ) == userId:pass
            else:
                raise forms.ValidationError( 'Email address already exists' )
        except User.DoesNotExist:
            pass

#------------------------------------------------------------------------------
# Save the information in the data base
#------------------------------------------------------------------------------

    def save( self ):
        userId = int(self.data['userId'])
        user = User.objects.get(userId = userId)

	lstVals                 = [user.name, user.email, user.birthday.date(),
                                   user.address, user.phone, user.balance, user.notes,
                                   user.userType]

        user.name               = self.data['name'].title()
        user.email              = self.data['email'].lower()
        user.address            = self.data['address'].lower()
        user.phone              = self.data['phone']

        birth                   = self.data['birth'].strip()
        if birth:
            birth               = birth.replace(".","-")
            birth               = birth.replace("/","-")
            user.birthday       = datetime.datetime.strptime(birth,'%Y-%m-%d')

        user.balance            = int(self.data['balance'])
        user.waiverSigned       = True if self.data.has_key("waiver")  else False
        user.notes              = self.data['notes']
 #       user.userType           = 1 if self.data.has_key("admin") else 0
        if self.data.has_key( "adminType" ):
            if self.data['adminType'] == "Y":
                user.userType   = 1
            else:
                user.userType   = 0

##        if self.data.has_key( "waiver" ):
##            if self.data['waiver'] == "Y":
##                user.waiverSigned   = True
##            else:
##                user.waiverSigned   = False

	user.lastAccess         = datetime.datetime.now(            )
	user.save()

	#----------------------------------------------------------------------
	# Set the recent change
	#----------------------------------------------------------------------

	newVals                 = [user.name, user.email, user.birthday.date(),
                                   user.address, user.phone, user.balance, user.notes,
                                   user.userType]

        for i in xrange( len(newVals) ):
            if newVals[i] != lstVals[i]:
                rcntChg         = RecentChange(                     )
                rcntChg.userId  = user
                
                if i == 0:
                    rcntChg.change= "Name"
                if i == 1:
                    rcntChg.change= "E-mail"
                if i == 2:
                    rcntChg.change= "Birthday"
                if i == 3:
                    rcntChg.change= "Address"
                if i == 4:
                    rcntChg.change= "Phone"
                if i == 5:
                    rcntChg.change= "Balance"
                if i == 6:
                    rcntChg.change= "Notes"
                if i == 7:
                    rcntChg.change= "Type"
                
                rcntChg.value   = str( newVals[i] )
                rcntChg.dateTime= datetime.datetime.now(            )
                rcntChg.save(                                       )

        #------------------------------------------------------------------------
        # If the balance is increased, then record the change in "Purchase" table
        #------------------------------------------------------------------------

        if newVals[5] > lstVals[5]:
            try:
                purchase = Purchase.objects.get( userId = user )
            except:
                purchase = Purchase()
                purchase.userId = user
                purchase.amount = int( newVals[5] )  #???
                purchase.discount = 0 #???
                
            purchase.numberOfClasses = int( newVals[5] )
            purchase.date = datetime.datetime.now()
            purchase.save()

        return user

###############################################################################
##
## "ImportUsersForm":  Form for import users data
##
###############################################################################

class ImportUsersForm(forms.Form):
    
    fileName    = FieldFileInput(   label = 'File name',
                                    required= True,
                                    placeholder="File name",
                                    attrs = { "extension":    "csv" }   )

###############################################################################
##
## "PurchaseUserForm":  Form for purchase user
##
###############################################################################

class PurchaseUserForm(forms.Form):
    userId      = FieldInteger(         label           = 'User Id',
                                        visible         = False             )

    
    newClasses    = FieldInteger(       label           = '* New Classes',
                                        placeholder     = 'Enter new classes'     )
    
#------------------------------------------------------------------------------
# Check for email address
#------------------------------------------------------------------------------

    def clean_newClasses( self ):
        newClasses      = int( self.data['newClasses'] )
        if newClasses < 1:
            raise forms.ValidationError( 'Please enter a positive integer number' )
            
#------------------------------------------------------------------------------
# Save the information in the data base
#------------------------------------------------------------------------------

    def save( self ):
        userId = int(self.data['userId'])
        user = User.objects.get(userId = userId)

        user.balance    += int( self.data['newClasses'] )

	user.lastAccess = datetime.datetime.now(            )
	user.save()

        #------------------------------------------------------------------------
        # Record it in "Purchase" table
        #------------------------------------------------------------------------

        try:
            purchase = Purchase.objects.get( userId = user )
        except:
            purchase = Purchase()
            purchase.userId = user
            purchase.amount = user.balance  #???
            purchase.discount = 0 #???
                
        purchase.numberOfClasses = user.balance
        purchase.date = datetime.datetime.now()
        purchase.save()

	#----------------------------------------------------------------------
	# Set the recent change
	#----------------------------------------------------------------------

        rcntChg         = RecentChange(                     )
        rcntChg.userId  = user
        rcntChg.change= "Balance"
        rcntChg.value   = str( user.balance )
        rcntChg.dateTime= datetime.datetime.now(            )
        rcntChg.save(                                       )

        return user

