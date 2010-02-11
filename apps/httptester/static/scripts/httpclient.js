// javascript for the httpclient
url = "/http/proxy/";

$(document).ready(function(){
	$('#form').submit(function(){ sendMsg(); return false; });
	setInterval("checkMsgs()", 5000);
});

function sendMsg() {
	if ($('#phone').val().length > 0 && $('#message').val().length > 0) {
		$.post(
			url, 
			{ "number": $('#phone').val(), "message": escape($('#message').val()) }, 
			function (response) { if (response) { // if Ajax call succeeds, execute this function
				// I don't speak javascript. Someone please clean this up
				to_eval = "resp_dict = " + response
				eval(to_eval)
				snippet = '<tr class="in"><td class="phone">' + resp_dict.phone + '</td><td class="dir">&laquo;</td><td class="msg">' + unescape(resp_dict.message) + '</td><td class="info">' + resp_dict.message.length + ' characters</td></tr>';
				$('#log').append(snippet);
				fixClasses();
				$('div.tester').scrollTo('#log tr:last', 800);
				$('#message').val("");
			}}
		);
	}
}

function fixClasses(){
	$('#log tr').removeClass('first');
	$('#log tr').removeClass('last');
	$('#log tr:first').addClass('first');
	$('#log tr:last').addClass('last');
}

function checkMsgs() {
	if ($('#phone').val().length > 0) {
		$.post(
			url,
			{ number: $('#phone').val(), message: "json_resp" }, 
			function (response) { if (response) {
				// I don't speak javascript. Someone please clean this up
				to_eval = "resp_dict = " + response
				eval(to_eval)
				snippet = '<tr class="out"><td class="phone">' + resp_dict.phone + '</td><td class="dir">&raquo;</td><td class="msg">' + resp_dict.message + '</td><td class="info">' + resp_dict.message.length + ' characters</td></tr>';
				$('#log').append(snippet);
				fixClasses();
				$('div.tester').scrollTo('#log tr:last', 800);
			}}

		);
	}
}
