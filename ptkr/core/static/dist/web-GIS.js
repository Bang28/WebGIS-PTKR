// leaflet search 
L.Control.geocoder({
    position: 'topleft'
}).addTo(map);

// zoom to layer function
$('.zoom-to-layer').click(function () {
    map.setView([-7.050, 108.891], 10)
});

// get locate
L.control.locate({
    position: 'topright',
    strings: {
        title: "Tampilkan lokasi anda"
    },
    locateOptions: {
        enableHighAccuracy: true
    }
}).addTo(map);