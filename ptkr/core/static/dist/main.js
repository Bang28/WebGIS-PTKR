// map class initialize
var map = L.map('map').setView([38.8610, 71.2761], 7);
map.zoomControl.setPosition('topright'); //set position zoom control to topright "by default topleft"

// adding osm layer
var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var ewi = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

// adding marker in the center of map
var singleMarker = L.marker([38.8610, 71.2761])
    .bindPopup('A pretty CSS popup.<br> Easily customizable.')
    .openPopup();

// add scale
L.control.scale({
    position: 'bottomright' //set position scale to bottom right "by default bottom left"
}).addTo(map);

// map coordinate display
map.on('mousemove', function (e) {
    $('.coordinate').html('Lat: ' + e.latlng.lat + ' Long: ' + e.latlng.lng)
});

// geoJson load
// L.geoJSON(data).addTo(map);
var marker = L.markerClusterGroup();
var taji = L.geoJSON(data, {
    onEachFeature: function (feature, layer) {
        layer.bindPopup(feature.properties.name)
    }
});
taji.addTo(marker);
marker.addTo(map); // default 

// leaflet layer control
var baseMaps = {
    'OSM': osm,
    'Esri World Imagery': ewi
}

var overlayMaps = {
    'GeoJSON Marker': marker, // default marker value when i uncomment marker in GeoJso load
    'Single Marker': singleMarker
}

L.control.layers(baseMaps, overlayMaps, {
    collapse: false,
    position: 'topleft', // default topright    
}).addTo(map);