##############################################################################
## Copyright (c) 2011-2013 Opticate, Inc.
## All rights reserved.
## This source code is confidential and may not be disclosed.
###############################################################################

###############################################################################
##
## "paginator.py":  Paginator definition
##
###############################################################################


from django.core.paginator  import Paginator, EmptyPage, PageNotAnInteger

###############################################################################
##
## "PaginatorObj": Define a paginator object
##
###############################################################################

class PaginatorObj( Paginator ):
    def __init__( self, objList, perPg, currPg = 1, padding = 3 ):
        
        currPg              = int(                      currPg          )
        self.currPg         = currPg
        self.paginator      = Paginator(                objList,
                                                        perPg           )

        self.setCurrPgintObj(                           currPg          )
        self.setVars(                                                   )
        self.setPgNum(                                  currPg,
                                                        padding         )
        
#-----------------------------------------------------------------------------
# "setCurrPgintObj": A function to set the current page paginator
#-----------------------------------------------------------------------------

    def setCurrPgintObj( self, pgNum ):

        try:
            self.currPgint  = self.paginator.page(      pgNum           )
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            self.currPgint  = self.paginator.page(      1               )
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            lstPage         = self.paginator.num_pages
            self.currPgint  = self.paginator.page(      lstPage         )
            
#-----------------------------------------------------------------------------
# "setVars": A function to set the some vaiables which used in HTML files
#-----------------------------------------------------------------------------

    def setVars( self, ):
        self.lastPage       = self.paginator.num_pages
        
        if self.currPg > self.lastPage:
            self.currPg     = self.lastPage
            
        self.isPaginated    = self.lastPage > 1
        
	self.hasPrev        = self.currPgint.has_previous(              )
	if self.hasPrev:
            self.prevPage   = self.currPgint.previous_page_number(  )
        else:
            self.prevPage   = 1
	
	self.hasNext        = self.currPgint.has_next(                  )
	if self.hasNext:
	    self.nextPage   = self.currPgint.next_page_number(          )
        else:
            self.nextPage   = self.lastPage
        
#-----------------------------------------------------------------------------
# "setCurrPgintObj": A function to set the current page paginator pages
#-----------------------------------------------------------------------------

    def setPgNum( self, pgNum, padding ):
        start               = pgNum - 1 - padding
        end                 = pgNum - 1 + padding
        if start < 0:
            end += 0 - start
            start = 0
            if end >= self.lastPage:
                end = self.lastPage - 1
        if end >= self.lastPage:
            start -= end - self.lastPage + 1
            end = self.lastPage - 1
            if start < 0:
                start = 0
                    
        self.pageNumbers    = [ ( p + 1 ) for p in xrange( start, end + 1 ) ]

#-----------------------------------------------------------------------------
# "getDataList": A function to return the current page paginator data list
#-----------------------------------------------------------------------------

    def getDataList( self ):
        return self.currPgint.object_list

