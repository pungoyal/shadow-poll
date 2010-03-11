$(document).ready(function() {

	var elem = ".#poll_questions ul li a";
	$(elem).css("opacity","0.5");

	$(elem).hover(function () {	 
	$(this).stop().animate({opacity: 1.0}, "slow");
	},
	function () {
	$(this).stop().animate({opacity: 0.5}, "slow");
	});
});