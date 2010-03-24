/**
 * The main map for the UNICEF Iraq project
 */

var map;
OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;
//OpenLayers.ImgPath = "http://js.mapbox.com/theme/dark/";
$(document).ready(function() {
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
                "http://a.unicef.mapbox.com/",
                "http://b.unicef.mapbox.com/",
                "http://c.unicef.mapbox.com/",
                "http://d.unicef.mapbox.com/"
            ],
    {
        'layername': 'unicef-iraq',
        'type':'png',
        'buffer':0,
        'transitionEffect': 'resize',
        'displayInLayerSwitcher': false
    });

    map.addLayers([iraq]);

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
});
