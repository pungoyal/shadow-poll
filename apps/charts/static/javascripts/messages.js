$(document).ready(function(){
		      $(".audio").
			  each(function(index){
				   addPlayer(this.id);
			       });
});

var addPlayer = function(audible){
    $("#" +audible).
	jPlayer({
		    ready:function(){
			this.element.jPlayer("setFile", "http://www.miaowmusic.com/mp3/Miaow-07-Bubble.mp3", "http://www.miaowmusic.com/ogg/Miaow-07-Bubble.ogg").jPlayer("play");

		    },
		    nativeSupport: false,
		    customCssIds: true,
		    swfPath: "../static/charts/javascripts/"
		})
	.jPlayer("onProgressChange", function(loadPercent, playedPercentRelative, playedPercentAbsolute, playedTime, totalTime) {
		     jpPlayTime.text($.jPlayer.convertTime(playedTime));
		     jpTotalTime.text($.jPlayer.convertTime(totalTime));
		     demoStatusInfo(this.element, jpStatus); 
		 });
    
};

