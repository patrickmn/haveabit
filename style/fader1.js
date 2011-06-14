$(function () {
    $('head').append('<style type="text/css"> \
#header {visibility: hidden; opacity: 100;} \
#teaser {visibility: hidden; opacity: 100;} \
#content {visibility: hidden; opacity: 100;} \
#footer {visibility: hidden; opacity: 100;} \
</style>');

    $(window).load(function() {
	$('#header').css({visibility: 'visible', opacity: 0}).fadeTo(1500, 1, null);
	// old: 1500, lambda func above -> .delay(100, 150, 200).fadeto(1000)
	$('#teaser').css({visibility: 'visible', opacity: 0}).fadeTo(1500, 1, null);
	$('#content').css({visibility: 'visible', opacity: 0}).fadeTo(1500, 1, null);
	$('#footer').css({visibility: 'visible', opacity: 0}).fadeTo(1500, 1, null);
    });
});
