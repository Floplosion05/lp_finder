function clamp(number, min, max) {
    return Math.max(min, Math.min(number, max));
}

function mobileAndTabletCheck() {
    let check = false;
    (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
    return check;
};

var map = L.map('map', {
        	            zoomControl: false,
                        scrollWheelZoom: false
});

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

Esri_WorldImagery.addTo(map);
map.dragging.disable();
map.touchZoom.disable();
map.doubleClickZoom.disable();
map.scrollWheelZoom.disable();
map.boxZoom.disable();
map.keyboard.disable();
if (map.tap) map.tap.disable();
document.getElementById('map').style.cursor='default';
L.DomEvent.disableScrollPropagation(document.getElementById('map'))

var iconOptions = {
	iconUrl: 'static/images/focus_3.png',
	iconSize: [75, 75]
}

var customIcon = L.icon(iconOptions);

var markerOptions = {
	icon: customIcon
}

var lat = document.getElementById("lat").textContent;
var long = document.getElementById("long").textContent;

var marker = L.marker([lat, long], markerOptions).addTo(map);
document.getElementsByClassName('leaflet-control-attribution')[0].style.display = 'none';
function mapZoom() { 
    console.log("test1")
    map.setView([lat, long], 12);
    map.flyTo([lat, long], 16, {
        animate: true,
        duration: 1.5
    });
    console.log("test2")
}
mapZoom();
/*
if (!mobileAndTabletCheck()) {
    setInterval(function () {
        const map_elem = document.getElementById('map');
        map_elem.style.opacity = clamp(map_elem.style.opacity - 0.1,0.1,1);
    }, 200);
}

if (!mobileAndTabletCheck()) {
    const map_elem = document.getElementById('map');
    window.addEventListener("mousewheel", (event) => {
        map_elem.style.opacity = clamp(map_elem.style.opacity - (event.deltaY / 10)/100,0,1);
    }, true);
}
*/

//Text Glitch Effect

const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

let interval = null;

document.addEventListener('DOMContentLoaded', function() {
    elem = document.getElementById("title");
    let iteration = 0;
    
    clearInterval(interval);
    
    interval = setInterval(() => {
        elem.innerText = elem.innerText
        .split("")
        .map((letter, index) => {
            if(index < iteration) {
                return elem.dataset.value[index];
            }
            
            return letters[Math.floor(Math.random() * 26)]
        })
        .join("");
    
        if(iteration >= elem.dataset.value.length){ 
            clearInterval(interval);
        }
    
    iteration += 1 / 4;
    }, 30);
});

let sections = gsap.utils.toArray("section"),
currentSection = sections[0];
gsap.defaults({overwrite: 'auto', duration: 0.3});
gsap.set("body", {height: (sections.length * 100) + "%"});

sections.forEach((section, i) => {
    ScrollTrigger.create({
        start: () => (i - 0.5) * innerHeight,
        end: () => (i + 0.5) * innerHeight,
        onToggle: self => self.isActive && setSection(section)
    });
});


function setSection(newSection) {
  if (newSection !== currentSection) {
    gsap.to(currentSection, {scale: 0.9, autoAlpha: 1})
    gsap.to(newSection, {scale: 1, autoAlpha: 1});
    currentSection = newSection;
    if (ScrollTrigger.getAll()[0].isActive) {
        map.setView([lat, long], 12, {animate: false});
        map.flyTo([lat, long], 16, {
            animate: true,
            duration: 1.5
        });
    }
  }
}
