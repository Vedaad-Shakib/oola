###############################################################################
## Copyright (c) 2013-2014 Bogt, Inc.
## All rights reserved.
## This source code is confidential and may not be disclosed.
###############################################################################

###############################################################################
##
## "models.py";  Data base definition
##
###############################################################################

from django.db import models

###############################################################################
##
## "User": user definition
##
###############################################################################

class User(models.Model):
    userId      = models.AutoField(     db_column       = 'user_id',
                                        primary_key     = True                )
    name        = models.CharField(     db_column       = 'full_name',
                                        max_length      = 128                 )
    email       = models.CharField(     db_column       = 'email',
                                        max_length      = 128                 )
    password    = models.CharField(     db_column       = 'password',
                                        max_length      = 128                 )
    dateCreated = models.DateTimeField( db_column       = 'date_created'      )
    lastAccess  = models.DateTimeField( db_column       = 'last_access'       )
    balance     = models.IntegerField(  db_column       = 'balance'           )
    address     = models.CharField(     db_column       = 'address',
                                        max_length      = 256                 )
    phone       = models.CharField(     db_column       = 'phone',
                                        max_length      = 16                  )
    birthday    = models.DateTimeField( db_column       = 'birthday'          )
    birthdayAssigned = models.BooleanField(db_column   	= 'birthday_assigned' )
    waiverSigned= models.BooleanField(  db_column       = 'waiver_signed'     )
    facebook    = models.BooleanField(  db_column       = 'facebook_connected')
    notes       = models.CharField(     db_column       = 'notes',
                                        max_length      = 256                 )
    userType    = models.IntegerField(  db_column       = 'user_type'         )
    idleTime    = models.IntegerField(  db_column       = 'idle_time'         )
    autoLogin   = models.CharField(     db_column       = 'auto_login',
                                        max_length      = 1		      )

##############################################################################
##
## "Purchase": Class purchases
##
##############################################################################

class Purchase(models.Model):
     purchaseId      = models.AutoField(     db_column   = 'purchase_id',
                                             primary_key = True               )
     userId          = models.ForeignKey(    User,
                                             db_column   = 'user_id'          )
     date            = models.DateTimeField( db_column   = 'date_of_purchase' )
     amount          = models.IntegerField(  db_column   = 'amount'           )
     numberOfClasses = models.IntegerField(  db_column   = 'number_of_classes')
     discount        = models.IntegerField(  db_column   = 'discount'         )

##############################################################################
##
## "Attendance": Class attendance
##
##############################################################################

class Attendance(models.Model):
     attendanceId    = models.AutoField(     db_column   = 'attendance_id',
                                             primary_key = True               )
     userId          = models.ForeignKey(    User,
                                             db_column   = 'user_id'          )
     dateTime        = models.DateTimeField( db_column   = 'date_and_time'    )
     DancerNumber    = models.IntegerField(  db_column   = 'number_of_dancers')

##############################################################################
##
## "Tag": Tag users
##
##############################################################################

class Tag(models.Model):
    tagId           = models.AutoField(     db_column   = 'tag_id',
                                            primary_key = True               )
    userId          = models.ForeignKey(    User,
                                            db_column   = 'user_id'          )
    tagName         = models.CharField(     db_column   = 'tag_name',
                                            max_length  = 32                 )

##############################################################################
##
## "ForgotPassword": Forgotten Password Keys
##
##############################################################################

class RandomPassword(models.Model):
    randomPasswordId = models.AutoField(     db_column    = 'random_password_id',
                                             primary_key  = True	   )
    userId           = models.ForeignKey(    User,
                                             db_column    = 'user_id'      )
    expiration       = models.DateTimeField( db_column    = 'expiration'   )
    passwordKey      = models.CharField(     db_column    = 'password_key',
                                             max_length   = '16'           )


###############################################################################
##
## "ForgotPassword": Forgot Password definition
##
###############################################################################

class ForgotPassword(models.Model):
    forgotPasswdId  = models.AutoField(	db_column	= 'forgotPasswd_id',
					primary_key	= True		)

    userId          = models.ForeignKey(User,
                                        db_column	= 'user_id'     )        

    forgotCode	    = models.CharField(	db_column	= 'forgot_code',
    					max_length	= 32		)

    forgotTime      = models.DateTimeField(db_column	= 'forgot_time'	)
    
    active	    = models.CharField(	db_column	= 'active',
    					max_length	= 1		)

