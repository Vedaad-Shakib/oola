from    django.conf         import settings
from    django.conf.urls    import patterns, url

#-------------------------------------------------------------------------
# Define urlpatterns
#-------------------------------------------------------------------------

urlpatterns = patterns('ula.views',
    url( r'^home/?$',					'mainPage'	),
    url( r'^admin/?$',					'mainPage'	),

    url( r'^mainPage/(?P<checkSignup>checkSignup)/?$',	'mainPage'      ),
    url( r'^mainPage/(?P<checkSignin>checkSignin)/?$',	'mainPage'      ),   
    url( r'^signout/?$', 				'signout'	),
    url( r'^signout/(?P<check>check)/?$',		'signout'	),

    url( r'^signin/?$', 				'signin'	),
    url( r'^signin/(?P<check>check)/?$',		'signin'	),
    
    url( r'^/?$',					'classPage'	), 
    url( r'^class/?$',					'classPage'	),

    url( r'^class/checkin/?$',				'classCheckin'	),
    url( r'^class/checkin/(?P<userId>[0-9]+)/?$',	'classCheckin'	),
    url( r'^class/checkin/checkRecent/?$',		'classCheckRecent'),
                       
    url( r'^class/signup/?$',				'classSignup'	),
    url( r'^class/signup/(?P<check>check)/?$',          'classSignup'   ),
    url( r'^class/cancel/(?P<totalGuests>[0-9]*)/(?P<userId>[0-9]+)/(?P<attendanceId>[0-9]*)/?$', 'classCancel'),
    url( r'^class/save/(?P<guests>[0-9]*)/(?P<userId>[0-9]+)/(?P<oldCount>[0-9]*)/?$', 'classSave'),

    url( r'^students/?$',				'students'	),
    url( r'^students/(?P<check>check)/?$',              'students'      ),

    url( r'^students/edit/?$',      			'edit'          ),

    url( r'^clearance/?$',				'clearance'	),

    url( r'^myprofile/?$',				'myprofile'	),
    url( r'^myprofile/(?P<check>check)/?$',		'myprofile'	),

    url( r'^forgotpassword/?$',				'forgotPassword'),
    url( r'^forgotpassword/(?P<check>check)/?$',	'forgotPassword' ),
    url( r'^forgotPdSentEmail/?$',			'forgotPdSentEmail'),

    url( r'^forgotCode/(?P<forgotCode>([a-z]|[A-Z]|[0-9]){32})/?$',
                                                	'changePassword'),
    url( r'^forgotCode/(?P<forgotCode>([a-z]|[A-Z]|[0-9]){32})/(?P<check>check)/?$',
                                                	'changePassword'),
    url( r'^passwordChanged/?$',			'passwordChanged'),

    url( r'^test/?$',					'test'		),
)

urlpatterns += patterns('',
    (   r'^.*/media/(?P<path>.*)$',             'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}
    ),
    (   r'media/(?P<path>.*)$',             'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}
    ),
)
