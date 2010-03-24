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
        for (var i=0; i<map.layers.length; i++) {
            var layer = map.layers[i]; 
            layer.setVisibility(0);
        }
        map.baseLayer.setVisibility(1);
        map.getLayersByName('poll_responses')[0].setVisibility(1);

        var layer = map.getLayersByName(this.value)[0];
        layer.setVisibility(1);
    });
});     