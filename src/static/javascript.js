// Submits a post request to the server.
function submission(event, method, parent, output) {
	event.preventDefault();
	var request = {
		'accident'		: obtain(parent, 'accident'),
		'aggregation'	: obtain(parent, 'aggregation'),
		'column'		: obtain(parent, 'column'),
		'date'			: obtain(parent, 'date'),
		'day'			: obtain(parent, 'day'),
		'definition'	: obtain(parent, 'definition'),
		'geometry'		: obtain(parent, 'geometry'),
		'lighting'		: obtain(parent, 'lighting'),
		'month'			: obtain(parent, 'month'),
		'method'		: method,
		'row'			: obtain(parent, 'row'),
		'severity'		: obtain(parent, 'severity'),
		'year'			: obtain(parent, 'year'),
	};
	$.ajax ({
		type: 'POST',
		url: '/submission',
		contentType: 'application/json; charset=UTF-8',
		async: false,
		data: request,
		dataType: 'jsonp',
		success: function(response) {
			console.log(response)
			createTable(JSON.parse(response), output);
		}
	});
}

// Extracts value from an input field.
function obtain(parent, name) {
	var value = $('x input[name=y]'.replace('x', parent).replace(
		'y', name)).val();
	$('x input[name=y]'.replace('x', parent).replace('y', name)).val('');
	return value;
}

// Returns a list of values in an object container.
Object.values = function(obj) {
	var values = [];
	for (var key in obj) {
		values.push(obj[key]);
	}
	return values;
}

// Generates an HTML table.
function createTable(obj, selector) {
	$(selector).html('');
	var header$ = $('<tr/>');
	for (var key in obj) {
		header$.append($('<th/>').html(key));
	}
	$(selector).append(header$);
	cols = Object.values(obj)
	rows = Object.values(Object.values(obj)[0])
	for (var i = 0; i < rows.length; i ++) {
		var row$ = $('<tr/>');
		for (var j = 0; j < cols.length; j ++) {
			row$.append($('<td/>').html(
				Object.values(Object.values(obj)[j])[i]));
		}
		$(selector).append(row$);
	}
}

// Loads elements corresponding to tab criteria.
function switchTab(event, tab, img) {
	var i, tabcontent, tablinks;
	if (img) {
		document.body.style.backgroundImage = "url(%s)".replace('%s', img);
	}
	tabcontent = document.getElementsByClassName('tabcontent');
	tablinks = document.getElementsByClassName('tablinks');
	for (i = 0; i < tabcontent.length; i ++) {
		tabcontent[i].style.display = 'none';
		tablinks[i].className = tablinks[i].className.replace(' active', '');
	}
	document.getElementById(tab).style.display = 'block';
	if (event) {
		event.currentTarget.className += ' active';
	}
}

// Loads visualisations corresponding to year criteria.
function switchSubTab(event, tab) {
	var i, tabcontent, tablinks;
	tabcontent = document.getElementsByClassName('subtabcontent');
	tablinks = document.getElementsByClassName('subtablinks');
	for (i = 0; i < tabcontent.length; i ++) {
		tabcontent[i].style.display = 'none';
		tablinks[i].className = tablinks[i].className.replace(' active', '');
	}
	document.getElementById(tab).style.display = 'block';
	event.currentTarget.className += ' active';
}
