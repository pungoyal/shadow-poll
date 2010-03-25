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

    $('.mdg_indicators').bind('click', function(e) {
        for (var i=0; i<mdg_overlay_array.length; i++) {
            var layer = mdg_overlay_array[i]; 
            layer.setVisibility(0);
        }

        var layer = map.getLayersByName(this.value)[0];
        layer.setVisibility(1);
    });
});     