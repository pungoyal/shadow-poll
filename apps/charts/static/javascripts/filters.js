$(document).ready(function(){
											$("#gender_slider").slider({
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
																												 window.location = window.location + "?gender="+gender;
																										 }
																								 });
									});