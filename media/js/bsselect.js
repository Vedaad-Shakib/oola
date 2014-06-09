/**
 * @version: 1.0.1
 * @author: Dan Grossman http://www.dangrossman.info/
 * @date: 2012-08-20
 * @copyright: Copyright (c) 2012 Dan Grossman. All rights reserved.
 * @license: Licensed under Apache License v2.0. See http://www.apache.org/licenses/LICENSE-2.0
 * @website: http://www.improvely.com/
 */
!function ($) {

    var BSSelect = function (element, goals, cb) {


        this.cb = function () { };

        //element that triggered the date range picker
        this.element = $(element);

        this.goals = goals;

        this.opens = 'right';
        if (this.element.hasClass('pull-right'))
            this.opens = 'left';

        this.element.on('click', $.proxy(this.show, this));

        var BSSTemplate = '<div class="daterangepicker dropdown-menu">' +
                '<div class="ranges">' +
                '</div>' +
	'</div>';

        this.container = $(BSSTemplate).appendTo('body');

        var list = '<ul>';
        for (var key in this.goals) {
            list += '<li title="' + key + '">' + this.goals[key] + '</li>';
        }
        list += '</ul>';
        this.container.find('.ranges').prepend(list);

        if (typeof cb == 'function')
            this.cb = cb;

        this.container.addClass('opens' + this.opens);

        //event listeners
        this.container.on('mousedown', $.proxy(this.mousedown, this));
        this.container.find('.ranges').on('click', 'li', $.proxy(this.clickGoal, this));

    };

    BSSelect.prototype = {

        constructor: BSSelect,

        mousedown: function (e) {
            e.stopPropagation();
            e.preventDefault();
        },

        move: function () {
            if (this.opens == 'left') {
                this.container.css({
			top: this.element.offset().top + this.element.outerHeight(),
			right: $(window).width() - this.element.offset().left - this.element.outerWidth(),
			left: 'auto'
		    });
            } else {
                this.container.css({
			top: this.element.offset().top + this.element.outerHeight(),
			left: this.element.offset().left,
			right: 'auto'
		    });
            }
        },

        show: function (e) {
            this.container.show();
            this.move();

            if (e) {
                e.stopPropagation();
                e.preventDefault();
            }
            
            $(document).on('mousedown', $.proxy(this.hide, this));
        },

        hide: function (e) {
            this.container.hide();
            $(document).off('mousedown', this.hide);
        },

        clickGoal: function (e) {
            var key = $(e.target).attr('title');
            this.cb(key);
            this.hide();
        }

    };

    $.fn.bsselect = function (options, cb) {
	return new BSSelect(this, options, cb);
    };

} (window.jQuery);