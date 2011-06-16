// IE sucks
(function($) {
    $.fn.habFadeIn = function(speed, callback) {
        $(this).fadeIn(speed, function() {
                if(jQuery.browser.msie)
                        $(this).get(0).style.removeAttribute('filter');
                if(callback != undefined)
                        callback();
        });
    };
    $.fn.habFadeOut = function(speed, callback) {
        $(this).fadeOut(speed, function() {
                if(jQuery.browser.msie)
                        $(this).get(0).style.removeAttribute('filter');
                if(callback != undefined)
                        callback();
        });
    };
    $.fn.habFadeTo = function(speed, opacity, callback) {
        $(this).fadeTo(speed, opacity, function() {
                if(jQuery.browser.msie)
                        $(this).get(0).style.removeAttribute('filter');
                if(callback != undefined)
                        callback();
        });
    };
})(jQuery);

$(function () {
    $('head').append('<style type="text/css"> \
#header {visibility: hidden; opacity: 100;} \
#teaser {visibility: hidden; opacity: 100;} \
#content {visibility: hidden; opacity: 100;} \
#footer {visibility: hidden; opacity: 100;} \
</style>');

    $(window).load(function() {
	$('#header').css({visibility: 'visible', opacity: 0}).habFadeTo(1500, 1, function() {
	    $('#teaser').css({visibility: 'visible', opacity: 0}).delay(100).habFadeTo(1000, 1, null);
	    $('#content').css({visibility: 'visible', opacity: 0}).delay(100).habFadeTo(1000, 1, null);
	    $('#footer').css({visibility: 'visible', opacity: 0}).delay(1200).habFadeTo(1000, 1, null);
	});
    });

    $(document).ready(function() {
	$('a').click(function(e) {
	    if (e.which == 1) {
		e.preventDefault();
		window.location = this.href;
		$('body').habFadeOut(500, null);
	    }
	});

        $(window).keydown(function(e) {
            if (e.which == 82) {
		// r
		window.location = '/random';
		$('body').habFadeOut(500, null);
            }
	    else if (e.which == 65) {
		// a
		// window.location = '<author slug link>';
		// $('body').habFadeOut(500, null);
	    }
	    else if (e.which == 72) {
		// h
		window.location = '/';
		$('body').habFadeOut(500, null);
	    }
        });
    });
});
