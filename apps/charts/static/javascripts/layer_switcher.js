$(document).ready(function() {
											$("#map_layer_overlay a.expand").toggle(
													function() {
															$('#expandable_content').slideDown();
															$(this).attr("class", "collapse");
													},
													function() {                   
															$('#expandable_content').slideUp();
															$(this).attr("class", "expand");
													});

$.each($('.mdg_indicators'), function(i, val){
					 var layer = map.getLayersByName(val.value)[0];
					 layer.setVisibility(val.checked);
});
$('.mdg_indicators').bind('click', function(e){
															var layer = map.getLayersByName(this.value)[0];
															layer.setVisibility(this.checked);
});
});     