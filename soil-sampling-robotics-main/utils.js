var map;
var markers = [];
var currentlocation = [];
var currentlocationB = [];
var currentlocationC = [];
var i;
function initialize(){
	new QWebChannel(qt.webChannelTransport, function (channel) {
        window.backend = channel.objects.backend;
    });
    map = L.map('map').setView([14.690177143345668, 120.54893374443054], 16);
	
    //L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
    //    maxZoom: 18
    //}).addTo(map);
	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 30,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoieHlwaGVyMDciLCJhIjoiY2tvMDA3YXJnMGF3YTJvcDRwMGp5ODhzNCJ9.Xz0uBoVH1aiqe7b12qkPsw'
}).addTo(map);
	//Print coordinates of the mouse
        map.on('click', function(e) {
            document.getElementById('coords').innerHTML = e.latlng.lat + ', ' + e.latlng.lng  ;
            backend.pointClicked(e.latlng.lat, e.latlng.lng);
			var drilllocIcon = L.icon({
    iconUrl: 'drillloc.png',
   
    iconSize:     [30, 30], // size of the icon
    
    iconAnchor:   [22, 40], // point of the icon which will correspond to marker's location
   
    popupAnchor:  [-7, -40] // point from which the popup should open relative to the iconAnchor
});
			var marker = L.marker([e.latlng.lat, e.latlng.lng,markers.length],{icon: drilllocIcon}).addTo(map);
			
			coordinatedisp=e.latlng.lat.toString()+","+e.latlng.lng.toString()+","+markers.length.toString()
			

          marker.bindPopup(coordinatedisp, 50);
          marker.openPopup();
		  markers[markers.length] = marker;
		  
        });
		
		
 
}

function Reset(){

for (i = 0; i < markers.length; i++)
{
map.removeLayer(markers[i]);
delete markers[i];
}
markers = []
}

function robotgpsA(lat,lng){
if(	currentlocation.length>0)
{map.removeLayer(currentlocation[0]);
delete currentlocation[0];
}
var robotAIcon = L.icon({
    iconUrl: 'robotA.png',
  
    iconSize:     [38, 60], // size of the icon
   
    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    
    popupAnchor:  [0, -70] // point from which the popup should open relative to the iconAnchor
});
map.panTo(L.latLng(lat, lng));
coordinatedisp=lat.toString()+","+lng.toString()
var markerl = L.marker([lat, lng],{icon: robotAIcon}).addTo(map);
markerl.bindPopup("Mobile Robot A", 50);
markerl.openPopup();
currentlocation[0] = markerl;
}

function robotgpsB(lat,lng){
if(	currentlocationB.length>0)
{map.removeLayer(currentlocationB[0]);
delete currentlocationB[0];
}
var robotBIcon = L.icon({
    iconUrl: 'robotB.png',
  
    iconSize:     [38, 60], // size of the icon
   
    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    
    popupAnchor:  [0, -70] // point from which the popup should open relative to the iconAnchor
});
map.panTo(L.latLng(lat, lng));
coordinatedisp=lat.toString()+","+lng.toString()
var markera = L.marker([lat, lng],{icon: robotBIcon}).addTo(map);
markera.bindPopup("Mobile Robot B", 50);
markera.openPopup();
currentlocationB[0] = markera;
}

function robotgpsC(lat,lng){
if(	currentlocationC.length>0)
{map.removeLayer(currentlocationC[0]);
delete currentlocationC[0];
}
var robotCIcon = L.icon({
    iconUrl: 'robotC.png',
  
    iconSize:     [38, 60], // size of the icon
   
    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    
    popupAnchor:  [0, -70] // point from which the popup should open relative to the iconAnchor
});
map.panTo(L.latLng(lat, lng));
coordinatedisp=lat.toString()+","+lng.toString()
var markerb = L.marker([lat, lng],{icon: robotCIcon}).addTo(map);
markerb.bindPopup("Mobile Robot C", 50);
markerb.openPopup();
currentlocationC[0] = markerb;
}