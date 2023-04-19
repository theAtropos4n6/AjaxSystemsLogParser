import re
import json
import os
import datetime

def parse_intel(first_dict):
	#second_dict = {"Date":{"User-ID":"","FirstName":"","LastName":"","Phone":"","Email":"","RegistrationTime":"","UserIndex":""}}
	second_dict = {}
	unix_time_str = None
	for k,v in first_dict.items():
		lines = v.split('\n')
		prev_line = None #holds previous line value for comparing purposes
		second_dict[k] = {}
		for line in lines: #iterate through the multiline string that is the value of the dict and extract intel
			if prev_line == "users{" and "id:" in line:
				user_id = line[4:-1]
				second_dict[k]["User-ID"] = user_id
			elif prev_line == "first_name{" and "value:" in line:
				first_name = line[7:-1]
				second_dict[k]["FirstName"] = first_name
			elif prev_line == "last_name{" and "value:" in line:
				last_name = line[7:-1]
				second_dict[k]["LastName"] = last_name
			elif prev_line == "phone{" and "value:" in line:
				phone = line[7:-1]
				second_dict[k]["Phone"] = phone
			elif prev_line == "email{" and "value:" in line:
				email = line[7:-1]
				second_dict[k]["Email"] = email
			elif prev_line == "registration_time{" and "seconds:" in line:
				unix_time_str = line[8:]
				unix_time = float(unix_time_str)
				registration_time = datetime.datetime.utcfromtimestamp(unix_time)
				second_dict[k]["RegistrationTime"] = f'{registration_time} [UTC]'
			elif prev_line == "user_index{" and "value:" in line:
				user_index = line[6:]
				second_dict[k]["UserIndex"] = user_index
			prev_line = line
	return second_dict

def parse_android_logfile(logfile):
	date_pattern=r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}:\d{3}'
	temp_dir = {}
	report_dir = {"4":{},"5":{}}
	with open(logfile,'r',encoding='utf-8') as log:
		counter = 0
		results_four = {}
		results = {}
		start_found = 0
		start_pattern = ["{objRoomId=","snapshot {"]
		for i in log:
			if start_found == 1:
				if re.match(date_pattern,i):
					result_entry = log_entry.rstrip('}\n')
					result_entry = result_entry.replace("}\n","")
					result_entry = result_entry.replace(" ","")
					results[log_cur_date] = result_entry
					start_found = 0				
				log_entry+=i

			if start_found == 0:
				if re.match(date_pattern,i):
					log_cur_date = str(re.match(date_pattern,i).group(0)) #holds the date of the latest entry prior to find the result string
				if start_pattern[1] in i:
					start_found = 1
					counter+=1
					log_entry = ""

			if start_pattern[0] in i:
				log_cur_date = str(re.match(date_pattern,i).group(0))
				#this block fixes the json so as to be a valid json file and to be loaded into json loads
				json_str = i.split(') : ',1)[-1]
				json_str = json_str.rstrip('\n')
				json_str = json_str.replace("=",':')
				json_str = json_str.replace(":",'":"')
				json_str = json_str.replace("{",'{"')
				json_str = json_str.replace(", ",'","')
				json_str = json_str.replace(':",',':"",')
				json_str = json_str.replace(':"}',':""}')
				json_dict = json.loads(json_str)
				results_four[log_cur_date] = json_dict

		report_dir["4"].update(results_four)		
		temp_dir = parse_intel(results)
		report_dir["5"].update(temp_dir)

	return report_dir


def parse_logfile_dir(input_file_dir): #returns dict_log
	dir_dict = {}
	dict_log ={}
	for file in os.listdir(input_file_dir):
		if " (build #" in file and file.startswith('v '):
			try:
				dict_log = parse_android_logfile(input_file_dir+"\\"+file)
				dir_dict[file] = dict_log
			except Exception as e:
				print(f"Error occured while reading logfiles directory. The error message was {e}")
	return dir_dict