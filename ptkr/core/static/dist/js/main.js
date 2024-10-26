// map class initialize
var map = L.map('map').setView([-7.205302081531848, 109.06230926513673], 12);
map.zoomControl.setPosition('topright'); //set position zoom control to topright "by default topleft"

// adding osm layer
var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

var ewi = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');

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
    'Open Street Map': osm,
    'Esri World Imagery': ewi,
}
