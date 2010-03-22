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

});