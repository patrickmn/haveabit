$(function () {
    $('head').append('<style type="text/css"> \
#header {visibility: hidden; opacity: 100;} \
#teaser {visibility: hidden; opacity: 100;} \
#content {visibility: hidden; opacity: 100;} \
#footer {visibility: hidden; opacity: 100;} \
</style>');

    $(window).load(function() {
	$('#header').css({visibility: 'visible', opacity: 0}).fadeTo(1500, 1, function() {
	    $('#teaser').css({visibility: 'visible', opacity: 0}).delay(100).fadeTo(1000, 1, null);
	    $('#content').css({visibility: 'visible', opacity: 0}).delay(100).fadeTo(1000, 1, null);
	    $('#footer').css({visibility: 'visible', opacity: 0}).delay(1100).fadeTo(1000, 1, null);
	});
	// $('#header').css({visibility: 'visible', opacity: 0}).fadeTo(1500, 1, null);
	// $('#teaser').css({visibility: 'visible', opacity: 0}).fadeTo(1500, 1, null);
	// $('#content').css({visibility: 'visible', opacity: 0}).fadeTo(1500, 1, null);
	// $('#footer').css({visibility: 'visible', opacity: 0}).fadeTo(1500, 1, null);
    });
});
