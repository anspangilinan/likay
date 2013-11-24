$(document).ready(function(event) {
    var options = {dragging: false, touchZoom: false, scrollWheelZoom: false, keyboard: false, zoomControl: false},
        map = L.map('map', options).setView([11.6722, 122.9627], 5),
        cloudmadeUrl = 'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.jpg',
        subDomains = ['1','2','3','4'],
        cloudmade = new L.TileLayer(cloudmadeUrl, {subdomains: subDomains, maxZoom: 18});

    map.addLayer(cloudmade);

    $("a[title='A JS library for interactive maps'").text("Likay");


    $("select[name='city-filter']").change(function(event) {
        var $selected = $(this).find(":selected"),
            name = $selected.data('name'),
            latitude = $selected.data('latitude'),
            longitude = $selected.data('longitude'),
            zoom = $selected.data('zoom'),
            subscribers = $selected.data('subscribers'),
            weatherStatus = $selected.data('weather-status');

        map.setView([latitude, longitude]);
        map.setZoom(zoom)

        var marker = L.marker([latitude, longitude]).addTo(map),
            cText = "<b>" + name + "</b>",
            wsText = weatherStatus,
            sText = "Subscribers: " + subscribers;

        marker.bindPopup(cText + "<br />" + wsText + "<br/>" + sText).openPopup();
    });
});