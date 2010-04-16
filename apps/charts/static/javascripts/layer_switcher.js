$(document).ready(function() {
    var slide_direction = "left";
    if($('#ar').hasClass('current_language')){
				slide_direction = "right";
		}
    $("#map_legend_trigger").click(
	  	 function() {
		      $(this).hide("slide", { direction: slide_direction }, 1000);
		      $('#mdg_legends').show("slide", { direction: slide_direction }, 1000);
	  });   
	
	 $("#map_legend_close").click(
	  	 function() {
		     $('#map_legend_trigger').show("slide", { direction: slide_direction }, 2000);
		     $('#mdg_legends').hide("slide", { direction: slide_direction }, 1000);
	  });  

    $("#map_layer_overlay a.expand").toggle(
            function() {
                $('#expandable_content').slideDown();
                $(this).attr("class", "collapse");
            },
            function() {
                $('#expandable_content').slideUp();
                $(this).attr("class", "expand");
            });

    $('.mdg_indicators').bind('click', function(e) {
        for (var i=0; i<mdg_overlay_array.length; i++) {
            var layer = mdg_overlay_array[i]; 
            layer.setVisibility(0);
        }

        var layer = map.getLayersByName(this.value)[0];
        layer.setVisibility(1);
        var p = layer.pallete;
        $.each($('.legend_color'), function(index, value){
            $(this).css('background-color', p.color_code[index]);
        });
        $.each($('.legend_text'), function(index, value){
            $(this).html(p.range[index]);
        });
        $('#mdg_indicator_text').html($(this).next().html());
        if(!$('#mdg_legends').is(':visible')){
						        $('#map_legend_trigger').hide("slide", { direction: slide_direction }, 1000);
						$('#mdg_legends').show("slide", { direction: slide_direction }, 1000);
				}

    });
});