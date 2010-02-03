// javascript for the httpclient
url = "/http/proxy/";

$(document).ready(function(){
	$('#form').submit(function(){ sendMsg(); return false; });
	setInterval("checkMsgs()", 5000);
});

function sendMsg() {
	if ($('#phone').val().length > 0 && $('#message').val().length > 0) {
		req = url + $('#phone').val() + "/" + escape($('#message').val());
		$.getJSON(
			req, // if Ajax call succeeds, execute the following script
			function (response) { if (response) {
				snippet = '<tr class="in"><td class="phone">' + response.phone + '</td><td class="dir">&laquo;</td><td class="msg">' + response.message + '</td><td class="info">' + response.message.length + ' characters</td></tr>';
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
		req = url + $('#phone').val() + "/json_resp";
		$.getJSON(
			req,
			function (response) { if (response) {
				snippet = '<tr class="out"><td class="phone">' + response.phone + '</td><td class="dir">&raquo;</td><td class="msg">' + response.message + '</td><td class="info">' + response.message.length + ' characters</td></tr>';
				$('#log').append(snippet);
				fixClasses();
				$('div.tester').scrollTo('#log tr:last', 800);
			}}

		);
	}
}
