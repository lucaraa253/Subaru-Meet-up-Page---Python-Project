let map;
// const location = "{{meet.location}}";
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 34.0522, lng: -118.2437 },
    zoom: 8,
    });

}