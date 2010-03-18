$(document).ready(function(){

    /**
     * BUBBLES
     * This loads the bubbles which represent the poll responses
     */

    var question_id = $("#question-id").html();
    var governorate_id = $("#governorate-id").html(); 
    function construct_kml_url(governorate_id, question_id)
    {
        var kml_url = "/get_kml/question" + question_id ;
        if (governorate_id != null && governorate_id != '')
        {
            kml_url = kml_url + "/governorate" + governorate_id ;
        }
        return kml_url;
    }
    
    kml_url = construct_kml_url(governorate_id, question_id);
    var bubbles = new OpenLayers.Layer.Vector(
        "poll_responses", 
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
                url: kml_url,
                format: new OpenLayers.Format.KML
                ({
                    extractStyles: true,
                    extractAttributes: true
                })
            })
        });
    bubbles.setOpacity(0.9);
    map.addLayer(bubbles);
    
    /**
     * CONTROLS
     */
    
    if (governorate_id == '')
    {
	    function onFeatureSelect(event) {
	        var feature = event.feature;
	        governorate_id = feature.attributes['id'];
	        window.document.location = '/charts/' + 'question' + question_id + '/governorate' +governorate_id;

	    }
	    
	    bubbles.events.on({
	        "featureselected": onFeatureSelect
	    });
    
        select = new OpenLayers.Control.SelectFeature([bubbles]);
        map.addControl(select);
        select.activate();
    }
    
    // This makes sure we zoom to the appropriate country/governorate level
    var bbox = $("#bbox").html();
    var governorate_zoom = $("#governorate-zoom").html();
    if (bbox != '')
    {	
        wkt = new OpenLayers.Format.WKT();
        vector = wkt.read(bbox);
        bounds = vector.geometry.getBounds().transform(
        			new OpenLayers.Projection('EPSG:4326'), 
        			new OpenLayers.Projection('EPSG:900913'));
        map.zoomToExtent(bounds);
        if (governorate_zoom != '')
        {
            map.zoomTo(governorate_zoom);
        }
    }

});