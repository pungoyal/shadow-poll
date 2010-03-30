var mdg_overlay_array;

function MdgPallete(color_code, range){
		this.color_code = color_code;
		this.range = range;
}

    var palette1 = new MdgPallete(["#fbec04", "#faba04", "#f87a15", "#f7371e", "#f60925"],["0 < 10", "10 < 20", "20 < 30", "30 < 40", ">= 40"]);

    var palette2 = new MdgPallete(["#fbec04", "#c3eb18", "#7de931", "#33e74b", "#00e65d"],["< 68", "68 < 76", "76 < 84", "84 < 92", ">= 92"]);

    var palette3 = new MdgPallete(["#fbec04", "#faba04", "#f87a15", "#f7371e", "#f60925"],["0 < 10", "10 < 20", "20 < 30", "30 < 40", ">= 40"]);

    var palette4 = new MdgPallete(["#2a7fff", "#aaccff", "#ffffff", "#ffaaee", "#ff2ad4"],["< 70", "70 < 90", "90 < 110", "110 < 130", ">= 130"]);

    var palette5 = new MdgPallete(["#aa87de", "#9075bc", "#6f5e91", "#4e4766", "#373748"],["< 30", "30 < 40", "40 < 50", "50 < 60", ">= 60"]);

    var palette6 = new MdgPallete(["#00aad4", "#00aad4", "#00aad4", "#00aad4", "#00aad4"],["< 45", "45 < 60", "60 < 75", "75 < 90", ">= 90"]);

$(document).ready(function() {
    var geoserver_url = "http://iraqyouth.mepemepe.com/geoserver/ows";
    mdg_overlay_array = new Array();
    function MDG_overlay_factory(name, style, color_pallete)
    {
        var overlay = new OpenLayers.Layer.WMS(
                name,
                geoserver_url,
						{
								layers: 'unicef:iraq_mdgs',
								transparent: true,
								format: 'image/png',
								styles: style
						},
						{
								isBaseLayer: false,
								visibility: false,
								pallete: color_pallete
						}
				);
        overlay.setOpacity(0.5);
				mdg_overlay_array.push(overlay);
        return overlay;
    }



    map.addLayer(MDG_overlay_factory("poverty_overlay", 'mdgs_poverty', palette1));
    map.addLayer(MDG_overlay_factory("underweigh_overlay", 'mdgs_underweight', palette2));
    map.addLayer(MDG_overlay_factory("under5mort_overlay", 'mdgs_under5mort', palette5));
    map.addLayer(MDG_overlay_factory("infantmort_overlay", 'mdgs_infantmort', palette5));
    map.addLayer(MDG_overlay_factory("primary_enrollment_overlay", 'mdgs_primary_enrollment', palette3));
    map.addLayer(MDG_overlay_factory("intermediate_enrollment_overlay", 'mdgs_intermediate_enrollment', palette3));
    map.addLayer(MDG_overlay_factory("secondary_enrollment_overlay", 'mdgs_secondary_enrollment', palette3));
    map.addLayer(MDG_overlay_factory("femaletomale_enrollment_overlay", 'mdgs_femaletomale_enrollment', palette4));
    map.addLayer(MDG_overlay_factory("improved_drinking_water_overlay", 'mdgs_improved_drinking_water'));
    map.addLayer(MDG_overlay_factory("improved_sanitation_overlay", 'mdgs_improved_sanitation'));
    $.each($('.mdg_indicators'), function(index, value){
							 if (this.checked){
									 var selected_layer = map.getLayersByName(this.value)[0];
									 selected_layer.setVisibility(true);
									 var p = selected_layer.pallete;
									 $.each($('.legend_color'), function(index, value){
															$(this).css('background-color', p.color_code[index]);
													});
									 $.each($('.legend_text'), function(index, value){
															$(this).html(p.range[index]);
													});
									 $('#mdg_indicator_text').html($(this).next().html());
							 }
    });
});