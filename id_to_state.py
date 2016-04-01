import json 

def get_id_text(): 
	the_file = open('./id_state.txt')
	lines = the_file.readlines() 
	the_file.close
	return lines

def write_json(myJSON, json_name): 
	with open(json_name + "_" + '.json', 'w') as outfile: 
		json.dump(myJSON, outfile)


def gen_json(): 
	theList = get_id_text()
	for i in range(0, len(theList)): 
		theList[i] = theList[i].replace("\n", "")
	result_dic = {}
	j = 1
	while("America Samoa" not in theList[j]): 
		line_array = theList[j].split("\t")
		result_dic[line_array[0]] = { "state": line_array[2], "abbrev": line_array[1] }
		j+=1


	write_json(result_dic, "id_to_state")

gen_json() 




