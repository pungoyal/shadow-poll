$(document).ready(function(){
var slider_value = 0;
var current_gender = $('#gender-filter').html();
var age_range = $('#age_range_filter').html().split(",");
$.each(age_range, function(index, value){
					 age_range[index] = parseInt(value);
			 });
var current_governorate = $('#governorate-id').html();
if(current_gender == "boys"){
		slider_value = -1;
}else if(current_gender == "girls"){
		slider_value = 1;
}
if(current_governorate == ''){
		current_governorate = "all";
}else{
		current_governorate = "governorate" + current_governorate;
}
$('#lower_age_range').html(age_range[0]);
$('#higher_age_range').html(age_range[1]);
$("#gender_slider").slider({
															 value: slider_value,
															 min: -1,
															 max: 1,
															 step:1
													 });
$("#age_slider").slider({
														range: true,
														min: 2,
														max: 18,
														values : age_range,
														slide: function(event, ui){
																$('#lower_age_range').html(ui.values[0]);
																$('#higher_age_range').html(ui.values[1]);
														}
												});
											
$("#filter_button").bind('click', function(e){
														 var age_slider_value  = $("#age_slider").slider("values").toString();
														 var gender_slider_value = $("#gender_slider").slider("value");
														 var gender = "all";
														 if(gender_slider_value == -1){
																 gender = "boys";
														 }else if(gender_slider_value == 1){
																 gender = "girls";
														 }
																 
														 window.location = current_governorate + "?gender=" + gender + "&age="+age_slider_value;
												 });
									});