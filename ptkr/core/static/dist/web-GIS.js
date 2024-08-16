// leaflet search 
L.Control.geocoder({
    position: 'topleft'
}).addTo(map);

// zoom to layer function
$('.zoom-to-layer').click(function () {
    map.setView([-7.204620857883746, 109.0623553088576], 14)
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