import re
import json
import os

def parse_log_info(results_string):
	results_dict = {}
	log_string_start = results_string.find('index=')
	log_string_finish = results_string.find(")",log_string_start)
	log_string = results_string[log_string_start:log_string_finish]
	log_list = log_string.split(",")
	counter = 1
	for i in log_list:	
		results_dict[counter] = {"index" :"", "logDeviceId":"","logDeviceName":"","logDeviceType":"","logEventType":"","logRoomId":"","logRoomName":"","logTimestamp":"","logTimestampRaw":"","logType":"","objectId":""}
		#index
		start = i.find('index')+7 #index="= = 7 chars
		end = i.find(";",start)
		results_dict[counter]["index"] = i[start:end-1] if start != 6 else ""
		#logdeviceid
		start = i.find('logDeviceId')+12 #logDeviceId= = 12 chars
		end = i.find(";",start)
		results_dict[counter]["logDeviceId"] = i[start:end] if start != 11 else ""
		#logDeviceName
		start = i.find('logDeviceName')+15 #logDeviceId= = 15 chars
		end = i.find(";",start)
		results_dict[counter]["logDeviceName"] = i[start:end-1] if start != 14 else ""
		#logDeviceType
		start = i.find('logDeviceType')+14 #logDeviceType= = 14 chars
		end = i.find(";",start)
		results_dict[counter]["logDeviceType"] = i[start:end] if start != 13 else ""
		if results_dict[counter]["logDeviceType"] == "33":
			results_dict[counter]["logDeviceType"] = "Hub"
		if results_dict[counter]["logDeviceType"] == "2":
			results_dict[counter]["logDeviceType"] = "Motion Sensor"
		if results_dict[counter]["logDeviceType"] == "1":
			results_dict[counter]["logDeviceType"] = "Door Sensor"
		if results_dict[counter]["logDeviceType"] == "11":
			results_dict[counter]["logDeviceType"] = "KeyFob"
		#logEventType
		start = i.find('logEventType')+13 #logEventType= = 12 chars
		end = i.find(";",start)
		results_dict[counter]["logEventType"] = i[start:end] if start != 12 else ""
		#logRoomId
		start = i.find('logRoomId')+10 #logDeviceId= = 12 chars
		end = i.find(";",start)
		results_dict[counter]["logRoomId"] = i[start:end] if start != 9 else ""
		#logRoomName
		start = i.find('logRoomName')+12 #logRoomName= = 12 chars
		end = i.find(";",start)
		results_dict[counter]["logRoomName"] = i[start:end] if start != 11 else ""
		#logTimestamp
		start = i.find('logTimestamp')+14 #logTimestamp= = 14 chars
		end = i.find(";",start)
		results_dict[counter]["logTimestamp"] = i[start:end-1] if start != 13 else ""
		#logTimestampRaw
		start = i.find('logTimestampRaw')+16 #logTimestampRaw= = 16 chars
		end = i.find(";",start)
		results_dict[counter]["logTimestampRaw"] = i[start:end] if start != 15 else ""
		#logType
		start = i.find('logType')+8 #logType= = 8 chars
		end = i.find(";",start)
		results_dict[counter]["logType"] = i[start:end] if start != 7 else ""
		if results_dict[counter]["logType"] in ["7","4"]:
			results_dict[counter]["logType"] = "Green"
		if results_dict[counter]["logType"] == "1":
			results_dict[counter]["logType"] = "Yellow"
		if results_dict[counter]["logType"] == "0":
			results_dict[counter]["logType"] = "Red"
		#objectId
		start = i.find('objectId')+9 #objectId= = 9 chars
		end = i.find(";",start)
		results_dict[counter]["objectId"] = i[start:end] if start != 8 else ""
		#intepreting values
		if results_dict[counter]["logEventType"] == "5":
			results_dict[counter]["logEventType"] = "Hub lid is closed"
		if results_dict[counter]["logEventType"] == "4":
			results_dict[counter]["logEventType"] = "Hub lid is opened"
		if results_dict[counter]["logEventType"] == "1":
			results_dict[counter]["logEventType"] = "External power restored"
		if results_dict[counter]["logEventType"] == "0":
			results_dict[counter]["logEventType"] = "External power failure"
		if results_dict[counter]["logEventType"] == "11":
			results_dict[counter]["logEventType"] = "Hub is online again"
		if results_dict[counter]["logEventType"] == "33":
			if results_dict[counter]["logDeviceType"] == "Hub":
				results_dict[counter]["logEventType"] = "Server connection via Ethernet restored"
			if results_dict[counter]["logDeviceType"] == "Door Sensor":
				results_dict[counter]["logEventType"] = "Closed"
		if results_dict[counter]["logEventType"] == "10":
			results_dict[counter]["logEventType"] = "Hub is offline. Check the network connection."
		if results_dict[counter]["logEventType"] == "32":
			if results_dict[counter]["logDeviceType"] == "Hub":
				results_dict[counter]["logEventType"] = "Server connection via Ethernet lost"
			if results_dict[counter]["logDeviceType"] == "Door Sensor":
				results_dict[counter]["logEventType"] = "Opening detected"
			if results_dict[counter]["logDeviceType"] == "Motion Sensor":
				results_dict[counter]["logEventType"] = "Motion detected"
		counter+=1
	return results_dict

def parse_hub_info(results_string):
	results_dict = {"gsm_simCardState" :"", "hubPowered":"","objectId":"","geo_gps_coords":"","groupsEnabled":"","gsm_activeSimNumber":"","hubName":"","timeZone":""}
	# sim status
	start = results_string.find('gsm_simCardState"=')+19 #"gsm_simCardState"= = 19 chars
	end = results_string.find(";",start)
	results_dict["gsm_simCardState"] = results_string[start:end] if start != 18 else ""
	#power status
	start = results_string.find('hubPowered=')+11 #hubPowered= = 11 chars
	end = results_string.find(";",start)
	results_dict["hubPowered"] = results_string[start:end]	if start != 10 else ""
	#hub id
	start = results_string.find('objectId=',end)+9 #objectId = 9 chars
	end = results_string.find(";",start)
	results_dict["objectId"] = results_string[start:end] if start != 8 else ""
	# geo_gps_coords  status
	start = results_string.find('geo_gps_coords',end)+16 #geo_gps_coords=" 16 chars
	end = results_string.find(";",start)
	results_dict["geo_gps_coords"] = results_string[start:end] if start != 15 else ""
	# groupsEnabled  status
	start = results_string.find('groupsEnabled',end)+14 #groupsEnabled== 18 chars
	end = results_string.find(";",start)
	results_dict["groupsEnabled"] = results_string[start:end] if start != 13 else ""
	# gsm_activeSimNumber  status
	start = results_string.find('gsm_activeSimNumber',end)+21 #gsm_activeSimNumber 21 chars
	end = results_string.find(";",start)
	results_dict["gsm_activeSimNumber"] = results_string[start:end] if start != 20 else ""
	# hubName  hubName
	start = results_string.find('hubName',end)+9 #hubName= 9 chars
	end = results_string.find(";",start)
	results_dict["hubName"] = results_string[start:end-1] if start != 8 else ""
	# timeZone
	start = results_string.find('timeZone',end)+10 #timeZone= 10 chars
	end = results_string.find(";",start)
	results_dict["timeZone"] = results_string[start:end-1] if start != 9 else ""
	return results_dict

def parse_dev_info(results_string):
	results_dict = {}
	dev_string_start = results_string.find('devices=(')
	dev_string_finish = results_string.find(");",dev_string_start)
	dev_string = results_string[dev_string_start:dev_string_finish]
	dev_list = dev_string.split(",")
	counter = 1
	for i in dev_list:	
		results_dict[counter] = {"firmWareVersion" :"", "index":"","objectId":"","objectType":"","online":""}
		# firmWareVersion status
		start = i.find('firmWareVersion=')+16 #firmWareVersion= = 16 chars
		end = i.find(";",start)
		results_dict[counter]["firmWareVersion"] = i[start:end] if start != 15 else ""
		# index id
		start = i.find('index=')+7 #index="= = 7 chars
		end = i.find(";",start)
		results_dict[counter]["index"] = i[start:end-1] if start != 6 else ""
		# objectId 
		start = i.find('objectId',end)+9 #objectId= 9 chars
		end = i.find(";",start)
		results_dict[counter]["objectId"] = i[start:end] if start != 8 else ""
		# objectType 
		start = i.find('objectType',end)+11 #objectType 11 chars
		end = i.find(";",start)
		results_dict[counter]["objectType"] = i[start:end] if start != 10 else ""
		# online  status
		start = i.find('online',end)+7 #online= 7 chars
		end = i.find(";",start)
		results_dict[counter]["online"] = i[start:end] if start != 6 else ""
		counter+=1
	return results_dict

def parse_agreementVer(results_string):
	results_dict = {}
	#user mail
	start = results_string.find("userMail")+10 #userMail=" = 10 chars
	end = results_string.find(";",start)
	results_dict["userMail"] = results_string[start:end-1] if start != 9 else ""
	#user mobile
	start = results_string.find("userMobile")+12 #userMobile=" = 12 chars
	end = results_string.find(";",start)
	results_dict["userMobile"] = results_string[start:end-1] if start != 11 else ""
	#user name		
	start = results_string.find("userName")+9 #userName= = 9 chars
	end = results_string.find(";",start)
	results_dict["userName"] = results_string[start:end] if start != 8 else ""
	return results_dict

def parse_room_info(results_string):
	results_dict = {}
	room_string_start = results_string.find('rooms=(')
	room_string_finish = results_string.find(");",room_string_start)
	room_string = results_string[room_string_start:room_string_finish]
	room_list = room_string.split(",")
	counter = 1
	for i in room_list:	
		results_dict[counter] = {"alarmDelay" :"", "armDelay":"","hub_objectId":"","index":"","objectId":"","roomName":""}
		# alarmDelay status
		start = i.find('alarmDelay=')+11 #alarmDelay= = 11 chars
		end = i.find(";",start)
		results_dict[counter]["alarmDelay"] = i[start:end] if start != 10 else ""
		# armDelay
		start = i.find('armDelay')+9 #armDelay="= = 9 chars
		end = i.find(";",start)
		results_dict[counter]["armDelay"] = i[start:end-1] if start != 8 else ""
		# hub_objectId 
		hub_start = i.find('hub={',end) #objectId= 9 chars
		start = i.find("objectId",hub_start)+9
		end = i.find(";",start)
		results_dict[counter]["hub_objectId"] = i[start:end] if start != 8 else ""
		# index 
		start = i.find('index',end)+7 #index 7 chars
		end = i.find(";",start)
		results_dict[counter]["index"] = i[start:end-1] if start != 6 else ""
		# objectId  status
		start = i.find('objectId',end)+9 #online= 9 chars
		end = i.find(";",start)
		results_dict[counter]["objectId"] = i[start:end] if start != 8 else ""
		# roomName  status
		start = i.find('roomName',end)+9 #roomName 10 chars
		end = i.find(";",start)
		results_dict[counter]["roomName"] = i[start:end] if start != 8 else ""
		counter+=1
	return results_dict

def parse_user_info(results_string):
	results_dict = {}
	user_string_start = results_string.find('users=')
	user_string_finish = results_string.find(");",user_string_start)
	user_string = results_string[user_string_start:user_string_finish]
	user_list = user_string.split("},")
	counter = 1
	for i in user_list:
		results_dict[counter] = {"alarmRules" :"", "armAccess":"","armRules":"","eventRules":"","malfRules":"","lastName":"","masterUser":"","shSMSRules":"","userIndex":"","userMail":"","userMobile":"","userName":""}
		#user alarmRules
		start = i.find("alarmRules")+11 #alarmRules= 11 chars
		end = i.find(";",start)
		results_dict[counter]["alarmRules"] = i[start:end] if start != 10 else ""
		#user armAccess
		start = i.find("armAccess")+10 #armAccess= 10 chars
		end = i.find(";",start)
		results_dict[counter]["armAccess"] = i[start:end] if start != 9 else ""
		#user armRules
		start = i.find("armRules")+9 #armRules= 9 chars
		end = i.find(";",start)
		results_dict[counter]["armRules"] = i[start:end] if start != 8 else ""
		#user eventRules
		start = i.find("eventRules")+11 #eventRules= 11 chars
		end = i.find(";",start)
		results_dict[counter]["eventRules"] = i[start:end] if start != 10 else ""
		#user malfRules
		start = i.find("malfRules")+10 #malfRules= 10 chars
		end = i.find(";",start)
		results_dict[counter]["malfRules"] = i[start:end] if start != 9 else ""
		#user lastName
		start = i.find("lastName")+9 #lastName= 9 chars
		end = i.find(";",start)
		results_dict[counter]["lastName"] = i[start:end] if start != 8 else ""
		#user masterUser
		start = i.find("masterUser")+11 #masterUser= 11 chars
		end = i.find(";",start)
		results_dict[counter]["masterUser"] = i[start:end] if start != 10 else ""
		#user shSMSRules
		start = i.find("shSMSRules")+11 #shSMSRules= 11 chars
		end = i.find(";",start)
		results_dict[counter]["shSMSRules"] = i[start:end] if start != 10 else ""
		#user userIndex
		start = i.find("userIndex")+10 #userIndex= 10 chars
		end = i.find(";",start)
		results_dict[counter]["userIndex"] = i[start:end] if start != 9 else ""
		#user userMail
		start = i.find("userMail")+10 #userMail= 10 chars
		end = i.find(";",start)
		results_dict[counter]["userMail"] = i[start:end-1] if start != 9 else ""
		#user userMobile
		start = i.find("userMobile")+12 #userMobile= 12 chars
		end = i.find(";",start)
		results_dict[counter]["userMobile"] = i[start:end-1] if start != 11 else ""
		#user userName
		start = i.find("userName")+9 #lastName= 9 chars
		end = i.find(";",start)
		results_dict[counter]["userName"] = i[start:end] if start != 8 else ""
		counter+=1
	return results_dict

def extract_intel(results_string):
	results_dict = {}
	if results_string.startswith("agreementVer"):
		results_dict = {"agreementVer" :{}, "type" : 1}
		results_dict["agreementVer"] = parse_agreementVer(results_string)
	elif results_string.startswith("hubs=("):
		results_dict = {"hub" :{}, "devices":{}, "rooms":{},"users":{}, "type" : 2}
		results_dict["hub"] = parse_hub_info(results_string)
		results_dict["devices"] = parse_dev_info(results_string)
		results_dict["rooms"] = parse_room_info(results_string)
		results_dict["users"] = parse_user_info(results_string)
	elif "logDeviceId" in results_string:
		results_dict = {"log_entry" :{}, "type" : 3}
		results_dict["log_entry"] = parse_log_info(results_string)
	return results_dict

def handle_intel(results_entry):
	report_dir = {}
	results_dict = {}
	for k,v in results_entry.items():
		results_dict[k]	= extract_intel(v)
	for k,v in results_dict.items():
		if results_dict[k]: # if dict entry not parsed skip
			report_dir[k] = v
	return report_dir

def parse_ios_logfile(logfile):
	temp_dir = {}
	report_dir = {"1":{},"2":{},"3":{}}
	with open(logfile,'r',encoding='utf-8') as log:
		counter = 0
		results = {}
		start_found = 0
		start_result = [")]... Result: {",")]... Result: ("]
		for i in log:
			if start_found == 1:
				if re.match(r"([0-9]+(:[0-9]+)+)",i):
					result_entry = log_entry.rstrip('}\n')
					result_entry = result_entry.replace(" ","")
					results[log_cur_date] = result_entry
					start_found = 0				
				log_entry+=i #adds each line to a temp string

			if start_found == 0:
				if re.match(r"([0-9]+(:[0-9]+)+)",i):
					log_cur_date = str(re.match(r"([0-9]+(:[0-9]+)+)",i).group(1)) #holds the date of the latest entry prior to find the result string
				if (start_result[0] in i) or (start_result[1] in i):
					start_found = 1
					counter+=1
					log_entry = "" #"{" #"Result: {"
		temp_dir = handle_intel(results)
		#grouping results based on their type
		for k,v in temp_dir.items():
			if temp_dir[k]["type"] == 1:
				report_dir["1"][k] = temp_dir[k]
			elif temp_dir[k]["type"] == 2:
				report_dir["2"][k] = temp_dir[k]
			elif temp_dir[k]["type"] == 3:
				report_dir["3"][k] = temp_dir[k]
	return report_dir

def parse_logfile_dir(input_file_dir): #returns dict_log
	ext = ('.log')
	fname = "systems.ajax.iosapp"
	dir_dict = {}
	dict_log ={}
	for file in os.listdir(input_file_dir):
		if file.endswith(ext) and file.startswith(fname):
			try:
				dict_log = parse_ios_logfile(input_file_dir+"\\"+file)
				dir_dict[file] = dict_log
			except Exception as e:
				print(f"Error occured while reading logfiles directory. The error message was {e}")
	return dir_dict
