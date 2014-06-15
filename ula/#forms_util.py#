###############################################################################
## Copyright (c) 2011-2011 Opticate, Inc.
## All rights reserved.
## This source code is confidential and may not be disclosed.
###############################################################################

###############################################################################
##
## "forms_utility.py":
##
###############################################################################

from django import forms

#==============================================================================
# Define constants
#==============================================================================

YES_NO_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No')
    )

###############################################################################
##
## "EmailInput":  Form input for email
##
###############################################################################

class EmailInput(forms.widgets.Input):
    input_type = 'email'

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs.update(dict(autocorrect='off',
                          autocapitalize='off',
                          spellcheck='false'))
        return super(EmailInput, self).render(name, value, attrs=attrs)

###############################################################################
##
## "FieldEmail":  Form field CharField + EmailInput
##
###############################################################################

class FieldEmail(forms.CharField):
    def __init__(       self,
                        label,
			extraClass	= "",
                        max_length      = 128,
                        visible         = True,
			placeholder	= None,
                        required        = "auto",
                        section         = 'main',
                        admin           = False,
                        attrs           = {} ):

        if required == "auto": required = ( label[0] == "*" )

        attrs                   = attrs.copy()
        attrs['size']           = '30'
        attrs['class']          = 'inputtext ' + extraClass
        if required: attrs['required']  = 'required'
	if placeholder: attrs['placeholder'] = placeholder

        if visible:
            widget              = EmailInput( attrs = attrs     )
        else:
            widget              = forms.HiddenInput( attrs = attrs      )

        super(FieldEmail,self).__init__(
                        label           = label,
                        max_length      = max_length,
                        required        = required,
                        widget          = widget                        )

        self.visible    = visible
        self.section    = section
        self.admin      = admin

###############################################################################
##
## "FieldText":  Form field CharField + TextInput
##
###############################################################################

class FieldText(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
    			max_length	= 128,
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['class']		= 'inputtext ' + extraClass
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.TextInput( attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( attrs = attrs	)

	super(FieldText,self).__init__(	
			label		= label,
			max_length	= max_length,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldDate":  Date field
##
###############################################################################

class FieldDate(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= EmailInput( attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( attrs = attrs	)

	super(FieldDate,self).__init__(	
			label		= label,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldPassword":  Form field CharField + PasswordlInput
##
###############################################################################

class FieldPassword(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
    			max_length	= 128,
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['class']		= 'inputtext ' + extraClass

        if required:
            attrs['required']	= 'required'
            attrs['minlength']  = '6'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.PasswordInput( attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( attrs = attrs	)


	super(FieldPassword,self).__init__(	
			label		= label,
			max_length	= max_length,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldPassword2":  Form field CharField + PasswordlInput
##
###############################################################################

class FieldPassword2(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
			match		= 'password',
    			max_length	= 128,
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['class']		= 'inputtext ' + extraClass
	#attrs['data-equals']	= match
	attrs['equalTo']	= "#id_" + match
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.PasswordInput( attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( attrs = attrs	)


	super(FieldPassword2,self).__init__(	
			label		= label,
			max_length	= max_length,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldPhone":  Form field CharField + TextInput
##
###############################################################################

class FieldPhone(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
    			max_length	= 128,
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['class']		= 'inputtext ' + extraClass
	attrs['phone']		= '1'
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.TextInput( attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( attrs = attrs	)

	super(FieldPhone,self).__init__(	
			label		= label,
			max_length	= max_length,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldInteger":  Form field IntegerField + TextInput
##
###############################################################################

class FieldInteger(forms.IntegerField):
    def __init__(	self,
    			label,
			extraClass	= "",
    			max_value	= None,
    			min_value	= None,
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['class']		= 'inputtext ' + extraClass
	attrs['integer']	= '1'
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.TextInput( attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( attrs = attrs	)

	super(FieldInteger,self).__init__(	
			label		= label,
    			max_value	= max_value,
    			min_value	= min_value,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldCheckBox":  Form field CharField + CheckboxInput
##
###############################################################################

class FieldCheckBox(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['class']		= 'inputtext ' + extraClass
	attrs['value']		= 1
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.CheckboxInput( attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( attrs = attrs	)

	super(FieldCheckBox,self).__init__(	
			label		= label,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldCombo":  Form field CharField + Combo
##
###############################################################################

class FieldCombo(forms.ComboField):
    def __init__(	self,
    			label,
			extraClass	= "",
                        visible		= True,
    			choices 	= YES_NO_CHOICES,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['class']		= 'inputtext ' + extraClass
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.Select(      attrs = attrs,
                                                     choices=choices    )
	else:
	    widget		= forms.HiddenInput( attrs = attrs	)

	super(FieldCombo,self).__init__(	
			label		= label,
 			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldFloat":  Form field FloatField + TextInput
##
###############################################################################

class FieldFloat(forms.FloatField):
    def __init__(	self,
    			label,
			extraClass	= "",
    			max_value	= None,
    			min_value	= None,
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['class']		= 'inputtext ' + extraClass
	attrs['float']		= '1'
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.TextInput(  	attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( 	attrs = attrs	)

	super(FieldFloat,self).__init__(	
			label		= label,
    			max_value	= max_value,
    			min_value	= min_value,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldInfo":  Form field CharField + TextInput
##
###############################################################################
	
class FieldInfo(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
    			max_length	= 128,
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
                        value 		= "",
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['class']		= 'inputtext ' + extraClass
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	attrs['readonly']	= 'readonly'
	attrs['value']		= value
	
	if visible:
	    widget		= forms.TextInput(  	attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( 	attrs = attrs	)

	super(FieldInfo,self).__init__(	
			label		= label,
			max_length	= max_length,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldRadioButton":  Form field CharField + RadioSelect
##
###############################################################################

class FieldRadioButton(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
			visible		= True,
                        choices 	= [],
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['class']		= 'inputtext ' + extraClass
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.RadioSelect(	attrs 	= attrs,
                                            		choices = choices   )
	else:
	    widget		= forms.HiddenInput( 	attrs 	= attrs	    )

	super(FieldRadioButton,self).__init__(		label	= label,
                                                	required= required,
							widget	= widget    )

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldSelectList":  Form field CharField + SelectMultiple
##
###############################################################################

class FieldSelectList(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
			visible		= True,
                        choices 	= [],
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['class']		= 'inputtext ' + extraClass
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.SelectMultiple( attrs 	= attrs,
                                            		choices = choices   )
	else:
	    widget		= forms.HiddenInput( 	attrs 	= attrs	    )

	super(FieldSelectList,self).__init__(		label	= label,
                                                	required= required,
							widget	= widget    )

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldTime":  Form field CharField + TextInput
##
###############################################################################

class FieldTime(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['class']		= 'inputtext ' + extraClass
	attrs['time']		= '1'
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.TextInput(  	attrs 	= attrs	    )
	else:
	    widget		= forms.HiddenInput( 	attrs 	= attrs	    )

	super(FieldTime,self).__init__(			label	= label,
                                                	required= required,
							widget	= widget    )

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldTextArea":  Form Text area field
##
###############################################################################

class FieldTextarea(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
    			max_length	= 1000,
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['cols']		= '28'
	attrs['class']		= 'inputtext ' + extraClass
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.Textarea( attrs = attrs	)
	else:
	    widget		= forms.HiddenInput( attrs = attrs	)

	super(FieldTextarea,self).__init__(	
			label		= label,
			max_length	= max_length,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldMultiEmail":  MultiEmail Form field
##
###############################################################################

class FieldMultiEmail(forms.CharField):
    def __init__(	self,
    			label,
			extraClass	= "",
    			max_length	= 512,
			visible		= True,
			placeholder	= None,
			required	= "auto",
			section		= 'main',
			admin		= False,
			attrs		= {} ):

	if required == "auto": required = ( label[0] == "*" )

	attrs			= attrs.copy()
	attrs['size']		= '30'
	attrs['class']		= 'inputtext ' + extraClass
	if required: attrs['required']	= 'required'
	if placeholder: attrs['placeholder'] = placeholder

	if visible:
	    widget		= forms.Textarea(       attrs = attrs	)
	else:
	    widget		= forms.HiddenInput(    attrs = attrs	)

	super(FieldMultiEmail,self).__init__(	
			label		= label,
			max_length	= max_length,
			required	= required,
			widget		= widget			)

	self.visible	= visible
	self.section	= section
	self.admin	= admin

###############################################################################
##
## "FieldFileInput":  Form field FieldFileInput
##
###############################################################################

class FieldFileInput(forms.FileField):
    def __init__(    	self,
                     	label,
			extraClass	= "",
                     	visible    	= True,
			placeholder	= None,
                     	required   	= "auto",
                     	section    	= 'main',
                     	admin      	= False,
                     	attrs      	= {} ):

        if required == "auto": required = ( label[0] == "*" )

        attrs           = attrs.copy()
        attrs['class']  = 'inputtext ' + extraClass
        if required: attrs['required']    = 'required'
	if placeholder: attrs['placeholder'] = placeholder

        if visible:
            widget      = forms.ClearableFileInput( attrs = attrs    )
        else:
            widget      = forms.HiddenInput( attrs = attrs    )

        super(FieldFileInput,self).__init__(
                label   = label,
                required= required,
                widget  = widget            )

        self.visible    = visible
        self.section    = section
        self.admin      = admin

###############################################################################
##
## "FieldSelect":  Form field CharField + FieldSelect
##
###############################################################################

class FieldSelect(forms.CharField):
    def __init__(    	self,
                     	label,
			extraClass	= "",
                     	visible    	= True,
			placeholder	= None,
                     	required   	= "auto",
                     	section    	= 'main',
                     	admin      	= False,
                     	attrs      	= {} ):

        if required == "auto": required = ( label[0] == "*" )

        attrs           = attrs.copy()
        attrs['class']  = 'inputtext ' + extraClass
        if required: attrs['required']    = 'required'
	if placeholder: attrs['placeholder'] = placeholder

        if visible:
            widget      = forms.Select(     attrs   = attrs,
                                            choices = choices           )
        else:
            widget      = forms.HiddenInput(attrs   = attrs             )

        super(FieldSelect,self).__init__(label  = label,
                                             required= required,
                                             widget = widget            )

        self.visible    = visible
        self.section    = section
        self.admin      = admin

###############################################################################
##
## "FieldMultiSelect":  Form field CharField + FieldMultiSelect
##
###############################################################################

class FieldMultiSelect(forms.MultiValueField):
    def __init__(   self,
                    label,
			extraClass	= "",
                    visible = True,
                    choices = YES_NO_CHOICES,
			placeholder	= None,
                    required= "auto",
                    section = 'main',
                    admin   = False,
                    attrs   = {}
            ):

        if required == "auto": required = ( label[0] == "*" )

        attrs           = attrs.copy()
        attrs['class']  = 'inputtext ' + extraClass
        if required: attrs['required']    = 'required'
	if placeholder: attrs['placeholder'] = placeholder

        if visible:
            widget      = forms.SelectMultiple( attrs = attrs,
                                                        choices=choices )
        else:
            widget      = forms.HiddenInput(            attrs = attrs   )

        super(FieldMultiSelect,self).__init__(
                                              label     = label,
                                              required  = required,
                                              widget    = widget        )

        self.visible    = visible
        self.section    = section
        self.admin      = admin

###############################################################################
##
## "FieldCheckboxMultiSelect":  Form field CharField + FieldCheckboxMultiSelect
##
###############################################################################

class FieldCheckboxMultiSelect(forms.MultiValueField):
    def __init__(   	self,
                    	label,
			extraClass	= "",
                    	visible		= True,
                    	choices		= YES_NO_CHOICES,
			placeholder	= None,
                    	required	= "auto",
                    	section 	= 'main',
                    	admin   	= False,
                    	attrs   	= {}
            ):

        if required == "auto": required = ( label[0] == "*" )

        attrs           = attrs.copy()
        attrs['class']  = 'inputtext ' + extraClass
        if required: attrs['required']    = 'required'
	if placeholder: attrs['placeholder'] = placeholder

        if visible:
            widget      = forms.CheckboxSelectMultiple( attrs = attrs,
                                                        choices=choices )
        else:
            widget      = forms.HiddenInput(            attrs = attrs   )

        super(FieldCheckboxMultiSelect,self).__init__(
                                              label     = label,
                                              required  = required,
                                              widget    = widget        )

        self.visible    = visible
        self.section    = section
        self.admin      = admin
