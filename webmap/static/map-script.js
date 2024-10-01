// const GEOJSON_GZ_URL = "https://storage.googleapis.com/food-n-climate-data/public/eu27_communes_indicators.geojson.gz";
const GEOJSON_GZ_URL =  'static/eu27_communes_indicators.geojson.gz'
const NUTS3_SOURCE_ID = 'nuts3-indicators';
const NUTS3_LAYER_ID = 'nuts3-indicators';

const fieldsToDisplay = [
    'PDO_all',
    'PDO_meat',
    'PDO_cheese',
    'PDO_oils_and_fats',
    'PDO_fruits_vegetables_cereals',
    'I_HNVF',
    'I_natura_2000',
    'I_CLC_richness',
    'I_semi_natural_farmland',
    'I_UNESCO_sites',
    'I_tourism_beds',
    'I_population_density',
    'I_median_age',
    'I_5year_migration_rate',
    'I_GDP_pc',
    'I_organic_farmland',
    'I_avg_farm_size',
    'I_unemployment_20_64',
]

class MapManager {

    geojson = undefined

    constructor(map) {
        this.map = map;
    }

    async fetchAndUnzipJSON(url) {

        console.log('Performing request to Google Drive');

        // Fetch the zipped file
        const response = await fetch(url, {
                // mode: 'no-cors',
                method: 'GET',
                headers: {
                    'accept': 'application/gzip',
                    'Referer': 'researcher',
                    'Accept-Encoding': 'identity'  // Prevent automatic gzip decompression by the browser
                }
            }
        );

        const respLength =  parseInt(response.headers.get('content-length'));
        const respLengthKB = Math.floor(respLength / 1024) + ' KB';
        response.ok ? console.log('Received size ' + respLengthKB) : () => {
            throw new Error(
                'Returned code ' + response.status + ' content-length = ' + respLengthKB
            );
        };

        const arrayBuffer = await response.arrayBuffer(); // Get the data as ArrayBuffer

        // Decompress using pako
        const decompressedData = pako.ungzip(new Uint8Array(arrayBuffer), { to: 'string' });

        // Parse the decompressed string into a JSON object
        console.log("JSON Object received:", JSON.parse(decompressedData).features.length , ' features');
        return JSON.parse(decompressedData);
    }

    async loadGeoJSONData() {
        // receives FeatureCollection
        this.geojson = await this.fetchAndUnzipJSON(GEOJSON_GZ_URL);

        // populate feature ids
        let counter = 0;
        this.geojson.features.forEach(feature => {
            feature.id = counter++;
        });

        // featureProperties = Object.keys(this.geojson.features[0].properties);
        // featureProperties = featureProperties.filter( ( el ) => {
        //     return !toRemove.includes( el );
        // } );

        return this.geojson;
    };

}


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

manager = new MapManager(map);
manager.loadGeoJSONData().then((geojson) => {
    map.addSource(NUTS3_SOURCE_ID, {
        type: 'geojson',
        data: geojson
    });

    map.addLayer({
        'id': NUTS3_LAYER_ID,
        'type': 'fill',
        'minzoom': 4,
        'source': NUTS3_SOURCE_ID, // reference the data source
        'layout': {},
        'paint': {
            'fill-color': '#0080ff', // blue color fill
            'fill-opacity': 0.5
        }
    });
});

// Create a popup, but don't add it to the map yet.
const popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
});


map.on('mousemove', NUTS3_LAYER_ID, (e) => {
    // Change the cursor style as a UI indicator.
    map.getCanvas().style.cursor = 'pointer';

    const feature = e.features[0];

    // Copy coordinates array.
    const coordinates = feature.geometry.coordinates.slice();
    const description = "<p>" + fieldsToDisplay.map((field, i) => {
        return field + ': ' + feature.properties[field];
    }).join("</p><p>") + "</p>";

    // Populate the popup and set its coordinates
    // based on the feature found.
    popup.setLngLat(e.lngLat).setHTML(description).addTo(map);
});

// map.on('mouseleave', NUTS3_SOURCE_ID, () => {
//     map.getCanvas().style.cursor = '';
//     popup.remove();
// });

// const availableProperties = [];
// var currentProperty;
//
// function switchToProperty(prop) {
//     if (!fieldsToDisplay.includes(prop)) {
//         throw Error('Property "' + prop + '" not found.');
//     }
//
//     swatch.addEventListener('click', () => {
//         map.setPaintProperty(layer.value, 'fill-color', color);
//     });
// }