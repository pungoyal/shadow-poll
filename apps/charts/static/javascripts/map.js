/**
 * The main map for the UNICEF Iraq project
 */

var map;
OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;
OpenLayers.ImgPath = "http://js.mapbox.com/theme/dark/";
$(document).ready(function(){
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
    
    // load the iraq map tiles
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
    map.addControl(new OpenLayers.Control.Permalink());

    /**
     * BUBBLES
     * This loads the bubbles which represent the poll responses
     */

    var question_id = $("#question-id").html();
    var governorate_id = $("#governorate-id").html(); 
    var gender_code = location.href.split("?")[1]
    
    function construct_kml_url(governorate_id, question_id, gender_code)
    {
        var kml_url = "/get_kml";
        if (governorate_id != '' && governorate_id != null)
        {
            kml_url = kml_url + "/" + governorate_id;
        }
        kml_url = kml_url + "/question"+ question_id;
        if (gender_code != '' && gender_code != null)
        {
            kml_url = kml_url + '?' + gender_code;
        }
        return kml_url;
    }
    kml_url = construct_kml_url(governorate_id, question_id, gender_code)
    
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
	        var splt_gender_code=location.href.split("?")
	        var gender_code = ""
	            if (splt_gender_code[1] != null && splt_gender_code[1] != '')
	            {
	            		gender_code="?" + splt_gender_code[1]
	            }
	        
	    	window.document.location = '/charts/' + governorate_id + 
	    							   '/question' + question_id + gender_code;
	    }
	    
	    bubbles.events.on({
	        "featureselected": onFeatureSelect,
	    });
    
        select = new OpenLayers.Control.SelectFeature([bubbles]);
        map.addControl(select);
        select.activate();
    }

    /**
     * ZOOM
     */

    // center is set, for example, by zooming and panning
    // the first time we load the page, 'center' is not set,
    // so we must specify zoomextent
    if (!map.getCenter()) 
    {
        map.zoomToExtent(new OpenLayers.Bounds.fromString("4139217,3209132,5603139,4652263"));
        map.zoomTo(6);
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
