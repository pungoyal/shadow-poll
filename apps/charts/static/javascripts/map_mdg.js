$(document).ready(function(){
var geoserver_url = "http://"+window.location.host+"/geoserver/ows";
var mdg_overlay = new OpenLayers.Layer.WMS(
                "MDG Data",
                geoserver_url,
                { 
                   layers: 'unicef:iraq_mdgs',
                   transparent: true,
                   format: 'image/png'
                },
                {
                   isBaseLayer: false,
                   visibility: true
                }
);
mdg_overlay.setOpacity(0.5);
map.addLayer(mdg_overlay);
});