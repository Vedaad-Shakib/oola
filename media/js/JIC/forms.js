$(function() {
  $.tools.validator.addEffect("myEffect", function(errors, event) {
    $.each(errors, function(index, error) {
      $("#form_error_" + error.input.attr("name")).html(error.messages[0]);
    });
  }, function(inputs) {
    $.each(inputs, function() {
      $("#form_error_" + $(this).attr("name")).html('');
    });
  });
  $.tools.validator.fn("[integer]", "Please enter a valid number", function(input, value) {
    return (/^\d+$/.test(value)) || (value == "") ? true : false;
  });
  $.tools.validator.fn("[float]", "Please enter a valid float number", function(input, value) {
    return (/^\d+(\.\d+)?$/.test(value)) || (value == "") ? true : false;
  });
  $.tools.validator.fn("[time]", "Please enter a valid time.", function(input, value) {
    return (/^((([0]?[1-9]|1[0-2])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?( )?(AM|am|aM|Am|PM|pm|pM|Pm))|(([0]?[0-9]|1[0-9]|2[0-3])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?))$/.test(value)) || (value == "") ? true : false;
  });

  $.tools.validator.fn("[data-equals]", "Value not equal to the $1 field", function(input) {
    var name = input.attr("data-equals"), field = this.getInputs().filter("[name=" + name + "]");
    return input.val() == field.val() ? true : [name];
  });
  $.tools.validator.fn("[minlength]", "Please provide at least $1 characters", function(input) {
    var min = input.attr("minlength");
    return input.val().length >= min ? true : [min];
  });
  $.tools.validator.fn("[optminlength]", "Please provide at least $1 characters", function(input) {
    var min = input.attr("optminlength");
    var vlen = input.val().length;
    return (vlen >= min) || (vlen == 0) ? true : [min];
  });
  $.tools.validator.fn("[phone]", "Please enter a valid phone number", function(input, value) {
    if (/^(\+\d)*\s*((\(\d{3}\)|\d{3}\-)\s*)*\d{3}(-{0,1}|\s{0,1})\d{2}(-{0,1}|\s{0,1})\d{2}$/.test(value) || /[0-9]{10}/.test(value) || (value == "") || (value == $(input).attr("placeholder"))) {
      return true;
    } else {
      return false;
    }
  });
  $.tools.validator.localize("en", {
    "[required]" : "This field is required",
  });

  $("#formup").validator({
    'effect' : 'myEffect'
  }).submit(function(e) {
    var form = $(this);
    if (!e.isDefaultPrevented()) {
      $.getJSON("checkSignup/?" + form.serialize(), function(json) {
        if (json.load === true) {
          saveDb = window.document.getElementById("svdDataMsg");
          saveBtn = window.document.getElementById("saveBtn");
          if (saveDb) {
            $(saveBtn).css({
              cursor : "progress"
            });
            $(window.document.body).css({
              cursor : "progress"
            });
            $(saveDb).text("Information has been saved.");
            setTimeout(function() {
              window.location.assign(json.url);
            }, 1000);
          } else {
            window.location.assign(json.url);
          }

        } else {
          form.data("validator").invalidate(json.errors);
        }
      });
      e.preventDefault();
    }
  });

  $("formup[id^='ajaxForm']").validator({
    'effect' : 'myEffect'
  }).submit(function(e) {
    if (!e.isDefaultPrevented()) {
      var form = $(this);
      e.preventDefault();
      $.getJSON(form.attr("action") + "checkSignup/?" + form.serialize(), function(json) {
        if (json.load === true) {
          if (json.closeSecId != "") {
            $(json.closeSecId).html("");
          }
          if (json.loadUrl != "") {
            if (json.loadUrl instanceof Array) {
              for (var i = 0; i < json.loadUrl.length; i++) {
                $(json.loadSecId[i]).load(json.loadUrl[i]);
              }
            } else {
              $(json.loadSecId).load(json.loadUrl);
            }
          }
        } else {
          form.data("validator").invalidate(json.errors);
        }
      });
    }
  });

  $("formup[id^='ajaxEditForm_']").validator({
    'effect' : 'myEffect'
  }).submit(function(e) {
    if (!e.isDefaultPrevented()) {
      var form = $(this);
      e.preventDefault();
      $.getJSON(form.attr("action") + "checkSignup/?" + form.serialize(), function(json) {
        if (json.load === true) {
          if (json.closeSecId != "") {
            $(json.closeSecId).html("");
          }
          if (json.loadUrl != "") {
            if (json.loadUrl instanceof Array) {
              for (var i = 0; i < json.loadUrl.length; i++) {
                $(json.loadSecId[i]).load(json.loadUrl[i]);
              }
            } else {
              $(json.loadSecId).load(json.loadUrl);
            }
          }
        } else {
          form.data("validator").invalidate(json.errors);
        }
      });
    }
  });

  $("formup#ajaxImpFileForm").validator({
    'effect' : 'myEffect'
  })

  $("formup#gnlForm").validator({
    'effect' : 'myEffect'
  })

  $.tools.validator.addEffect("myEffect2", function(errors, event) {
    $.each(errors, function(index, error) {
      $("#form_error2_" + error.input.attr("name")).html(error.messages[0]);
    });
  }, function(inputs) {
    $.each(inputs, function() {
      $("#form_error2_" + $(this).attr("name")).html('');
    });
  });
  $("#formin").validator({
    'effect' : 'myEffect2'
  }).submit(function(e) {
    var form = $(this);
    if (!e.isDefaultPrevented()) {
      $.getJSON("checkSignin/?" + form.serialize(), function(json) {
        if (json.load === true) {

          saveDb = window.document.getElementById("svdDataMsg");
          saveBtn = window.document.getElementById("saveBtn");
          if (saveDb) {
            $(saveBtn).css({
              cursor : "progress"
            });
            $(window.document.body).css({
              cursor : "progress"
            });
            $(saveDb).text("Information has been saved.");
            setTimeout(function() {
              window.location.assign(json.url);
            }, 1000);
          } else {
            window.location.assign(json.url);
          }

        } else {
          form.data("validator").invalidate(json.errors);
        }
      });
      e.preventDefault();
    }
  });

  $("form[id^='ajaxForm']").validator({
    'effect' : 'myEffect2'
  }).submit(function(e) {
    if (!e.isDefaultPrevented()) {
      var form = $(this);
      e.preventDefault();
      $.getJSON(form.attr("action") + "checkSignin/?" + form.serialize(), function(json) {
        if (json.load === true) {
          if (json.closeSecId != "") {
            $(json.closeSecId).html("");
          }
          if (json.loadUrl != "") {
            if (json.loadUrl instanceof Array) {
              for (var i = 0; i < json.loadUrl.length; i++) {
                $(json.loadSecId[i]).load(json.loadUrl[i]);
              }
            } else {
              $(json.loadSecId).load(json.loadUrl);
            }
          }
        } else {
          form.data("validator").invalidate(json.errors);
        }
      });
    }
  });

  $("form[id^='ajaxEditForm_']").validator({
    'effect' : 'myEffect2'
  }).submit(function(e) {
    if (!e.isDefaultPrevented()) {
      var form = $(this);
      e.preventDefault();
      $.getJSON(form.attr("action") + "checkSignin/?" + form.serialize(), function(json) {
        if (json.load === true) {
          if (json.closeSecId != "") {
            $(json.closeSecId).html("");
          }
          if (json.loadUrl != "") {
            if (json.loadUrl instanceof Array) {
              for (var i = 0; i < json.loadUrl.length; i++) {
                $(json.loadSecId[i]).load(json.loadUrl[i]);
              }
            } else {
              $(json.loadSecId).load(json.loadUrl);
            }
          }
        } else {
          form.data("validator").invalidate(json.errors);
        }
      });
    }
  });

  $("formin#ajaxImpFileForm").validator({
    'effect' : 'myEffect2'
  })

  $("formin#gnlForm").validator({
    'effect' : 'myEffect2'
  })

});
