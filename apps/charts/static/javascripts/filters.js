$(document).ready(function(){
var slider_value = 0;
var current_gender = $('#gender-filter').html();
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
											$("#gender_slider").slider({
																										 value: slider_value,
																										 min: -1,
																										 max: 1,
																										 step:1,
																										 slide: function(event, ui){
																												 var gender = "all";
																												 if(ui.value == -1){
																														 gender = "boys";
																												 }else if(ui.value == 1){
																														 gender = "girls";
																												 }
																												 window.location =  current_governorate + "?gender="+gender;
																										 }
																								 });

											$("#age_slider").slider({
																									range: true,
																									min: 2,
																									max: 18,
																									values :[5, 15]
																							});
									});