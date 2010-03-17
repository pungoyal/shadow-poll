$(document).ready(function(){
		      $(".audio").
			  each(function(index){
				   addPlayer(this.id, index == 0, this.id.substring('jquery_jplayer'.length, this.id.length));
			       });
});

var addPlayer = function(audible, play, playerId){
    var soundFile = $("#soundfile_" + playerId).val();
    $("#" +audible)
	.jPlayer({
		    ready:function(){
			this.element.jPlayer("setFile", soundFile).jPlayer(play?"play":"pause");

		    },
		    nativeSupport: false,
		    customCssIds: true,
		    swfPath: "/static/charts/javascripts/"
		})
	.jPlayer("onProgressChange", function(loadPercent, playedPercentRelative, playedPercentAbsolute, playedTime, totalTime) {
		     jpPlayTime.text($.jPlayer.convertTime(playedTime));
		     jpTotalTime.text($.jPlayer.convertTime(totalTime));
		     demoStatusInfo(this.element, jpStatus); 
		 })
	.jPlayer("cssId", "play", "jplayer_play" + playerId)
	.jPlayer("cssId", "pause", "jplayer_pause" + playerId)
	.jPlayer("cssId", "stop", "jplayer_stop" + playerId)
	.jPlayer("cssId", "loadBar", "jplayer_load_bar" + playerId)
	.jPlayer("cssId", "playBar", "jplayer_play_bar" + playerId)
	.jPlayer("cssId", "volumeMin", "jplayer_volume_min" + playerId)
	.jPlayer("cssId", "volumeMax", "jplayer_volume_max" + playerId)
	.jPlayer("cssId", "volumeBar", "jplayer_volume_bar" + playerId)
	.jPlayer("cssId", "volumeBarValue", "jplayer_volume_bar_value" + playerId)
    ;
};

