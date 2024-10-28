// map class initialize
var map = L.map('map').setView([-7.205302081531848, 109.06230926513673], 12);
map.zoomControl.setPosition('topright'); //set position zoom control to topright "by default topleft"

// adding osm layer
var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png')

var ewi = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');

const apiKey = "AIzaSyDpX2A-VIf4owRpMDeuf4gaIQHREBrWlC0";
var roadmapLayer = L.tileLayer(`https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}&key=${apiKey}`);
var satelliteLayer = L.tileLayer(`https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}&key=${apiKey}`);
var hybridLayer = L.tileLayer(`https://mt1.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}&key=${apiKey}`).addTo(map);
var terrainLayer = L.tileLayer(`https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}&key=${apiKey}`);


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
    'Maps Road Map': roadmapLayer,
    'Maps Satellite': satelliteLayer,
    'Maps Hybrid': hybridLayer,
    'Maps Terrain': terrainLayer,
    'Open Street Map': osm,
    'Esri World Imagery': ewi,
}
