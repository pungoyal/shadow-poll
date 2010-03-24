$(document).ready(function(){
var geoserver_url = "http://iraqyouth.mepemepe.com/geoserver/ows";
function MDG_overlay_factory(name, style)
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
	                   visibility: false
	                }
	);
	overlay.setOpacity(0.5);
	return overlay;
}

map.addLayer(MDG_overlay_factory("poverty_overlay", 'mdgs_poverty'));
map.addLayer(MDG_overlay_factory("underweigh_overlay", 'mdgs_underweight'));
map.addLayer(MDG_overlay_factory("under5mort_overlay", 'mdgs_under5mort'));
map.addLayer(MDG_overlay_factory("infantmort_overlay", 'mdgs_infantmort'));
map.addLayer(MDG_overlay_factory("primary_enrollment_overlay", 'mdgs_primary_enrollment'));
map.addLayer(MDG_overlay_factory("intermediate_enrollment_overlay", 'mdgs_intermediate_enrollment'));
map.addLayer(MDG_overlay_factory("secondary_enrollment_overlay", 'mdgs_secondary_enrollment'));
map.addLayer(MDG_overlay_factory("femaletomale_enrollment_overlay", 'mdgs_femaletomale_enrollment'));
map.addLayer(MDG_overlay_factory("improved_drinking_water_overlay", 'mdgs_improved_drinking_water'));
map.addLayer(MDG_overlay_factory("improved_sanitation_overlay", 'mdgs_improved_sanitation'));

});