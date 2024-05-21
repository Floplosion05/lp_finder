var defaultMarker = L.AwesomeMarkers.icon({
    markerColor: 'darkblue'
});

var industryMarker = L.AwesomeMarkers.icon({
    icon: 'gear-wide-connected',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var hotelMarker = L.AwesomeMarkers.icon({
    icon: 'buildings',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var educationalMarker = L.AwesomeMarkers.icon({
    icon: 'book',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var medicalMarker = L.AwesomeMarkers.icon({
    icon: 'capsule',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var militaryMarker = L.AwesomeMarkers.icon({
    icon: 'crosshair',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var bunkerMarker = L.AwesomeMarkers.icon({
    icon: 'shield-lock',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var houseMarker = L.AwesomeMarkers.icon({
    icon: 'house',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var religiousMarker = L.AwesomeMarkers.icon({
    icon: 'yin-yang',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var entertainmentMarker = L.AwesomeMarkers.icon({
    icon: 'cash-coin',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var trafficMarker = L.AwesomeMarkers.icon({
    icon: 'car-front',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var agricultureMarker = L.AwesomeMarkers.icon({
    icon: 'flower1',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var ruinsMarker = L.AwesomeMarkers.icon({
    icon: 'hammer',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var miscMarker = L.AwesomeMarkers.icon({
    icon: 'compass',
    prefix: 'bi',
    markerColor: 'darkblue'
});

var categories = [
    "Industrie",
    "Hotel",
    "Schule",
    "Medizinisch",
    "Militär",
    "Bunker",
    "Haus",
    "Religiös",
    "Unterhaltung",
    "Verkehr",
    "Landwirtschaft",
    "Ruine",
    "Sonstiges"
];

var awesomemarkers=[defaultMarker, industryMarker, hotelMarker, educationalMarker, medicalMarker, militaryMarker, bunkerMarker, houseMarker, religiousMarker, entertainmentMarker, trafficMarker, agricultureMarker, ruinsMarker, miscMarker]

var map = L.map('map');
map.locate({setView: true, maxZoom: 20});
map.addControl(new L.Control.Fullscreen());

var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    noWrap: true,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    subdomains: ['a','b','c']
})//.addTo(map);

var osmHOT = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    noWrap: true,
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors, Tiles style by Humanitarian OpenStreetMap Team hosted by OpenStreetMap France',
    subdomains: ['a','b','c']
});

var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    noWrap: true,
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    bounds: [
        [-90, -180],
        [90, 180]
    ]
});

var baseMaps = {
    "Terrain": osm,
    "Humanitarian": osmHOT,
    "Satellite": Esri_WorldImagery
};

var layerControl = L.control.layers(baseMaps).addTo(map);
Esri_WorldImagery.addTo(map);
L.control.scale().addTo(map);
map.doubleClickZoom.disable();
document.getElementsByClassName("leaflet-control-attribution")[0].style.display = "none";

const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

let interval = null;

map.on("popupopen", function(e) {
    elem = document.getElementById(e.popup._source._popup._content.split('id="')[1].split('"')[0]);
    
    let iteration = 0;
    
    clearInterval(interval);
    
    interval = setInterval(() => {
        elem.innerHTML = elem.innerHTML
        .split("")
        .map((letter, index1) => {
            if(index1 < iteration) {
                return elem.dataset.value[index1];
            }
            
            return letters[Math.floor(Math.random() * 26)]
        })
        .join("");
    
        if(iteration >= elem.dataset.value.length){ 
            clearInterval(interval);
        }
    
    iteration += 1 / 2;
    }, 30);
});