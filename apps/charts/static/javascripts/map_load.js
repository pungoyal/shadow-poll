/**
 * Javascript documentation:
 *
 * Given that OpenLayers involves a lot of property lists,
 * keep in mind the one GIGANTIC javascript quirk that matters:
 *
 * IE will break if you have an object declaration with a trailing comma, like
 *
 * obj = { fa: 'fa', foo: 'foo', };
 *
 * Instead, this works:
 *
 * obj = { fa: 'fa', foo: 'foo' };
 *
 */
var map;
//OpenLayers.ImgPath = '/img/openlayers/';

/**
 * MAP CONSTRUCTION
 */

options = {
  units: "m",
  maxResolution: 156543.0339,
  numZoomLevels: 20,
  maxExtent: new OpenLayers.Bounds(-20037508,-20037508,20037508,20037508),
  projection: new OpenLayers.Projection("EPSG:900913"),
  displayProjection: new OpenLayers.Projection("EPSG:4326"),
  // restrictedExtent: new OpenLayers.Bounds(-20037508,-20037508,20037508,20037508),
  restrictedExtent: new OpenLayers.Bounds(3830412.3607388, 3160212.4968564, 6178557.8692412, 4657155.2585266),
  controls: [new OpenLayers.Control.PanZoomBar(), new OpenLayers.Control.Navigation()]
}

map = new OpenLayers.Map('map2', options);

/**
 * LAYERS
 */

map.addLayer(
  new OpenLayers.Layer.MapBox('World Light', 
  {
    layername: 'world-light',
    serverResolutions: [156543.0339,
      78271.51695,
      39135.758475,
      19567.8792375,
      9783.93961875,
      4891.96980938,
      2445.98490469,
      1222.99245234,
      611.496226172,
      305.748113086,
      152.874056543,
      76.4370282715,
      38.2185141357,
      19.1092570679,
      9.55462853394,
      4.77731426697,
      2.38865713348,
      1.19432856674,
      0.597164283371],

    resolutions: [
      4891.96980938,
      2445.98490469,
      1222.99245234,
      611.496226172]
    }
  ));
 

var cities = new OpenLayers.Layer.Vector("Cities KML", {
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
    protocol: new OpenLayers.Protocol.HTTP({
        url: "/get_kml/",
        format: new OpenLayers.Format.KML({
            extractStyles: true,
            extractAttributes: true
        })
    })
});

map.addLayer(cities);
/*

var reports = new OpenLayers.Layer.Vector("KML", {
    projection: map.displayProjection,
    strategies: [new OpenLayers.Strategy.Fixed()],
    protocol: new OpenLayers.Protocol.HTTP({
        url: "/kml/reports",
        format: new OpenLayers.Format.KML({
            extractStyles: true,
            extractAttributes: true
        })
    })
});

map.addLayer(reports);

var areas = new OpenLayers.Layer.Vector("Areas KML", {
    projection: map.displayProjection,
    strategies: [new OpenLayers.Strategy.Fixed()],
    protocol: new OpenLayers.Protocol.HTTP({
        url: "/kml/areas",
        format: new OpenLayers.Format.KML({
            extractStyles: true,
            extractAttributes: true
        })
    })
});

map.addLayer(areas);
*/

/**
 * CONTROLS
 */

function onPopupClose(evt) {
  select.unselectAll();
}

function onFeatureSelect(event) {
  var feature = event.feature;
  // Since KML is user-generated, do naive protection against
  // Javascript.
  var content = "<div class='ol-popup-name'>" + 
    feature.attributes.name + 
    "</div><div class='openlayers-tooltip-description'>" + 
    feature.attributes.description + "</div>";
  popup = new OpenLayers.Popup.FramedCloud("stick", 
  feature.geometry.getBounds().getCenterLonLat(),
  new OpenLayers.Size(100,100),
  content,
  null, true, onPopupClose);
  feature.popup = popup;
  map.addPopup(popup);
}

function onFeatureUnselect(event) {
  var feature = event.feature;
  if(feature.popup) {
    map.removePopup(feature.popup);
    feature.popup.destroy();
    delete feature.popup;
  }
}

cities.events.on({
    "featureselected": onFeatureSelect,
    "featureunselected": onFeatureUnselect
});

reports.events.on({
    "featureselected": onFeatureSelect,
    "featureunselected": onFeatureUnselect
});

select = new OpenLayers.Control.SelectFeature([reports, cities]);
map.addControl(select);
select.activate();

// Default LayerSwitcher on Map
// map.addControl(new OpenLayers.Control.LayerSwitcher());

// Custom BlockSwitcher attached to DOM element
OpenLayersPlusBlockswitcher.hattach($('.openlayers-blockswitcher'), map);

map.zoomTo(1);
