var map;
var home = [42.70, 23.32];

function initMap() {
    map = new L.Map("map", {
        center: new L.LatLng(home[0], home[1]),
        zoom: 12
    });
	
    // var origLayer = map.addLayer(new L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.{ext}', {
	// 	attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	// 	subdomains: 'abcd',
	// 	minZoom: 0,
	// 	maxZoom: 20,
	// 	ext: 'png'
	// }));
	// var origLayer = map.addLayer(new L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
	// 	maxZoom: 17,
	// 	attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
	// }));
	var origLayer = map.addLayer(new L.tileLayer('https://{s}.tile.openstreetmap.se/hydda/full/{z}/{x}/{y}.png', {
		maxZoom: 18,
		attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
	}));
}

function add_row(next) {
	var result = $('#row-template').clone();
	$('.name', result).text(next.name);
	$('.lat', result).text(next.latitude);
	$('.long', result).text(next.longitude);

    var marker = L.marker([next.latitude,next.longitude]).addTo(map).bindPopup(next.name);
	$('#table-body').append(result);
}

function read(data) {
	$('#table-body').html('<tbody id="table-body"></tbody>');		    				
	var locs = JSON.parse(data).result;
	if (locs.length == 1) {
		$('#latitude').val(locs[0].latitude);
		$('#longitude').val(locs[0].longitude);
		
		map.panTo(new L.LatLng(locs[0].latitude, locs[0].longitude));	
	}
	for (next of locs) {
		add_row(next);
	}		
}

function clear() {
	map.panTo(new L.LatLng(home[0], home[1]));
	return $.ajax({url:"/at", success: read, method: "GET"});
}

function init() {
	initMap();

	clear();

	$('#name').on('click', clear);


	// Do not submit form on enter
	$('#name').on('keydown', function(e){
		if (e.keyCode == 13) {
			e.preventDefault();
		}
	});

	$('#name').on('keyup', function(e){
		if (e.keyCode == 13) {
			e.preventDefault();
			// console.log($('#name').val());
			if ($('#name').val().length > 0) {
				$.ajax({url:"/where/" + $('#name').val(), success: read, method: "GET"});
			}
		}
	});

}

$(document).ready(init);
