/**
 * The main map for the UNICEF Iraq project
 */

var map;
OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;
OpenLayers.ImgPath = "http://js.mapbox.com/theme/dark/";
$(document).ready(function(){
	var question_id = $("#question-id").html();
    var options = {
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        units: "m",
        numZoomLevels: 12,
        maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(-20037500, -20037500, 20037500, 20037500),
        controls: []
    };
    map = new OpenLayers.Map('map', options);
 
    // create WMS layer
    var iraq = new OpenLayers.Layer.TMS(
        "Iraq Terrain",
        [
	        "http://a.tile.mapbox.com/",
	        "http://b.tile.mapbox.com/",
	        "http://c.tile.mapbox.com/",
	        "http://d.tile.mapbox.com/"
        ],
        {
	        'layername': 'iraq',
	        'type':'jpg'
        });
 
        map.addLayers([iraq]); 
        //map.addControl(new OpenLayers.Control.LayerSwitcher());
        map.addControl(new OpenLayers.Control.Permalink());

	if (!map.getCenter()) 
	{
		map.zoomToExtent(new OpenLayers.Bounds.fromString("4139217,3209132,5603139,4652263"));
		map.zoomTo(6);
	}
	
	var bubbles = new OpenLayers.Layer.Vector(
		"Poll Responses", 
		{
	    projection: map.displayProjection,
	    strategies: [new OpenLayers.Strategy.Fixed()],
	    styleMap: new OpenLayers.StyleMap(
	      OpenLayers.Util.applyDefaults(
	          {
	            fillColor: "#93ce54", 
	            fillOpacity: 1, 
	            strokeColor: "#4c8014",
	            pointRadius: 4
	          },
	          OpenLayers.Feature.Vector.style["default"]
	        )
	    ),
	    protocol: new OpenLayers.Protocol.HTTP
	    ({
	        url: "/get_kml/"+ question_id,
	        format: new OpenLayers.Format.KML
	        ({
	            extractStyles: true,
	            extractAttributes: true
	        })
	    })
	});
	bubbles.setOpacity(0.5);
	map.addLayer(bubbles);
	
	//bbox = '{{ bbox }}'
	var bbox = $("#bbox").html();
	if (bbox != '')
	{
	    wkt = new OpenLayers.Format.WKT();
	    vector = wkt.read(bbox);
	    bounds = vector.geometry.getBounds().transform(new OpenLayers.Projection('EPSG:4326'), new OpenLayers.Projection('EPSG:900913'));
	    map.zoomToExtent(bounds);
	}
});
