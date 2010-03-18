$(document).ready(function(){
var geoserver_url = "http://"+window.location.host+"/geoserver/ows";
var poverty_overlay = new OpenLayers.Layer.WMS(
                "poverty_overlay",
                geoserver_url,
                { 
                   layers: 'unicef:iraq_mdgs',
                   transparent: true,
                   format: 'image/png',
                   styles: 'mdgs_poverty'
                },
                {
                   isBaseLayer: false,
                   visibility: false
                }
);
poverty_overlay.setOpacity(0.5);
map.addLayer(poverty_overlay);

var underweigh_overlay = new OpenLayers.Layer.WMS(
                "underweigh_overlay",
                geoserver_url,
                { 
                   layers: 'unicef:iraq_mdgs',
                   transparent: true,
                   format: 'image/png',
                   styles: 'mdgs_underweight'
                },
                {
                   isBaseLayer: false,
                   visibility: false
                }
);
underweigh_overlay.setOpacity(0.5);
map.addLayer(underweigh_overlay);

var under5mort_overlay = new OpenLayers.Layer.WMS(
                "under5mort_overlay",
                geoserver_url,
                { 
                   layers: 'unicef:iraq_mdgs',
                   transparent: true,
                   format: 'image/png',
                   styles: 'mdgs_under5mort'
                },
                {
                   isBaseLayer: false,
                   visibility: false
                }
);
under5mort_overlay.setOpacity(0.5);
map.addLayer(under5mort_overlay);
});