// full screen map view
var mapId = document.getElementById('map');
function fullScreenView() {
    if (document.fullscreenElement){
        document.exitFullscreen()
    }else{
        mapId.requestFullscreen();
    }
}

// map print with ext library "leaflet browser print function"
L.control.browserPrint({
    position: 'topright', // default topleft
}).addTo(map)

// leaflet search 
L.Control.geocoder().addTo(map);

// leaflet measure
L.control.measure({
    primaryLengthUnit: 'kilometers',
    secondaryLengthUnit: 'meters',
    primaryAreaUnit: 'sqmeters',
    secondaryAreaUnit: undefined
}).addTo(map);

// zoom to layer function
$('.zoom-to-layer').click(function () {
    map.setView([38.8610, 71.2761], 7)
});