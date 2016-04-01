#!/usr/bin/env python 

from lxml import html 
import requests 
import re # Regular expressions 
import json
import time 
import sys 


# NEED THE TEXT FILE FROM THE JS CRAWLER 
def scrape_hosp_info(): 
	# Open the file 
	theFile = open('./hosp_routes.txt')
	# Read the lines 
	lines = theFile.readlines()
	# Close the file
	theFile.close
	# Print the last line 
	return lines


def compose_readmission_json(theState, mod_val): 
	baseURL = "http://www.hospital-data.com"
	# Get the routes of the hospitals 
	lines = scrape_hosp_info() 
	theState = theState.replace(" ", "-")
	result = []
	i = 0 
	span = len(lines) 
	not_done = True 
	while i < span and not_done: 
		if ".." not in lines[i] and theState in lines[i]: 
			dic = {}
			state = lines[i].replace('\n', '')
			dic['state'] = state 
			dic['hospitals'] = []
			i += 1
			while ".." in lines[i] and i < span: 
				if i%mod_val != 0: 
					print i 
				elif "html" in lines[i]: 
					print i
					time.sleep(10) # Delay for 5 seconds
					page = requests.get(baseURL + lines[i][2:])

					tree = html.fromstring(page.content)

					# Computation to see if the hospital is legit 
					heart_failure = tree.xpath('//div/b[contains(text(), "Readmission Rates from Heart Failure")]/../table/tr/td/text()')
					heart_attack = tree.xpath('//div/b[contains(text(), "Readmission Rates from Heart Attack")]/../table/tr/td/text()')
					pneumonia = tree.xpath('//div/b[contains(text(), "Readmission Rates from Pneumonia")]/../table/tr/td/text()')
					
					if (len(heart_failure) == 0) and (len(heart_attack) == 0) and (len(pneumonia) == 0): 
						i = i + 1 
						continue # Don't need this hospital 

					print lines[i][2:]

					print "Heart Failure Rates"
					print heart_failure
					for j in range(0, len(heart_failure)):
						num = heart_failure[j].replace('%', '')
						heart_failure[j] = float(num)



					print "Heart Attack Rates"
					print heart_attack
					for j in range(0, len(heart_attack)):
						num = heart_attack[j].replace('%', '')
						heart_attack[j] = float(num)



					print "Pneumonia Rates"
					print pneumonia
					for j in range(0, len(pneumonia)):
						num = pneumonia[j].replace('%', '')
						pneumonia[j] = float(num)



					location = tree.xpath('//blockquote/text()')
					location = location[1] # Location is the first element 
					town = location.split(',')[0].replace('\n', '').replace('\r', '')

					print "Town"

					print town 

					mini_dic = {}
					mini_dic['hospital_town'] = town
					mini_dic['heart_failure'] = heart_failure
					mini_dic['heart_attack'] = heart_attack
					mini_dic['pneumonia'] = pneumonia
					dic['hospitals'].append(mini_dic)

				i = i + 1

			result.append(dic)
			not_done = False 

		i = i + 1

	return result 




def write_json(myJSON, json_name, state_name): 
	with open(json_name + "_" + state_name + '.json', 'w') as outfile: 
		json.dump(myJSON, outfile)




desired_state = sys.argv[1]
mod_val = int(sys.argv[2])
print "running"
write_json(compose_readmission_json(desired_state, mod_val), 'readmission_info', desired_state)







