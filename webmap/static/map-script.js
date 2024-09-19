
// Nata,  Sep 19 2024 generated (new)
const mapbox_access_token_dev = "pk.eyJ1IjoibmVta292YSIsImEiOiJjbTE5Mm12ZnIwMjFsMnFyMWR6M2pucHJxIn0.CN8ZPiPgnO-JSSfhBhJUtw";
const map_projection_definition_conic = {
    name: 'albers',
    center: [10, 48],
    parallels: [38, 40]
};

mapboxgl.accessToken = mapbox_access_token_dev;
const map = new mapboxgl.Map({
    container: 'map',   // container ID
    center: [9.5, 42.5],     // starting position [lng, lat]
    zoom: 4,     // starting zoom
    projection: 'winkelTripel'    // replace with map_projection_definition_conic for conic
});