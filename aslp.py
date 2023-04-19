import PySimpleGUI as sg 
import time
import os
import base64
from pathlib import Path
import scripts.html_reporting as hr
import scripts.android_parser as andpar 
import scripts.ios_parser as iospar
cur_time = time.time()
cur_time_in_ms = int(cur_time*1000)
validation_status = []
version = "1.0.0"

#######################################################################################################
#                                """atropos icon BEGIN"""
#######################################################################################################
myfavicon = hr.get_icon()
#######################################################################################################
#                                """atropos icon FINISH"""
#######################################################################################################
#######################################################################################################
#                                """USER Parsing function BEGIN"""
#######################################################################################################
#This method is the most important in this file. It takes the user GUI inputs and sends the commands to the rest of the parsers/carvers etc.
def parse_user_input(values,input_choice):
	filename = os.path.basename(values['-INPUT-F-'])
	window['-PROGRESS-BAR-'].UpdateBar(55,100)
	if input_choice == "Folder":
		dir_dicto = {}
		window['-PROGRESS-BAR-'].UpdateBar(60,100)
		hr.mylogger(f"\n{cur_time}: Begin parsing files within the input folder")
		for file in os.listdir(values['-INPUT-F-']):
			if file.endswith('.log') and file.startswith("systems.ajax.iosapp"):
				dir_ios_dicto = iospar.parse_logfile_dir(values['-INPUT-F-'])
			elif " (build #" in file and file.startswith('v '):
				dir_android_dicto = andpar.parse_logfile_dir(values['-INPUT-F-'])
		time_zone = "Mobile Device Selected Time Zone"
		dir_dicto.update(dir_ios_dicto) 
		dir_dicto.update(dir_android_dicto) 
		window['-PROGRESS-BAR-'].UpdateBar(65,100)
		hr.mylogger(f"\n{cur_time}: Begin reporting results")
		for k,v in dir_dicto.items():
			for k1,v1 in v.items():
				if k1 == "1": #iOS user info
					hr.html_report_parsed(v["1"],values['-OUTPUT-FOLDER-'],values['-INPUT-F-']+'/'+k,time_zone,"iOS","1")
				if k1 == "2": #iOS hub info
					hr.html_report_parsed(v["2"],values['-OUTPUT-FOLDER-'],values['-INPUT-F-']+'/'+k,time_zone,"iOS","2")
				if k1 == "3":#iOS log info
					hr.html_report_parsed(v["3"],values['-OUTPUT-FOLDER-'],values['-INPUT-F-']+'/'+k,time_zone,"iOS","3")
				if k1 == "4": #android log info
					hr.html_report_parsed(v["4"],values['-OUTPUT-FOLDER-'],values['-INPUT-F-']+'/'+k,time_zone,"Android","4")
				if k1 == "5": #android user info
					hr.html_report_parsed(v["5"],values['-OUTPUT-FOLDER-'],values['-INPUT-F-']+'/'+k,time_zone,"Android","5")
		hr.create_report_folder_results(values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],dir_dicto,rtype="Generic")
		hr.create_report_stand_html(values['-OUTPUT-FOLDER-'])
		hr.create_report_icons(values['-OUTPUT-FOLDER-'])
		hr.create_report_index(values['-OUTPUT-FOLDER-'],version,["folder",values['-INPUT-F-']])
		window['-PROGRESS-BAR-'].UpdateBar(75,100)
		hr.mylogger(f"\n{cur_time}: Finishing reporting results")	
	elif input_choice == "log" and "systems.ajax.iosapp" in filename:#iOS  parser
		window['-PROGRESS-BAR-'].UpdateBar(60,100)
		hr.mylogger(f"\n{cur_time}: Begin parsing iOS logfile")
		dict_log = iospar.parse_ios_logfile(values['-INPUT-F-'])
		time_zone = "Mobile Device Selected Time Zone"
		window['-PROGRESS-BAR-'].UpdateBar(65,100)
		hr.mylogger(f"\n{cur_time}: Begin reporting results")
		for k,v in dict_log.items():
			if k == "1": #user info
				hr.html_report_parsed(v,values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],time_zone,"iOS","1")
			if k == "2": #hub info
				hr.html_report_parsed(v,values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],time_zone,"iOS","2")
			if k == "3":#log info
				hr.html_report_parsed(v,values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],time_zone,"iOS","3")
		hr.create_report_stand_html(values['-OUTPUT-FOLDER-'])
		hr.create_report_icons(values['-OUTPUT-FOLDER-'])
		hr.create_report_index(values['-OUTPUT-FOLDER-'],version,["log",filename,"iOS"])
		window['-PROGRESS-BAR-'].UpdateBar(75,100)
		hr.mylogger(f"\n{cur_time}: Finishing reporting results")	
	elif " (build #" in filename and filename.startswith('v '): #Android parser
		window['-PROGRESS-BAR-'].UpdateBar(60,100)
		hr.mylogger(f"\n{cur_time}: Begin parsing Android logfile")
		dict_log = andpar.parse_android_logfile(values['-INPUT-F-'])
		time_zone = "Mobile Device Selected Time Zone"
		window['-PROGRESS-BAR-'].UpdateBar(65,100)
		hr.mylogger(f"\n{cur_time}: Begin reporting results")
		for k,v in dict_log.items():
			if k == "4": #log info
				hr.html_report_parsed(v,values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],time_zone,"Android","4")
			if k == "5": #user info
				hr.html_report_parsed(v,values['-OUTPUT-FOLDER-'],values['-INPUT-F-'],time_zone,"Android","5")
		hr.create_report_stand_html(values['-OUTPUT-FOLDER-'])
		hr.create_report_icons(values['-OUTPUT-FOLDER-'])
		hr.create_report_index(values['-OUTPUT-FOLDER-'],version,["log",filename,"Android"])
		window['-PROGRESS-BAR-'].UpdateBar(75,100)
		hr.mylogger(f"\n{cur_time}: Finishing reporting results")	
	window['-PROGRESS-BAR-'].UpdateBar(80,100)
#######################################################################################################
#									"""USER Parsing function FINISH"""
#######################################################################################################
#######################################################################################################
#									"""GUI Code section BEGIN"""
#######################################################################################################
def make_window(version):
	sg.theme('Reddit')
	logging_output= []
	right_click_menu_def = [[],['About']]


	input_files_frame = [[sg.Input(s=(40,2),key='-INPUT-F-'), sg.FileBrowse(button_text='File Browser', file_types=(("Log Files", "*.log"),)),sg.FolderBrowse(button_text='Folder Browser',target = (sg.ThisRow,-2))]]

	output_files_frame = [[sg.Input(s=(53,2),key='-OUTPUT-FOLDER-'),sg.FolderBrowse('Folder Browser')]]

	input_layout = [ 
		   [sg.Frame('Select either a logfile [.log] or a folder containing logfiles:',input_files_frame,font='Any 12')],
		   [sg.Frame("Select report's output folder:",output_files_frame,font='Any 12')],
		   [sg.ProgressBar(max_value=100, orientation='h',size=(45,15), key='-PROGRESS-BAR-',bar_color=("Green","Light Grey"))],
		   [sg.Button("Process"), sg.Button('Cancel')]]
	
	window = sg.Window('Ajax Systems Log Parser v. '+version, input_layout, icon=myfavicon, right_click_menu=right_click_menu_def, right_click_menu_tearoff=False, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True)
	return window

def validate_input(values):
	input_f = values['-INPUT-F-']
	output_f = values['-OUTPUT-FOLDER-']
	input_choice = ""
	iflag = ""
	oflag = ""
	if len(input_f) == 0:
		sg.popup_error("Neither 'INPUT FILE' nor 'INPUT FOLDER' were provided.",title="Input Error",keep_on_top = True, icon=myfavicon)
		iflag =  False
	elif not os.path.exists(input_f):
		sg.popup_error("'INPUT FILE' or 'INPUT FOLDER' does not exist.",title = "Input Error",keep_on_top = True, icon=myfavicon)
		iflag =  False
	elif os.path.isdir(input_f):
		iflag = True
		input_choice = "Folder"
	else:
		if not input_f.lower().endswith(".log") and (not input_f.lower().startswith("v ") or not input_f.lower().startswith("systems.ajax")): #test
			sg.popup_error(f"File type not supported: You provided {input_f[-3:]} whereas .log type is supported.",title = "Filetype Error",keep_on_top = True, icon='scripts/Images/myfavicon.ico')
			iflag = False
		else:
			iflag = True
			input_choice = Path(input_f).suffix[1:].lower()
	if len(output_f) == 0:
		sg.popup_error("No 'OUTPUT FOLDER' was provided.",title = "Output Error",keep_on_top = True, icon=myfavicon)
		oflag = False
	elif not os.path.exists(output_f):
		sg.popup_error("'OUTPUT FOLDER' does not exist.",title = "Output Error",keep_on_top = True, icon=myfavicon)
		oflag = False
	elif os.path.isdir(output_f):
		oflag = True
	if 	iflag == False or oflag == False:
		flag = False
	else:
		flag = True
	return [flag,input_choice]

#######################################################################################################
#									"""GUI Code section FINISH"""
#######################################################################################################
#######################################################################################################
#									"""Main Part BEGIN"""
#######################################################################################################
window = make_window(version)


while True:
	event,values = window.read()
	if event in (sg.WIN_CLOSED,'Cancel'):
		break
	elif event == 'About':
		hr.mylogger(f"\n{cur_time}: User clicked About Info")
		about_info = f"""Current Version: {version}\n\nDeveloped by Evangelos Dragonas (@theAtropos4n6)\n\nResearch by:\n-Evangelos Dragonas\n-Costas Lambrinoudakis\n\nMore information available at: https://github.com/AjaxSystemsLogParser"""
		sg.popup(about_info, title='About',button_type=0,keep_on_top=True,icon=myfavicon)
	elif event == 'Process':
		validation_results = validate_input(values)
		if validation_results[0] == True:
			window['-PROGRESS-BAR-'].UpdateBar(5,100)
			hr.mylogger(f"\n{cur_time}:Validation of user input success")
			window['-PROGRESS-BAR-'].UpdateBar(10,100)
			hr.mylogger(f"\n{cur_time}:User Input File/Folder:{values['-INPUT-F-']}")
			hr.mylogger(f"\n{cur_time}:User Output Folder:{values['-OUTPUT-FOLDER-']}")
			window['-PROGRESS-BAR-'].UpdateBar(20,100)
			hr.mylogger(f"\n{cur_time}:Process Start.")
			window['-PROGRESS-BAR-'].UpdateBar(25,100)
			hr.mylogger(f"\n{cur_time}:Parsing User Input.")
			window['-PROGRESS-BAR-'].UpdateBar(30,100)
			parse_user_input(values,validation_results[1])
			hr.mylogger(f"\n{cur_time}:Process Complete.")
			hr.log_exporter(values['-OUTPUT-FOLDER-'],hr.ajax_log)
			window['-PROGRESS-BAR-'].UpdateBar(100,100)
			prinfo = f"""Process Complete"""
			sg.popup(prinfo, title='Ajax Systems Log Analyzer',button_type=0,keep_on_top=True,icon=myfavicon)
			break
window.close()