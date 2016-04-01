#!/usr/bin/env python 

from lxml import html 
import requests 
import re # Regular expressions 
import json


states = {}
with open('state_info.json') as data_file: 
    states = json.load(data_file)




# Get a list of purely the towns where physician data exists for a given state 
def towns_of_physicians(state, class_name):
	page = requests.get("http://www1.salary.com/" + state + "/Physician-Hospitalist-salary.html")
	tree = html.fromstring(page.content)
	places = tree.xpath('//li[@class="' + class_name + '"]/a/span/text()')
	for i in range(0, len(places)):
		arr = places[i].split(',')
		places[i] = arr[0]
	return places




# Obtains the median value of a certain town in a certain state 
def get_median_value_of_town(state, town):
	url = "http://www1.salary.com/" + state + "/" + town + "/Physician-Hospitalist-salary.html"
	print url
	page = requests.get(url)
	tree = html.fromstring(page.content)
	median = tree.xpath('//span[@id="label-mediansalary"]/text()')
	print median
	if len(median) > 0: 
		median[0] = median[0].split(' ')[1]
		return median[0]
	else: 
		return None

def make_salary_json(states, class_name):
	result = []
	for state_tuple in states:
		state_json = {}
		state = state_tuple['name']
		state_json['state'] = state 
		state_json['state_towns'] = []
		state_places = towns_of_physicians(state, class_name)
		for place in state_places: 
			place_json = {}
			place_json['place_name'] = place
			place_json['median_salary'] = get_median_value_of_town(state_tuple['abbreviation'], place)
			if place_json['median_salary'] != None: 
				state_json['state_towns'].append(place_json)
		result.append(state_json)
	return result 


def write_json(myJSON, json_name): 
	with open(json_name + '.json', 'w') as outfile: 
		json.dump(myJSON, outfile)


other_states = [
    {
        "name": "Alaska",
        "abbreviation": "AK"
    },
    {
      	"name": "California",
      	"abbreviation": "CA"
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
        "name": "Hawaii",
        "abbreviation": "HI"
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
        "name": "New Hampshire",
        "abbreviation": "NH"
    },
    {
        "name": "New Jersey",
        "abbreviation": "NJ"
    },
    {
        "name": "Rhode Island",
        "abbreviation": "RI"
    }
]


 #write_json(make_salary_json(states, "collapeslink collapeslinks-adjicon collapeslinks-red"), 'salary_info')

write_json(make_salary_json(other_states, "collapeslink collapeslinks-adjicon collapeslinks-green"), 'other_salary_info')





