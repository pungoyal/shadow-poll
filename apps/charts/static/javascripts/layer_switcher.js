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
$('.mdg_indicators').bind('click', function(e){
if(this.checked){
		
}else{
		
}
});

									});     