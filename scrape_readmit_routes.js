// TO RUN THIS 
// Must have PhantomJS installed 
// (this thing is honestly so cool I'm so happy I got to use it)
// `phantomjs readmit.js` (involves $PATH variable or alias for phantomjs)


// Test URL 
var url = "http://www.hospital-data.com/dirs/Massachusetts-Hospitals.html"

// Used to build on when progressing through scraping the information 
var baseURL = "http://www.hospital-data.com"

// Get all the URLs w/data
var paths = []

// State information
var states = [
    {
        "name": "Alabama",
        "abbreviation": "AL"
    },
    {
        "name": "Alaska",
        "abbreviation": "AK"
    },
    {
        "name": "American Samoa",
        "abbreviation": "AS"
    },
    {
        "name": "Arizona",
        "abbreviation": "AZ"
    },
    {
        "name": "Arkansas",
        "abbreviation": "AR"
    },
    {
        "name": "California",
        "abbreviation": "CA"
    },
    {
        "name": "Colorado",
        "abbreviation": "CO"
    },
    {
        "name": "Connecticut",
        "abbreviation": "CT"
    },
    {
        "name": "Delaware",
        "abbreviation": "DE"
    },
    {
        "name": "District Of Columbia",
        "abbreviation": "DC"
    },
    {
        "name": "Federated States Of Micronesia",
        "abbreviation": "FM"
    },
    {
        "name": "Florida",
        "abbreviation": "FL"
    },
    {
        "name": "Georgia",
        "abbreviation": "GA"
    },
    {
        "name": "Guam",
        "abbreviation": "GU"
    },
    {
        "name": "Hawaii",
        "abbreviation": "HI"
    },
    {
        "name": "Idaho",
        "abbreviation": "ID"
    },
    {
        "name": "Illinois",
        "abbreviation": "IL"
    },
    {
        "name": "Indiana",
        "abbreviation": "IN"
    },
    {
        "name": "Iowa",
        "abbreviation": "IA"
    },
    {
        "name": "Kansas",
        "abbreviation": "KS"
    },
    {
        "name": "Kentucky",
        "abbreviation": "KY"
    },
    {
        "name": "Louisiana",
        "abbreviation": "LA"
    },
    {
        "name": "Maine",
        "abbreviation": "ME"
    },
    {
        "name": "Marshall Islands",
        "abbreviation": "MH"
    },
    {
        "name": "Maryland",
        "abbreviation": "MD"
    },
    {
        "name": "Massachusetts",
        "abbreviation": "MA"
    },
    {
        "name": "Michigan",
        "abbreviation": "MI"
    },
    {
        "name": "Minnesota",
        "abbreviation": "MN"
    },
    {
        "name": "Mississippi",
        "abbreviation": "MS"
    },
    {
        "name": "Missouri",
        "abbreviation": "MO"
    },
    {
        "name": "Montana",
        "abbreviation": "MT"
    },
    {
        "name": "Nebraska",
        "abbreviation": "NE"
    },
    {
        "name": "Nevada",
        "abbreviation": "NV"
    },
    {
        "name": "New Hampshire",
        "abbreviation": "NH"
    },
    {
        "name": "New Jersey",
        "abbreviation": "NJ"
    },
    {
        "name": "New Mexico",
        "abbreviation": "NM"
    },
    {
        "name": "New York",
        "abbreviation": "NY"
    },
    {
        "name": "North Carolina",
        "abbreviation": "NC"
    },
    {
        "name": "North Dakota",
        "abbreviation": "ND"
    },
    {
        "name": "Northern Mariana Islands",
        "abbreviation": "MP"
    },
    {
        "name": "Ohio",
        "abbreviation": "OH"
    },
    {
        "name": "Oklahoma",
        "abbreviation": "OK"
    },
    {
        "name": "Oregon",
        "abbreviation": "OR"
    },
    {
        "name": "Palau",
        "abbreviation": "PW"
    },
    {
        "name": "Pennsylvania",
        "abbreviation": "PA"
    },
    {
        "name": "Puerto Rico",
        "abbreviation": "PR"
    },
    {
        "name": "Rhode Island",
        "abbreviation": "RI"
    },
    {
        "name": "South Carolina",
        "abbreviation": "SC"
    },
    {
        "name": "South Dakota",
        "abbreviation": "SD"
    },
    {
        "name": "Tennessee",
        "abbreviation": "TN"
    },
    {
        "name": "Texas",
        "abbreviation": "TX"
    },
    {
        "name": "Utah",
        "abbreviation": "UT"
    },
    {
        "name": "Vermont",
        "abbreviation": "VT"
    },
    {
        "name": "Virgin Islands",
        "abbreviation": "VI"
    },
    {
        "name": "Virginia",
        "abbreviation": "VA"
    },
    {
        "name": "Washington",
        "abbreviation": "WA"
    },
    {
        "name": "West Virginia",
        "abbreviation": "WV"
    },
    {
        "name": "Wisconsin",
        "abbreviation": "WI"
    },
    {
        "name": "Wyoming",
        "abbreviation": "WY"
    }
]


// I used the following StackOverflow post for a general idea regarding how I was to implement this function 
// http://stackoverflow.com/questions/28560393/how-to-navigate-a-paginated-website-with-phantomjs
function clickElement(element) {
	var event = document.createEvent('MouseEvents'); 
	event.initMouseEvent('click', true, true, window, 1, 0, 0); 
	element.dispatchEvent(event); 
}


function crawl(i, click, link_array) {
	// page.render(i + ".png"); 
	var content = page.content;
	var listTho = page.evaluate(function(func) {
		var element = document.querySelector('#linkstable_next');
		link = element.children[0]; 
		
		// Taken from this thread: 
		// http://stackoverflow.com/questions/5898656/test-if-an-element-contains-a-class
		if ((' ' + element.className + ' ').indexOf(' disabled ') > -1) {
			return false;  
		}	


		arr = []
		var j = 0; 
		var linksOdd = document.querySelectorAll('tr.odd td a'); 
		for (j = 0; j < linksOdd.length; j++) {
			arr.push(linksOdd[j].getAttribute('href')); 
		}

		var linksEven = document.querySelectorAll('tr.even td a'); 
		for (j = 0; j < linksEven.length; j++) {
			arr.push(linksEven[j].getAttribute('href')); 
		}


		func(link);

		return arr; 

	}, click, link_array); 


	// End case 
	if (listTho == false) {
		return; 
	} 

	
	for (var j = 0; j < listTho.length; j++) {
		console.log(listTho[j]); 
	}
	
	crawl(++i, click, link_array); 

}




function siftThroughPages(url, page) {

	page.open(url, function(status) {
		if (status !== 'success') {
			phantom.exit(); 
		} else { 
			crawl(1, clickElement, paths); 
		}
	});  
}




// BULK WORK 

var page = require('webpage').create();


function recursiveSift(i, page) {

	if (i >= states.length) {
		phantom.exit(); 
		return; 
	}

	var state_name = states[i]["name"]; 
	state_name = state_name.replace(" ", "-"); 
	var URL = "http://www.hospital-data.com/dirs/" + state_name + "-Hospitals.html"; 
	console.log(state_name); 
	siftThroughPages(URL, page); 
	setTimeout(function(){
		recursiveSift(++i, page); 
	}, 10000); 


}


recursiveSift(0, page); 









