// map class initialize
var map = L.map('map').setView([-1.5387473, 118.4170327], 5);
map.zoomControl.setPosition('topright'); //set position zoom control to topright "by default topleft"

// adding osm layer
var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var ewi = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

// add scale
L.control.scale({
    position: 'bottomright' //set position scale to bottom right "by default bottom left"
}).addTo(map);

// map coordinate display
map.on('mousemove', function (e) {
    $('.coordinate').html('Lat: ' + e.latlng.lat + ' Long: ' + e.latlng.lng)
});

// leaflet layer control
var baseMaps = {
    'OSM': osm,
    'Esri World Imagery': ewi,
}
