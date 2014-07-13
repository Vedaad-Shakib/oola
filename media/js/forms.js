jQuery( function() {

  //=====================================================================
  // Override jquery validate plugin defaults
  //=====================================================================

  jQuery.validator.setDefaults({
    highlight: function(element) {
        jQuery(element).closest('.form-group').addClass('has-error');
    },
    unhighlight: function(element) {
        jQuery(element).closest('.form-group').removeClass('has-error');
    },
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function(error, element) {
        if(element.parent('.input-group').length) {
            error.insertAfter(element.parent());
        } else {
            error.insertAfter(element);
        }
    }
  });

  //=====================================================================
  //  Add custom validation methods
  //=====================================================================

  jQuery.validator.addMethod( "phone", function(value, element) {
    if ( /^(\+\d)*\s*((\(\d{3}\)|\d{3}\-)\s*)*\d{3}(-{0,1}|\s{0,1})\d{2}(-{0,1}|\s{0,1})\d{2}$/.test(value)
	|| /[0-9]{10}/.test(value)
	|| (value == "")
	|| (value == jQuery(element).attr("placeholder"))) {
      return true ;
    } else {
      return false ;
    }
  }, "Please enter a valid phone number" );

  jQuery.validator.addMethod( "integer", function(value, element) { 
    return (/^\d+$/.test(value)) || (value == "") ? true : false ;
  }, "Please enter a valid number" );
  
  /*
  jQuery.validator.addMethod( "float", function(value, element) { 
    return (/^\d+(\.\d+)?$/.test(value)) || (value == "") ? true : false ;
  }, "Please enter a valid float number" );
  
  For add Product problem I comment this */
  
  jQuery.validator.addMethod( "time", function(value, element) { 
    return (/^((([0]?[1-9]|1[0-2])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?( )?(AM|am|aM|Am|PM|pm|pM|Pm))|(([0]?[0-9]|1[0-9]|2[0-3])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?))$/.test(value)) || (value == "") ? true : false ;
  }, "Please enter a valid time" );

  jQuery.validator.addMethod( "date", function(value, element) { 	
    return (/^((19)[7-9]\d|(20)[01]\d)[\.\-/](0?[1-9]|1[0-2])[\.\-/](0?[1-9]|[12]\d|3[01])$/.test(value)) || (value == "") ? true : false ;
  }, "Please enter a valid date" );

  jQuery.validator.addMethod( "file", function(value, element) {
    var ext = element.getAttribute("extension");
    if ( ext ){
    	var myRe = new RegExp("^.+\." + ext + "$" );
    	return (myRe.test(value)) || (value == "") ? true : false ;
    }
    else{
    	return true
    }
  }, "Please select a valid file type" );

  //=====================================================================
  //  Validate Drop down forms 
  //=====================================================================

  jQuery("form[id=chkDrpDwnFrm]").each(function() {
   jQuery(this).validate({
    submitHandler: function(form) {
	var jForm = jQuery(form);
	jQuery.getJSON( jForm.attr("action") + "check/?" + jForm.serialize(), function(json) {
		if (json.load === true) {
		
			if (json.url != ""){
				window.location.assign( json.url );
			}

			if (json.closeSecId != ""){
				jQuery( json.closeSecId ).dropdown('toggle');
			}

			if (json.loadUrl != ""){
				if (json.modalSec === true) {
					jQuery( json.loadSecId ).load( json.loadUrl ).modal();
				}
				else{
					jQuery( json.loadSecId ).load( json.loadUrl );
				}
			}

		}
		else{
			jForm.validate().showErrors(json.errors);
		}
	});
    }	
   });
  });

  //=====================================================================
  //  Validate Register forms
  //=====================================================================

  jQuery("#formup").submit( function(e){
    var form = jQuery(this);
    if (!e.isDefaultPrevented()) {
      if( form.valid() ){
      
	    jQuery.getJSON( form.attr("action") + "checkSignup/?" + form.serialize(), function(json) {
		  if (json.load === true) {
			if (json.url != ""){
				window.location.assign( json.url );
			}

			if (json.closeSecId != ""){
				jQuery( json.closeSecId ).html('');
			}

			if (json.loadUrl != ""){
				if (json.modalSec === true) {
					jQuery( json.loadSecId ).load( json.loadUrl ).modal();
				}
				else{
					jQuery( json.loadSecId ).load( json.loadUrl );
				}
			}

		  }
		  else{
			form.validate().showErrors(json.errors);
		  }
	    });
	    
	  }
      e.preventDefault();
    }
    
  });


  //=====================================================================
  //  Validate Signin form
  //=====================================================================

  jQuery("#formin").submit( function(e){
    var form = jQuery(this);
    if (!e.isDefaultPrevented()) {
      if( form.valid() ){
      
	    jQuery.getJSON( form.attr("action") + "checkSignin/?" + form.serialize(), function(json) {
		  if (json.load === true) {
			if (json.url != ""){
				window.location.assign( json.url );
			}

			if (json.closeSecId != ""){
				jQuery( json.closeSecId ).html('');
			}

			if (json.loadUrl != ""){
				if (json.modalSec === true) {
					jQuery( json.loadSecId ).load( json.loadUrl ).modal();
				}
				else{
					jQuery( json.loadSecId ).load( json.loadUrl );
				}
			}

		  }
		  else{
			form.validate().showErrors(json.errors);
		  }
	    });
	    
	  }
      e.preventDefault();
    }
    
  });

  //=====================================================================
  //  Validate form
  //=====================================================================

  jQuery("#form").submit( function(e){
    var form = jQuery(this);
    if (!e.isDefaultPrevented()) {
      if( form.valid() ){
      
	    jQuery.getJSON( form.attr("action") + "check/?" + form.serialize(), function(json) {
		  if (json.load === true) {
			if (json.url != ""){
				window.location.assign( json.url );
			}

			if (json.closeSecId != ""){
				jQuery( json.closeSecId ).html('');
			}

			if (json.loadUrl != ""){
				if (json.modalSec === true) {
					jQuery( json.loadSecId ).load( json.loadUrl ).modal();
				}
				else{
					jQuery( json.loadSecId ).load( json.loadUrl );
				}
			}

		  }
		  else{
			form.validate().showErrors(json.errors);
		  }
	    });
	    
	  }
      e.preventDefault();
    }
    
  });

  //=====================================================================
  //  Validate Modal Dialog forms 
  //=====================================================================

  jQuery("form[id=chkMdDlgFrm]").each(function() {
   jQuery(this).validate({
    submitHandler: function(form) {
	var jForm = jQuery(form);
	jQuery.getJSON( jForm.attr("action") + "check/?" + jForm.serialize(), function(json) {
		if (json.load === true) {
		
			if (json.url != ""){
				window.location.assign( json.url );
			}

			if (json.closeSecId != ""){
				jQuery( json.closeSecId ).modal('hide');
			}

			if (json.loadUrl != ""){
				jQuery( json.loadSecId ).load( json.loadUrl );
			}

		}
		else{
			jForm.validate().showErrors(json.errors);
		}
	});
    }	
   });
  });

  //=====================================================================
  //  Close Drop down form and then submit (POST) it 
  //=====================================================================

  jQuery( "form#postDrpdnForm" ).submit( function(e){
	  var form 	= jQuery( this );
      if( form.valid() ){
	  	var id	= jQuery( this ).attr( "drpdnId" );
	    jQuery( '#' + id ).dropdown('toggle');
	  }
	  else{
	    e.preventDefault();
	  }
  });

  //=====================================================================
  //  Check file input field
  //  I used this because the error message wouldn't remove when OK
  //=====================================================================

  jQuery("input[type=file]").each(function(){
  	jQuery( this ).change(function(e){ 		// fires every time this field changes
        jQuery(this).valid();               // force a validation test on this field
    });
  });

  //=====================================================================
  //  Validate Modal Dialog form and then submit (POST) it 
  //=====================================================================

  jQuery( "form#postMdDlgForm" ).submit( function(e){
	  var form 	= jQuery( this );
      if( form.valid() ){
	  }
	  else{
	    e.preventDefault();
	  }
  });

  //=====================================================================
  //  Auto complete field
  //=====================================================================

	jQuery( "[id^=autoCmpField]" ).each(function( i ) 
	{
		var url = jQuery(this).attr("autoCmpUrl");
		jQuery(this).typeahead({
		    source: function (query, process) {
		        return jQuery.get(url, { query: query }, function (data) {
		            return process(data);
		        });
		    }
		});
	});

  //=====================================================================
  //  Validate Modal Dialog forms 
  //=====================================================================

  jQuery("form[id= editStudentFrm]").each(function() {
   jQuery(this).validate({
    submitHandler: function(form) {
	var jForm = jQuery(form);
	jQuery.getJSON( jForm.attr("action") + "check/?" + jForm.serialize(), function(json) {
		if (json.load === true) {
			jQuery( json.closeSecId ).modal('hide');
			submitCntrlForm();
		}
		else{
			jForm.validate().showErrors(json.errors);
		}
	});
    }	
   });
  });


  
});
