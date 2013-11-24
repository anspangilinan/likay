$(document).ready(function(event) {
    var options =  {dragging: false, touchZoom: false, scrollWheelZoom: false}
        map = L.map('map', options);

    map.setView([11.6722, 122.9627], 5);

    $("a[title='A JS library for interactive maps'").text("Likay");

    L.tileLayer('http://{s}.tile.cloudmade.com/API-key/997/256/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
        maxZoom: 18
    }).addTo(map);

    $("select[name='city-filter']").change(function(event) {
        var $selected = $(this).find(":selected"),
            latitude = $selected.data('latitude'),
            longitude = $selected.data('longitude'),
            weatherStatus = $selected.data('weather-status');

        map.setView(latitude, longitude, 8.3);
    });
});