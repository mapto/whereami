var map;
var home = [42.70, 23.32];

function initMap() {
    map = new L.Map("map", {
        center: new L.LatLng(home[0], home[1]),
        zoom: 12
    });
	
    // var origLayer = map.addLayer(new L.StamenTileLayer("toner", {
    //     detectRetina: true
    // }));
	var origLayer = map.addLayer(new L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
		maxZoom: 17,
		attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
	}));	
}

function isIterable(obj) {
  // checks for null and undefined
  if (obj == null) {
    return false;
  }
  return typeof obj[Symbol.iterator] === 'function';
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
	if (locs.length > 1) {
		for (next of locs) {
			add_row(next);
		}		
	} else {
		add_row(locs);

		$('#latitude').val(locs.latitude);
		$('#longitude').val(locs.longitude);
		
		map.panTo(new L.LatLng(locs.latitude, locs.longitude));	
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
