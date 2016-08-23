import os
from os.path import basename
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import paramiko
import time
from threading import Thread
def patch_crypto_be_discovery():	#This is so I can compile!!

    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
    ]
patch_crypto_be_discovery()			#This is so I can compile!!

#NetScriptAssist v3.0
			
#Window Settings-----------------------------------------------------
window = Tk()
window.geometry("500x445")			#Default Window Geometry
window.title("NetScript Assist")	#Window Title
window.iconbitmap("NetScript.ico")	#Window Icon
#----------------------------------------------------!Window Settings

#Global Variables----------------------------------------------------
sleep_var = 2 					#Sleep variable (Def=2)
date = time.strftime("%m") + "-" + time.strftime("%d") + "-" + time.strftime("%y")
endProgram_var = 0				#Program Quit variable
scriptRunner_var = IntVar()		#Checkbox: Edit-scriptRunner -> scriptRunner (On Always) 
scriptRunner_var.set(1)
scriptRealtime_var = IntVar()	#Checkbox: Edit-scriptRealtime -> scriptRealtime (On/Off)
scriptEditor_var = IntVar()			#Checkbox: Edit-scriptEditor -> scriptEditor (On/Off)
elevate_btn_var = IntVar()			#Checkbox: scriptRunner_User_frame: elevate (On/Off)
checkAll_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: CheckAll (On/Off)
check1_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 1
check2_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 2
check3_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 3
check4_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 4
check5_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 5
check6_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 6
check7_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 7
check8_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 8
check9_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 9
check10_btn_var = IntVar()			#Checkbox: scriptRunner_Node_frame: Check 10
sleep_btn_var = IntVar()			#Checkbox: Edit-scriptRunner -> Sleep Var (On/Off)
runnerFile_get = ""				#runnerFile open 
runnerFile_name = ""			#runnerFile name
scriptFile_name = ""			#Script File name 
scriptFile_get = ""				#Script File open
scriptRun_name = "" 			#Script Run name
scriptRun_get = ""				#Script Run open 
#---------------------------------------------------!Global Variables

#Global Lists--------------------------------------------------------
sleepList=[0,1,2,3,4,5,6,7,8,9,10]
scriptList=[""]
scriptList_compareCombobox=[""]
checkBtn_List=[""]
ipAddress_List=[""]
compareCombobox_errorList=[]
checkBtn_errorList=[]
ipAddress_errorList=[]
#-------------------------------------------------------!Global Lists

#Program Functions---------------------------------------------------
def error_function(errnum):	#Run error windows
	if errnum == 0:
		messagebox.showwarning("Error: "+str(errnum), "Entry not valid:\nA node has not been selected!")
	elif errnum == 1:
		messagebox.showwarning("Error: "+str(errnum), "Entry not valid:\nAn IP Address is invalid!")
	elif errnum == 2:
		messagebox.showwarning("Error: "+str(errnum), "Entry not valid:\nA Script is invalid!")
	elif errnum == 3:
		messagebox.showwarning("Error: "+str(errnum), "Entry not valid:\n-An IP Address is invalid\n-A Script is invalid!")
	else:
		messagebox.showwarning("Error!", "Generic Error")		
def valid_ip(ip):			#Check to make sure IP Addresses are valid
	parts = ip.split('.')
	return (
		len(parts) == 4
		and all(part.isdigit() for part in parts)
		and all(0 <= int(part) <= 255 for part in parts)
		)
def populate_ScriptList():	#Populate combobox1_cbx with updated scriptList
	global scriptList
	scriptList=[]
	for file in os.listdir("Scripts"):
		if file.endswith(".netsa"):
			scriptList.append(file)
	scriptList.append("")
	combobox1_cbx.configure(values=scriptList)		#Repopulate the scripts list 
	combobox2_cbx.configure(values=scriptList)
	combobox3_cbx.configure(values=scriptList)
	combobox4_cbx.configure(values=scriptList)
	combobox5_cbx.configure(values=scriptList)
	combobox6_cbx.configure(values=scriptList)
	combobox7_cbx.configure(values=scriptList)
	combobox8_cbx.configure(values=scriptList)
	combobox9_cbx.configure(values=scriptList)
	combobox10_cbx.configure(values=scriptList)
def populate_Lists():		#Populate Lists: checkBtn_List, ipAddress_List, scriptList_compareCombobox
	
	global checkBtn_List, ipAddress_List, scriptList_compareCombobox
	
	checkBtn_List = [ #checkBtn_List 
	check1_btn_var.get(), check2_btn_var.get(), check3_btn_var.get(), check4_btn_var.get(), check5_btn_var.get(),
	check6_btn_var.get(), check7_btn_var.get(), check8_btn_var.get(), check9_btn_var.get(), check10_btn_var.get()
	]
	
	ipAddress_List = [ #ipAddress_List
	ipEntry1_ent.get(), ipEntry2_ent.get(), ipEntry3_ent.get(), ipEntry4_ent.get(), ipEntry5_ent.get(),
	ipEntry6_ent.get(), ipEntry7_ent.get(), ipEntry8_ent.get(), ipEntry9_ent.get(), ipEntry10_ent.get()
	]
	
	scriptList_compareCombobox = [
	scriptList[combobox1_cbx.current()], scriptList[combobox2_cbx.current()], scriptList[combobox3_cbx.current()], 
	scriptList[combobox4_cbx.current()], scriptList[combobox5_cbx.current()], scriptList[combobox6_cbx.current()],
	scriptList[combobox7_cbx.current()], scriptList[combobox8_cbx.current()], scriptList[combobox9_cbx.current()],
	scriptList[combobox10_cbx.current()]
	]
def createErrorLists():			#Populate Lists: compareCombobox_errorList, checkBtn_errorList, ipAddress_errorList	#Execute 1
	global compareCombobox_errorList, checkBtn_errorList, ipAddress_errorList
	
	populate_Lists()				#Grab the newest checkBtn_List, ipAddress_List, and scriptList_compareCombobox
	
	compareCombobox_errorList=[]	#Reset: compareCombobox_errorList
	checkBtn_errorList=[]			#Reset: checkBtn_errorList
	ipAddress_errorList=[]			#Reset: ipAddress_errorList
	
	#Combolist check
	counter = 0
	for i in checkBtn_List:							#Check if combobox has something put in it 
		if i == 0:										#If you are not checked, PASS
			compareCombobox_errorList.append(0)
		else:
			if scriptList_compareCombobox[counter]=="":
				compareCombobox_errorList.append(1)
			else:
				compareCombobox_errorList.append(0)
		counter = counter +1	
	
	#IP Address check 
	ipAddress_errors=[]						#Create the ipAddress_errors
	for i in iter(ipAddress_List):					#append true or false for: ipAddress_List[x] = valid ip
		ipAddress_errors.append(valid_ip(i))
	
	counter = 0
	for i in checkBtn_List:							#Check if IP Addresses are valid: LOOP
		if i == 0:										#If you are not checked, PASS
			ipAddress_errorList.append(0)
		else:
			if ipAddress_errors[counter] == True:
				ipAddress_errorList.append(0)
			else:
				ipAddress_errorList.append(1)
		counter = counter + 1
	reviewErrorLists()
def reviewErrorLists():			#Review Lists: compareCombobox_errorList, checkBtn_errorList, ipAddress_errorList	#Execute 2

	ipAddress_error = 0
	combobox_error = 0
	
	if (all(v == 0 for v in ipAddress_errorList) == 1) == False:	#If there is an error in ipAddress_errorList
		ipAddress_error = 1												#Make ipAddress_error = 1 
																		#Change the colors of the errored entries
		if ipAddress_errorList[0] == 1:						
			ipEntry1_ent.configure(bg="red")
		else:
			ipEntry1_ent.configure(bg="white")
		if ipAddress_errorList[1] == 1:
			ipEntry2_ent.configure(bg="red")
		else:
			ipEntry2_ent.configure(bg="white")
		if ipAddress_errorList[2] == 1:
			ipEntry3_ent.configure(bg="red")
		else:
			ipEntry3_ent.configure(bg="white")
		if ipAddress_errorList[3] == 1:
			ipEntry4_ent.configure(bg="red")
		else:
			ipEntry4_ent.configure(bg="white")
		if ipAddress_errorList[4] == 1:
			ipEntry5_ent.configure(bg="red")
		else:
			ipEntry5_ent.configure(bg="white")
		if ipAddress_errorList[5] == 1:
			ipEntry6_ent.configure(bg="red")
		else:
			ipEntry6_ent.configure(bg="white")
		if ipAddress_errorList[6] == 1:	
			ipEntry7_ent.configure(bg="red")
		else:
			ipEntry7_ent.configure(bg="white")
		if ipAddress_errorList[7] == 1:
			ipEntry8_ent.configure(bg="red")
		else:
			ipEntry8_ent.configure(bg="white")
		if ipAddress_errorList[8] == 1:
			ipEntry9_ent.configure(bg="red")
		else:
			ipEntry9_ent.configure(bg="white")
		if ipAddress_errorList[9] == 1:
			ipEntry10_ent.configure(bg="red")
		else:
			ipEntry10_ent.configure(bg="white")		
	else:															#If not, change the colors back to good 
		ipAddress_error = 0
		ipEntry1_ent.configure(bg="white")
		ipEntry2_ent.configure(bg="white")
		ipEntry3_ent.configure(bg="white")
		ipEntry4_ent.configure(bg="white")
		ipEntry5_ent.configure(bg="white")
		ipEntry6_ent.configure(bg="white")
		ipEntry7_ent.configure(bg="white")
		ipEntry8_ent.configure(bg="white")
		ipEntry9_ent.configure(bg="white")
		ipEntry10_ent.configure(bg="white")
	
	if (all(v == 0 for v in compareCombobox_errorList) == 1) == False:	#If there is an error in compareCombobox_errorList
		combobox_error = 1									
	else:
		combobox_error = 0
	
	#Pre Execute Errors
	if (all(v == 0 for v in checkBtn_List)) == True:
		error_function(0)
	elif ipAddress_error == 1 and combobox_error == 1:
		error_function(3)
	elif ipAddress_error == 1:
		error_function(1)
	elif combobox_error == 1:
		error_function(2)
	
	else:
		startProgram()
def startProgram():				#Start the thread definition 														#Execute 3
	execute_btn.configure(text = "Executing... Please Wait", state=DISABLED, fg = "RED")
	filemenu.entryconfigure(1, state="disabled")
	filemenu.entryconfigure(3, state="disabled")
	t1 = Thread(target = SSH)
	t1.start()	
def SSH():						#Start the SSH communication
	global sleep_var
	scriptRealtime_var.set(1)				#Set the realtime checkbox as on 
	scriptRealtime_toggle()					#Turn on the Script Realtime Window 
	
	sleep_var = int(sleep_cbx.get())
	print (sleep_var)
	
	username = username_ent.get()			#Username Variable 
	password = password_ent.get()			#Password Variable
	elevatepassword = elevateEnt_ent.get()	#elevate Password Variable

	checkBtn_counter = 0					#Counter (Which check button you are on) 
	
	realtime_editor.insert(END,"\n------------------------------------------------------------\n")
	realtime_editor.see("end")
	realtime_editor.insert(END,"Executing...")
	realtime_editor.see("end")
	realtime_editor.insert(END,"\n------------------------------------------------------------")
	
	while checkBtn_counter < (len(checkBtn_List)):	#While your counter is less than 10
		if endProgram_var == 1: #If you exited the program, stop the next script form starting
			quit()
		
		nodeip = ipAddress_List[checkBtn_counter]				#Set Node IP
		script = scriptList_compareCombobox[checkBtn_counter]	#Set Script Name
		check_var = checkBtn_List[checkBtn_counter]				#Set Checkbutton var
																#progressbar = progress[checkBtn_counter]_pgb
		if checkBtn_counter == 0:					#Set progress bar 1
			progressbar = progress1_pgb
		elif checkBtn_counter == 1:					#Set progress bar 2
			progressbar = progress2_pgb
		elif checkBtn_counter == 2:					#Set progress bar 3
			progressbar = progress3_pgb
		elif checkBtn_counter == 3:					#Set progress bar 4
			progressbar = progress4_pgb
		elif checkBtn_counter == 4:					#Set progress bar 5
			progressbar = progress5_pgb
		elif checkBtn_counter == 5:					#Set progress bar 6
			progressbar = progress6_pgb
		elif checkBtn_counter == 6:					#Set progress bar 7
			progressbar = progress7_pgb
		elif checkBtn_counter == 7:					#Set progress bar 8
			progressbar = progress8_pgb
		elif checkBtn_counter == 8:					#Set progress bar 9
			progressbar = progress9_pgb
		elif checkBtn_counter == 9:					#Set progress bar 10
			progressbar = progress10_pgb
		else:
			pass
		
		if check_var == 1: #If the checkbox is checked:
			if endProgram_var == 1: #If you exited the program, stop the next script form starting
				quit()
				
			#Set the realtime_editor
			realtime_editor.insert(END,"\n------------------------------------------------------------\n")
			realtime_editor.see("end")
			realtime_editor.insert(END,(nodeip+" - "+script+"\n"))
			realtime_editor.see("end")									
			realtime_editor.insert(END,"------------------------------------------------------------\n")			
			realtime_editor.see("end")			
		
			#SSH Connection	(Establish)
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:	#Try to establish the connection
				ssh.connect(nodeip, username=username, password=password)	#Try to connect to ssh using the username/pw 
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())	#Accept any cert
				chan = ssh.invoke_shell()									#Invoke shell on the channel 
				startSSH_var = 1
			except:	#If you cannot establish the connection
				result = messagebox.askquestion("Error!", ("Your authentication failed on node: "+ nodeip+"...\n -Would you like to continue?"))
				if result == "no":			#If no, quit()
					execute_btn.configure(text="Execute", fg="Green", state=NORMAL)
					exit()
				else:						#If yes, don't startScript_var and move on 
					startSSH_var = 0		
			
			if startSSH_var == 1:	#If you are successful on ssh: Run this 
				#Script File Information-----------------------------------------------		
				scriptFile_file = (".\\Scripts\\"+script)	#Set the script file
				scriptFile_open = open(scriptFile_file)		#Open the script file
				scriptFile_text = scriptFile_open.read()	#Set scriptFile_text as the script text
				 #scriptFile_text_send = Text with CHANGED variables 
				 #scriptFile_text_print = Text with UNCHANGED variables
				scriptFile_text_send = scriptFile_text													#Variable to be sent through chan.send
				scriptFile_text_send = scriptFile_text_send.replace('$username',username)					#Replace $username with username
				scriptFile_text_send = scriptFile_text_send.replace('$password', password)					#Replace $password with password
				scriptFile_text_send = scriptFile_text_send.replace('$elevatepassword', elevatepassword)	#Replace $elevatepassword with elevatepassword
				scriptFile_text_send = scriptFile_text_send.replace('$date', date)							#Replace $date with date 
				scriptFile_text_send = scriptFile_text_send.split('\n')										#Split the scriptFile_text on each line break
				scriptFile_text_print = scriptFile_text													#Variable to be sent through realtime_editor
				scriptFile_text_print = scriptFile_text.split('\n')											#Split the scriptFile_text on each line break
				#Send the script line by line----------------------------------------------
				lineCounter = 0										#Loop Counter
				lineCounter_max = len(scriptFile_text_send)-1		#Max times to loop 
				progressbar["value"] = 0							#Progress Bar start value
				progressbar["maximum"] = lineCounter_max-1			#Progress Bar Static Max
				while lineCounter < lineCounter_max:	#While you are not at the last line of scriptFile
					if "#" in scriptFile_text_print[lineCounter]:	#Skip the comments
						progressbar["value"] = lineCounter				#Set Progress Bar
						realtime_editor.insert(END, ("Skipping Comment: "+scriptFile_text_print[lineCounter]+"\n"))
						realtime_editor.see("end")
						lineCounter = lineCounter + 1					#Continue Loop 
					else:											#Send the command
						progressbar["value"] = lineCounter				#Set Progress Bar
						realtime_editor.insert(END, ("Sending: "+scriptFile_text_print[lineCounter]+"\n"))	#Print scriptFile_text_print
						realtime_editor.see("end")
						chan.send(scriptFile_text_send[lineCounter]+"\n")									#Send scriptFile_text_send
						time.sleep(sleep_var)																		#Sleep after send
						lineCounter = lineCounter + 1														#Continue Loop 
				
				realtime_editor.insert(END,"         -----Output of the script -----\n")
				realtime_editor.see("end")
				output = (chan.recv(9999).decode("utf-8"))		#Change the output to ascii from utf-8
				outputList = output.split("\r")					#Split the string by carage return
				output = " ".join(outputList)					#Return the string back to a string
				realtime_editor.insert(END,output)				#Display the output at the end of realtime_editor	
				realtime_editor.see("end")						#Show the end of realtime_editor	
				realtime_editor.insert(END,"\n------------------------------------------------------------\n")
				realtime_editor.see("end")
		
		else:
			pass
		
		
		
		checkBtn_counter += 1
	
	
	messagebox.showinfo("Success!","Your scripts have completely executed!")		
	SSH_cleanup()						
def SSH_cleanup():
	progress1_pgb["value"]=0	#Reset Progress Bar 1
	progress2_pgb["value"]=0	#Reset Progress Bar 2
	progress3_pgb["value"]=0	#Reset Progress Bar 3
	progress4_pgb["value"]=0	#Reset Progress Bar 4
	progress5_pgb["value"]=0	#Reset Progress Bar 5
	progress6_pgb["value"]=0	#Reset Progress Bar 6
	progress7_pgb["value"]=0	#Reset Progress Bar 7
	progress8_pgb["value"]=0	#Reset Progress Bar 8
	progress9_pgb["value"]=0	#Reset Progress Bar 9
	progress10_pgb["value"]=0	#Reset Progress Bar 10
	
	execute_btn.configure(text="Execute", fg="Green", state=NORMAL)	#Reset execute button
	filemenu.entryconfigure(1, state=NORMAL)
	filemenu.entryconfigure(3, state=NORMAL)
#--------------------------------------------------!Program Functions

#Menu----------------------------------------------------------------
#Define Menus
menubar = Menu(window)							#Menubar
filemenu = Menu(menubar, tearoff=0)				#File Menu 

editmenu = Menu(menubar, tearoff=0)				#Edit Menu 
scriptRunner_Menu = Menu(editmenu, tearoff=0)		#Edit -> Script Runner Menu
scriptEditor_Menu = Menu(editmenu, tearoff=0)		#Edit -> Script Editor Menu
scriptRealtime_Menu = Menu(editmenu, tearoff=0)		#Edit -> Script realtime Menu

helpmenu = Menu(menubar, tearoff=0)				#Help Menu 

#Menu Functions
#File Functions
def fileMenu_clearAll():
	scriptRunner_newFile()
	scriptRealtime_newFile()
	scriptEditor_newFile()
	scriptRealtime_var.set(0)
	scriptRealtime_toggle()
def fileMenu_testConnections_start():
	testConnections_thread = Thread(target = fileMenu_testConnections_execute)
	filemenu.entryconfigure(3, state="disabled", label="Testing In Progress...")
	filemenu.entryconfigure(1, state="disabled")
	execute_btn.configure(text = "Testing... Please Wait", state=DISABLED, fg = "RED")
	testConnections_thread.start()
	
	
def fileMenu_testConnections_execute():
		#Set the menu item disabled
	scriptRealtime_on()						#Pop open the Script Realtime
	username = username_ent.get()			#Username Variable 
	password = password_ent.get()			#Password Variable
	
	realtime_editor.insert(END,"\n------------------------------------------------------------\n")	#Realtime Editor Insert
	realtime_editor.see("end")																		#Realtime Editor Insert
	realtime_editor.insert(END,"Testing Connections\n")												#Realtime Editor Insert
	realtime_editor.insert(END,"------------------------------------------------------------\n")	#Realtime Editor Insert
	realtime_editor.see("end")																		#Realtime Editor Insert
	
	populate_Lists()
	if 1 not in checkBtn_List:
		realtime_editor.insert(END,"Test failed: There are no devices checked")
		realtime_editor.see("end")
	else:
		checkBtn_List_counter = 0
		checkBtn_List_max = len(checkBtn_List)
		
		while checkBtn_List_counter < checkBtn_List_max:
			if checkBtn_List[checkBtn_List_counter] == 0:
				pass
			else:
				nodeip = ipAddress_List[checkBtn_List_counter]
				if nodeip == '':
					realtime_editor.insert(END,"Connection failed: Checkbox "+str(checkBtn_List_counter+1)+" has no IP Address\n")	
					realtime_editor.see("end")
				elif (valid_ip(nodeip)) == False:
					realtime_editor.insert(END,"Connection failed: \'"+nodeip+"\' - is not a valid IP Address\n")
					realtime_editor.see("end")					
				else:	#Try to ssh into the machine
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					try: 	
						ssh.connect(nodeip, username=username, password=password)	#Try to connect to ssh using the username/pw 
						ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())	#Accept any cert
						chan = ssh.invoke_shell()									#Invoke shell on the channel 
						realtime_editor.insert(END,"Connection succeeded: \'"+nodeip+"'\n")
						realtime_editor.see("end")
					except:
						realtime_editor.insert(END,"Connection failed: \'"+nodeip+"' - Authentication Failed\n")
						realtime_editor.see("end")
			checkBtn_List_counter += 1
	
	
	filemenu.entryconfigure(3, state="normal", label="Test Connections")#Set the menu item enabled
	execute_btn.configure(text="Execute", fg="Green", state=NORMAL)
	filemenu.entryconfigure(1, state="normal")
	messagebox.showinfo("Testing Complete","Your test connections have completed.\nSee Script Realtime for more information.")
	
#Edit Functions	
def scriptRunner_newFile():				#Edit -> Script Runner: New File
	scriptRunner_frame.config(text="NetScript Assist: Script Runner")
	global runnerFile_get, scriptList_compareCombobox, checkBtn_List, ipAddress_List
	window.title("NetScript Assist")
	runnerFile_get = ""
	scriptList_compareCombobox=[""]
	checkBtn_List=[""]
	ipAddress_List=[""]
	
	username_ent.delete(0,END)
	password_ent.delete(0,END)
	elevate_btn_var.set(0)
	elevate()
	
	checkAll_btn.deselect()																									#Uncheck CheckAll btn
	check1_btn.deselect(), check2_btn.deselect(), check3_btn.deselect(), check4_btn.deselect(), check5_btn.deselect()		#Uncheck nodes 1-5
	check6_btn.deselect(), check7_btn.deselect(), check8_btn.deselect(), check9_btn.deselect(), check10_btn.deselect()		#Uncheck nodes 6-10

	ipEntry1_ent.delete(0, END), ipEntry2_ent.delete(0, END), ipEntry3_ent.delete(0, END), ipEntry4_ent.delete(0, END), ipEntry5_ent.delete(0, END)		#Delete entries ipEntry 1-5
	ipEntry6_ent.delete(0, END), ipEntry7_ent.delete(0, END), ipEntry8_ent.delete(0, END), ipEntry9_ent.delete(0, END), ipEntry10_ent.delete(0, END)	#Delete entries ipEntry 6-10
	
	combobox1_cbx.delete(0, END), combobox2_cbx.delete(0, END), combobox3_cbx.delete(0, END), combobox4_cbx.delete(0, END), combobox5_cbx.delete(0, END) 
	combobox6_cbx.delete(0, END), combobox7_cbx.delete(0, END), combobox8_cbx.delete(0, END), combobox9_cbx.delete(0, END), combobox10_cbx.delete(0, END)
	
	sleep_cbx.set(2)
	sleep_lbl.grid_forget()
	sleep_cbx.grid_forget()
def scriptRunner_openFile():			#Edit -> Script Runner: Open File
	global runnerFile_get, runnerFile_name
	
	runnerFile_get = filedialog.askopenfile(initialdir=".\\Runner\\")		#Ask user what file to open
	populate_ScriptList()													#In case a user deletes from here
	runnerFile_open = open(runnerFile_get.name, "r")						#Save that file as 'runnerFile_open'
	runnerFile_name = (basename(runnerFile_open.name))
	
	scriptRunner_frame.config(text="NetScript Assist: Script Runner - "+runnerFile_name)
	
	nodeList = []															#Start a new nodeList
	
	for line in iter(runnerFile_open):										#For # of lines (3) run the loop to create nodeList
		nodeList.append(line)													#append each \n as a new item in nodeList
		
	checkBtn_List_Str = nodeList[0]											#nodeList[0] = checkBtn_List_Str
	ipAddress_List_Str = nodeList[1]										#nodeList[1] = ipAddress_List_Str
	scriptList_compareCombobox_Str = nodeList[2]							#nodeList[2] = scriptList_compareCombobox_Str
	sleep_cbx.set(nodeList[3])												#nodeList[3] = sleep_timer
	
	checkBtn_List_Open = checkBtn_List_Str.split()								#Split checkBtn_List_Str spaces into a new list: checkBtn_List_Open
	ipAddress_List_Open = ipAddress_List_Str.split()							#Split ipAddress_List_Str spaces into a new list: ipAddress_List_Open
	scriptList_compareCombobox_Open = scriptList_compareCombobox_Str.split()	#Split scriptList_compareCombobox_Str spaces into a new list: scriptList_compareCombobox_Open
	
	if any("1" in s for s in checkBtn_List_Open):	#If a checkbox is checked run this 
		if checkBtn_List_Open[0] == "1":	#If checkbox 1 = checked
			check1_btn.select()
		else:
			check1_btn.deselect()
		
		if checkBtn_List_Open[1] == "1":	#If checkbox 2 = checked
			check2_btn.select()
		else:
			check2_btn.deselect()
		
		if checkBtn_List_Open[2] == "1":	#If checkbox 3 = checked
			check3_btn.select()
		else:
			check3_btn.deselect()
		
		if checkBtn_List_Open[3] == "1":	#If checkbox 4 = checked
			check4_btn.select()
		else:
			check4_btn.deselect()
		
		if checkBtn_List_Open[4] == "1":	#If checkbox 5 = checked
			check5_btn.select()
		else:
			check5_btn.deselect()
		
		if checkBtn_List_Open[5] == "1":	#If checkbox 6 = checked
			check6_btn.select()
		else:
			check6_btn.deselect()
		
		if checkBtn_List_Open[6] == "1":	#If checkbox 7 = checked
			check7_btn.select()
		else:
			check7_btn.deselect()
		
		if checkBtn_List_Open[7] == "1":	#If checkbox 8 = checked
			check8_btn.select()
		else:
			check8_btn.deselect()		
			
		if checkBtn_List_Open[8] == "1":	#If checkbox 9 = checked
			check9_btn.select()
		else:
			check9_btn.deselect()
			
		if checkBtn_List_Open[9] == "1":	#If checkbox 10 = checked
			check10_btn.select()
		else:
			check10_btn.deselect()
	else:											#If not, move on 
		print ("")

	if all ("null" in s for s in ipAddress_List_Open):	#If there are no IP Addresses
		print ("")
	else:												#If there are IP Addresses 
		if ipAddress_List_Open[0] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry1_ent.delete(0, END)						#Start fresh 
			ipEntry1_ent.insert(0, ipAddress_List_Open[0])	#change the IP address
		else:
			ipEntry1_ent.delete(0, END)	
				
		if ipAddress_List_Open[1] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry2_ent.delete(0, END)						#Start fresh 
			ipEntry2_ent.insert(0, ipAddress_List_Open[1])	#change the IP address
		else:
			ipEntry2_ent.delete(0, END)						#Start fresh
		
		if ipAddress_List_Open[2] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry3_ent.delete(0, END)						#Start fresh 
			ipEntry3_ent.insert(0, ipAddress_List_Open[2])	#change the IP address
		else:
			ipEntry3_ent.delete(0, END)						#Start fresh 
		
		if ipAddress_List_Open[3] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry4_ent.delete(0, END)						#Start fresh 
			ipEntry4_ent.insert(0, ipAddress_List_Open[3])	#change the IP address
		else:
			ipEntry4_ent.delete(0, END)						#Start fresh 
		
		if ipAddress_List_Open[4] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry5_ent.delete(0, END)						#Start fresh 
			ipEntry5_ent.insert(0, ipAddress_List_Open[4])	#change the IP address
		else:
			ipEntry5_ent.delete(0, END)						#Start fresh 

		if ipAddress_List_Open[5] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry6_ent.delete(0, END)						#Start fresh 
			ipEntry6_ent.insert(0, ipAddress_List_Open[5])	#change the IP address
		else:
			ipEntry6_ent.delete(0, END)						#Start fresh 
		
		if ipAddress_List_Open[6] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry7_ent.delete(0, END)						#Start fresh 
			ipEntry7_ent.insert(0, ipAddress_List_Open[6])	#change the IP address
		else:
			ipEntry7_ent.delete(0, END)						#Start fresh 
		
		if ipAddress_List_Open[7] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry8_ent.delete(0, END)						#Start fresh 
			ipEntry8_ent.insert(0, ipAddress_List_Open[7])	#change the IP address
		else:
			ipEntry8_ent.delete(0, END)						#Start fresh 
		
		if ipAddress_List_Open[8] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry9_ent.delete(0, END)						#Start fresh 
			ipEntry9_ent.insert(0, ipAddress_List_Open[8])	#change the IP address
		else:
			ipEntry9_ent.delete(0, END)						#Start fresh 		
		
		if ipAddress_List_Open[9] != "null":	#If ipAddress_List_Open[0] does not = null: enter the IP
			ipEntry10_ent.delete(0, END)						#Start fresh 
			ipEntry10_ent.insert(0, ipAddress_List_Open[9])	#change the IP address
		else:
			ipEntry10_ent.delete(0, END)						#Start fresh 	

	if all ("null" in s for s in scriptList_compareCombobox_Open):	#If there are no Scripts
		print ("No Scripts selected")
	else:
		if scriptList_compareCombobox_Open[0] != "null":
			combobox1_cbx.delete(0, END)
			combobox1_cbx.insert(0, scriptList_compareCombobox_Open[0])
		else:
			combobox1_cbx.delete(0, END)

		if scriptList_compareCombobox_Open[1] != "null":
			combobox2_cbx.delete(0, END)
			combobox2_cbx.insert(0, scriptList_compareCombobox_Open[1])
		else:
			combobox2_cbx.delete(0, END)
	
		if scriptList_compareCombobox_Open[2] != "null":
			combobox3_cbx.delete(0, END)
			combobox3_cbx.insert(0, scriptList_compareCombobox_Open[2])
		else:
			combobox3_cbx.delete(0, END)
	
		if scriptList_compareCombobox_Open[3] != "null":
			combobox4_cbx.delete(0, END)
			combobox4_cbx.insert(0, scriptList_compareCombobox_Open[3])
		else:
			combobox4_cbx.delete(0, END)
	
		if scriptList_compareCombobox_Open[4] != "null":
			combobox5_cbx.delete(0, END)
			combobox5_cbx.insert(0, scriptList_compareCombobox_Open[4])
		else:
			combobox5_cbx.delete(0, END)
	
		if scriptList_compareCombobox_Open[5] != "null":
			combobox6_cbx.delete(0, END)
			combobox6_cbx.insert(0, scriptList_compareCombobox_Open[5])
		else:
			combobox6_cbx.delete(0, END)
	
		if scriptList_compareCombobox_Open[6] != "null":
			combobox7_cbx.delete(0, END)
			combobox7_cbx.insert(0, scriptList_compareCombobox_Open[6])
		else:
			combobox7_cbx.delete(0, END)
	
		if scriptList_compareCombobox_Open[7] != "null":
			combobox8_cbx.delete(0, END)
			combobox8_cbx.insert(0, scriptList_compareCombobox_Open[7])
		else:
			combobox8_cbx.delete(0, END)
	
		if scriptList_compareCombobox_Open[8] != "null":
			combobox9_cbx.delete(0, END)
			combobox9_cbx.insert(0, scriptList_compareCombobox_Open[8])
		else:
			combobox9_cbx.delete(0, END)
	
		if scriptList_compareCombobox_Open[9] != "null":
			combobox10_cbx.delete(0, END)
			combobox10_cbx.insert(0, scriptList_compareCombobox_Open[9])
		else:
			combobox10_cbx.delete(0, END)

	if sleep_cbx.get() != "2":										#If sleep variable is not default, show them. 
		sleep_btn_var.set(1)
		sleep_toggle()		
def scriptRunner_saveFile():			#Edit -> Script Runner: Save File
	global runnerFile_get, checkBtn_List, ipAddress_List, scriptList_compareCombobox

	if runnerFile_get == "":
		scriptRunner_saveAsFile()
	else:
		populate_Lists()
				
		runnerFile_open = open(runnerFile_get.name, "w")
		
		counter = 0
		for i in checkBtn_List:
			runnerFile_open.write(str(checkBtn_List[counter])+" ")
			counter = counter +1
		runnerFile_open.write('\n')	
			
		counter = 0
		for i in ipAddress_List:
			if ipAddress_List[counter]=="":
				ipAddress_List[counter]= "null"
			else:
				print ("")
			runnerFile_open.write(str(ipAddress_List[counter])+" ")	
			counter = counter+1
		runnerFile_open.write('\n')
		
		counter = 0
		for i in scriptList_compareCombobox:
			if scriptList_compareCombobox[counter]=="":
				scriptList_compareCombobox[counter]="null"
			else:
				print ("")
			runnerFile_open.write(str(scriptList_compareCombobox[counter])+" ")	
			counter = counter+1
			
		runnerFile_open.write('\n')	
		runnerFile_open.write(sleep_cbx.get())	#Write the sleep number 
def scriptRunner_saveAsFile():			#Edit -> Script Runner: Save As File
	
	global runnerFile_get, checkBtn_List, ipAddress_List, scriptList_compareCombobox, runnerFile_name
	
	
	runnerFile_get = filedialog.asksaveasfile(initialdir=".\\Runner\\", defaultextension=".netsr")	
	populate_Lists()
	runnerFile_open = open(runnerFile_get.name, "w")
	
	runnerFile_name = (basename(runnerFile_open.name))
	scriptRunner_frame.config(text="NetScript Assist: Script Runner - "+runnerFile_name)
	
	print (runnerFile_open)
	
	counter = 0
	for i in checkBtn_List:
		runnerFile_open.write(str(checkBtn_List[counter])+" ")
		counter = counter +1
	runnerFile_open.write('\n')	
		
	counter = 0
	for i in ipAddress_List:
		if ipAddress_List[counter]=="":
			ipAddress_List[counter]= "null"
		else:
			print ("")
		runnerFile_open.write(str(ipAddress_List[counter])+" ")	
		counter = counter+1
	runnerFile_open.write('\n')
	
	counter = 0
	for i in scriptList_compareCombobox:
		if scriptList_compareCombobox[counter]=="":
			scriptList_compareCombobox[counter]="null"
		else:
			pass
		runnerFile_open.write(str(scriptList_compareCombobox[counter])+" ")	
		counter = counter+1
	runnerFile_open.write('\n')	
	
	runnerFile_open.write(sleep_cbx.get())	#Write the sleep number 
def sleep_toggle():						#Sleep Toggle (On/Off)

	if sleep_btn_var.get() == 1:
		sleep_lbl.grid(row=0, column=4, columnspan=2, sticky="E")
		sleep_cbx.grid(row=0, column=6, sticky="W")		
	else:
		sleep_lbl.grid_forget()
		sleep_cbx.grid_forget()	
def scriptEditor_on():					#Turn Script Editor ON
	scriptEditor_var.set(1)
	scriptEditor_toggle()
def scriptEditor_toggle(): 				#Edit -> Script Editor: Turn Script Editor On/Off
	forget_additional_frame()			
	if scriptRealtime_var.get() == 1:	#If realtime is on, shut it off 
		scriptRealtime_var.set(0)
	else:
		pass
		
	if scriptEditor_var.get() == 1:	#If checked:
		window.geometry("1003x425")											#Make screen larger
		additional_frame.configure(text="NetScript Assist: Script Editor")	#Make additional_frame text = NetScript Assist: Script Editor
		additional_frame.pack(side=TOP, anchor=E)							#Pack additional_frame
		editor_scrollbar.pack(side=RIGHT, fill=Y)									#Pack editor_scrollbar to additional_frame
		editor.pack(side=TOP)												#Pack the editor in additional_frame
		editor_statusbar.pack(side=BOTTOM, anchor=W)
		
	else:							#If unchecked:
		window.geometry("500x425")		#Make screen smaller
		editor_scrollbar.pack_forget()
		editor.pack_forget()
		additional_frame.pack_forget()	
def scriptEditor_toggle_Hotkey(hotkey):	#Edit -> Script Editor: Check hotkey to turn Script Editor On/Off
	
	if scriptEditor_var.get() == 0:	#If Script Editor box:Unchecked
		scriptEditor_var.set(1)			#Check Checkbox	
	else:							#If Script Editor box:Checked
		scriptEditor_var.set(0)			#Uncheck Checkbox
		
	scriptEditor_toggle()				#Call the scriptEditor_toggle Function	
def scriptEditor_newFile():				#Edit -> Script Editor: New File
	
	global scriptFile_name
	scriptFile_name = ""													#Clear the scriptFile_name 
	editor_statusbar.configure(text="Currently Editing: "+scriptFile_name)	#Clear the editor_statusbar "Currently Editing: "
	editor.delete(1.0, END)													#Clear the previous editor text 

	scriptEditor_on()	
def scriptEditor_openFile():			#Edit -> Script Editor: Open File
			
	global scriptFile_name, scriptFile_get				
	scriptFile_get = filedialog.askopenfile(initialdir=".\\Scripts\\")		#Ask user to open a file in .\Scripts\
	populate_ScriptList()													#Populate the list in case people delete from here
	scriptFile_open = open(scriptFile_get.name, "r") 						#Open the file with read access
	scriptFile_name = (basename(scriptFile_open.name))						#Save the file name (file.nssa) as scriptFile_name
	scriptFile_text = scriptFile_open.read()
	
	editor_statusbar.configure(text="Currently Editing: "+scriptFile_name)	#editor_statusbar display "Currently Editing: scriptFile_name"
	editor.delete(1.0, END)													#Clear the previous editor text
	editor.insert(END,scriptFile_text[:-1])							#Display the scriptFile_text in the editor (:1 = everything but the last enter)
	print (scriptFile_text[:-1])
	
	populate_ScriptList()
	
	scriptEditor_on()
def scriptEditor_saveAsFile():			#Edit -> Script Editor: Save As File 
		
	global scriptFile_name, scriptFile_get
	scriptFile_get = filedialog.asksaveasfile(initialdir=".\\Scripts\\", defaultextension=".netsa")	#Ask user to save a file in .\Scripts\(.netsa)
	populate_ScriptList()																			#Populate the list in case people delete from here
	scriptFile_openNew = open(scriptFile_get.name, "w")												#Open the file with write access
	scriptFile_name = (basename(scriptFile_openNew.name))												#Save the file name (file.nssa) as scriptFile_name
	scriptFile_openNew.write(editor.get(1.0, END))														#Write the contents of editor to scriptFile_openNew
	editor_statusbar.configure(text="Currently Editing: "+scriptFile_name)								#editor_statusbar display "Currently Editing: scriptFile_name"

	populate_ScriptList()	
	
	scriptEditor_on()
def scriptEditor_saveFile():			#Edit -> Script Editor: Save File 
		
	global scriptFile_name, scriptFile_get
		
	if scriptFile_name == "": 	#If file does not already exist:
		scriptEditor_saveAsFile()				#Run SaveAs Function
	else:						#If file does already exist:
		scriptEntry_List = editor.get(1.0, END).split("\n")
		print (len(scriptEntry_List), scriptEntry_List)
		scriptFile_open = open(scriptFile_get.name, "w")	#Open the file (scriptFile_open) with write access
	
		scriptFile_open.write(editor.get(1.0, END))			#Write the contents of editor to scriptFile_open
		print ("saving:", scriptFile_open)
		populate_ScriptList()
	#Might need to update scriptList 	
	
	
	scriptEditor_on()
def scriptEditor_scriptVariables():		#Edit -> Script Editor: Show Script Variables
	messagebox.showinfo("NetScript Assist: Script Editor - Variables!","""You can use the following variables:
---------------------------------------------------------------------------
$username             [The Username entered in Script Runner]
$password              [The Password entered in Script Runner]
$elevatepassword  [The Elevate Password entered in Script Runner]
$date                       [The Current Date: MM-DD-YY]
---------------------------------------------------------------------------
#text                   [This represents a comment. The line will NOT be sent]
""")	
def scriptRealtime_on():
	scriptRealtime_var.set(1)
	scriptRealtime_toggle()
def scriptRealtime_toggle():				#Edit -> Script Realtime: Turn Script Editor On/Off
	forget_additional_frame()
	if scriptEditor_var.get() == 1:
		scriptEditor_var.set(0)
	else:
		pass 
	if scriptRealtime_var.get() == 1: #If checked:
		window.geometry("1003x425")
		additional_frame.configure(text="NetScript Assist: Script Realtime")
		additional_frame.pack(side=TOP, anchor=E)
		realtime_editor_scrollbar.pack(side=RIGHT, fill=Y)
		realtime_editor.pack(side=TOP)
	else:
		window.geometry("500x425")	
def scriptRealtime_toggle_Hotkey(hotkey):	#Edit -> Script Realtime: Check hotkey to turn Script Editor On/Off
	
	if scriptRealtime_var.get() == 0:
		scriptRealtime_var.set(1)
	else:
		scriptRealtime_var.set(0)
	
	scriptRealtime_toggle()
def scriptRealtime_newFile():				#Edit -> Script Realtime: New File
	global scriptRun_name
	scriptRun_name = ""
	realtime_editor.delete(1.0, END)
	scriptRealtime_on()
def scriptRealtime_openFile():				#Edit -> Script Realtime: Open File
	global scriptRun_name, scriptRun_get
	scriptRun_get = filedialog.askopenfile(initialdir=".\\Realtime Logs\\")		#Ask user to open a file in .\Scripts\
	scriptRun_open = open(scriptRun_get.name, "r") 						#Open the file with read access
	scriptRun_name = (basename(scriptRun_open.name))						#Save the file name (file.nssa) as scriptRun_name
	realtime_editor.delete(1.0, END)													#Clear the previous realtime_editor text
	realtime_editor.insert(END,scriptRun_open.read())							#Display the scriptRun_text in the realtime_editor
	scriptRealtime_on()
def scriptRealtime_saveAsFile():			#Edit -> Script Realtime: Save As File
	global scriptRun_name, scriptRun_get
	scriptRun_get = filedialog.asksaveasfile(initialdir=".\\Realtime Logs\\", defaultextension=".netrt")	#Ask user to save a file in .\Scripts\(.netsa)
	scriptRun_openNew = open(scriptRun_get.name, "w")												#Open the file with write access
	scriptRun_name = (basename(scriptRun_openNew.name))												#Save the file name (file.nssa) as scriptRun_name
	scriptRun_openNew.write(realtime_editor.get(1.0, END))														#Write the contents of editor to scriptRun_openNew	
	scriptRealtime_on()
def scriptRealtime_saveFile():				#Edit -> Script Realtime: Save File
	global scriptRun_name, scriptRun_get
		
	if scriptRun_name == "": 	#If file does not already exist:
		scriptRealtime_saveAsFile()				#Run SaveAs Function
	else:						#If file does already exist:
		scriptRun_open = open(scriptRun_get.name, "w")	#Open the file (scriptRun_open) with write access
		scriptRun_open.write(realtime_editor.get(1.0, END))			#Write the contents of editor_realtime to scriptRun_open
		print ("saving:", scriptRun_open)
	scriptRealtime_on()

#Help Functions
def helpmenu_about():
	messagebox.showinfo("NetScript Assist: v1.0","""About NetScript Assist
--------------------------------------------------
Author:           NetScriptAssist (Script Ruler) 
Home Page:   http://www.netscriptassist.com
--------------------------------------------------

I have a Networking background and wanted to kindle my love for programming. I put my heart into this program and I think the end result will show. If you have any comments/questions/concerns, please let me know. 

Email: NetScriptAssist@gmail.com

I found my program helpful and I hope you do too! Please tell a friend. :)
""")	

def helpmenu_help():		#Help: Help
	os.system(".\\Files\\help.txt")	

#Menu Items
#File Menu----------------------------------------------------------------------------
filemenu.add_cascade(label="Execute", command=createErrorLists)
filemenu.add_command(label="Clear All", command=fileMenu_clearAll)	#File -> Clear All
filemenu.add_separator()
filemenu.add_command(label="Test Connections", command=fileMenu_testConnections_start)

#Edit Menu----------------------------------------------------------------------------
#Script Runner
scriptRunner_Menu.config(activeborderwidth="3")
scriptRunner_Menu.add_checkbutton(label="Script Runner", state="disabled", variable=scriptRunner_var)
scriptRunner_Menu.add_separator()
scriptRunner_Menu.add_cascade(label="New", command=scriptRunner_newFile)
scriptRunner_Menu.add_cascade(label="Open", command=scriptRunner_openFile)
scriptRunner_Menu.add_cascade(label="Save", command=scriptRunner_saveFile)
scriptRunner_Menu.add_cascade(label="Save As", command=scriptRunner_saveAsFile)
scriptRunner_Menu.add_separator()
scriptRunner_Menu.add_checkbutton(label="Edit Sleep Variable", variable=sleep_btn_var, command=sleep_toggle)
#Script Editor 
scriptEditor_Menu.config(activeborderwidth="3")																						#Script Editor: Make border larger
scriptEditor_Menu.add_checkbutton(label="Script Editor", command=scriptEditor_toggle, variable=scriptEditor_var, accelerator="<Ctrl+E>")#Script Editor: Checkbox
scriptEditor_Menu.add_separator()																									#Script Editor: ------------------------
scriptEditor_Menu.add_cascade(label="New", command=scriptEditor_newFile)															#Script Editor: -> New
scriptEditor_Menu.add_cascade(label="Open", command=scriptEditor_openFile)															#Script Editor: -> Open
scriptEditor_Menu.add_cascade(label="Save", command=scriptEditor_saveFile)															#Script Editor: -> Save
scriptEditor_Menu.add_cascade(label="Save As", command=scriptEditor_saveAsFile)														#Script Editor: -> Save As
scriptEditor_Menu.add_separator()
scriptEditor_Menu.add_cascade(label="Show Script Variables", command=scriptEditor_scriptVariables)		
#Script realtime 
scriptRealtime_Menu.config(activeborderwidth="3")	
scriptRealtime_Menu.add_checkbutton(label="Script Realtime", command=scriptRealtime_toggle, variable=scriptRealtime_var, accelerator="<Ctrl+R>")
scriptRealtime_Menu.add_separator()		
scriptRealtime_Menu.add_cascade(label="New", command=scriptRealtime_newFile)
scriptRealtime_Menu.add_cascade(label="Open", command=scriptRealtime_openFile)
scriptRealtime_Menu.add_cascade(label="Save", command=scriptRealtime_saveFile)
scriptRealtime_Menu.add_cascade(label="Save As", command=scriptRealtime_saveAsFile)


#Help Menu----------------------------------------------------------------------------
helpmenu.add_cascade(label="Help", command=helpmenu_help)	
helpmenu.add_cascade(label="About NetScript Assist", command=helpmenu_about)
								
#Apply Menus
menubar.add_cascade(label="File", menu=filemenu) 						#Apply File Menu 
menubar.add_cascade(label="Edit", menu=editmenu)						#Apply Edit Menu 
editmenu.add_cascade(label="Script Runner", menu=scriptRunner_Menu)		#Apply Edit -> Script Realtime Menu
editmenu.add_separator()
editmenu.add_cascade(label="Script Editor", menu=scriptEditor_Menu)		#Apply Edit -> Script Editor Menu
editmenu.add_separator()
editmenu.add_cascade(label="Script Realtime", menu=scriptRealtime_Menu)	#Apply Edit -> Script Realtime Menu

menubar.add_cascade(label="Help", menu=helpmenu)

#---------------------------------------------------------------!Menu

#Frames--------------------------------------------------------------
#Frame Buffers
Buffer_Left_frame = Frame(window)
Buffer_Left_lbl = Label(Buffer_Left_frame, text=" ")
Buffer_Left_frame.pack(side=LEFT)
Buffer_Left_lbl.pack(side=LEFT)
Buffer_Right_frame = Frame(window)
Buffer_Right_lbl = Label(Buffer_Right_frame, text=" ")
Buffer_Right_frame.pack(side=RIGHT)
Buffer_Right_lbl.pack(side=RIGHT)
Buffer_Bot_frame = Frame(window)
Buffer_Bot_lbl = Label(Buffer_Bot_frame, text=" ")
Buffer_Bot_frame.pack(side=BOTTOM)

#Main Frames 
scriptRunner_frame = LabelFrame(window, text="NetScript Assist: Script Runner", fg="blue")	#Script Runner Frame 
scriptRunner_User_frame = Frame(scriptRunner_frame)											#Script Runner Frame -> User Frame
scriptRunner_Node_frame = Frame(scriptRunner_frame)											#Script Runner Frame -> Node Frame
execute_frame = LabelFrame(window)															#Execute Frame
additional_frame = LabelFrame(window, fg="blue")											#Additional Frame

execute_frame.pack(side=BOTTOM, anchor=W)			#PACK Execute Frame:
scriptRunner_frame.pack(side=LEFT, anchor=N)		#PACK Script Runner Frame: TOP,W
scriptRunner_User_frame.pack(side=TOP, anchor=W)	#PACK Script Runner Frame -> User Frame: TOP, W
scriptRunner_Node_frame.pack(side=TOP, anchor=W)	#PACK Script Runner Frame -> Node Frame: TOP, W
				#PACK Execute Frame: TOP, W 
#-------------------------------------------------------------!Frames

#Widgets-------------------------------------------------------------
#Widget Functions
def elevate():		#scriptRunner_User_frame: Elevate Checkbox (On/Off)
	
	if elevate_btn_var.get() == 1:	#If checked:
		transition_lbl.grid_forget()											#Forget the spacer
		elevateEnt_lbl.grid(row=3, column=0, columnspan=2, sticky="E")			#Grid the label
		elevateEnt_ent.grid(row=3, column=2, columnspan=2, sticky="W", padx=5)	#Grid the entry		
	else:							#If unchecked:
		transition_lbl.grid(row=4, column=0)
		elevateEnt_lbl.grid_forget()												#Forget the label 
		elevateEnt_ent.grid_forget()												#Forget the entry
		elevateEnt_ent.delete(0, END)		
def checkAll():			#scriptRunner_Node_frame: CheckAll Checkbox (On/Off)
	
	if checkAll_btn_var.get() == 1:	#If checked:
		check1_btn.select(), check2_btn.select(), check3_btn.select(), check4_btn.select(), check5_btn.select()					#Check nodes 1-5
		check6_btn.select(), check7_btn.select(), check8_btn.select(), check9_btn.select(), check10_btn.select()				#Check nodes 6-10
	else:							#If unchecked:
		check1_btn.deselect(), check2_btn.deselect(), check3_btn.deselect(), check4_btn.deselect(), check5_btn.deselect()		#Uncheck nodes 1-5
		check6_btn.deselect(), check7_btn.deselect(), check8_btn.deselect(), check9_btn.deselect(), check10_btn.deselect()		#Uncheck nodes 6-10
def rightClick_menu(w):	#SEARCHFORME
	global rightClick
	rightClick = Menu(w, tearoff=0)
	rightClick.add_command(label="Cut")
	rightClick.add_command(label="Copy")
	rightClick.add_command(label="Paste")
def rightClick_action(e):		#SEARCHFORME
	w = e.widget
	rightClick.entryconfigure("Cut",
	command=lambda: w.event_generate("<<Cut>>"))
	rightClick.entryconfigure("Copy",
	command=lambda: w.event_generate("<<Copy>>"))
	rightClick.entryconfigure("Paste",
	command=lambda: w.event_generate("<<Paste>>"))
	rightClick.tk.call("tk_popup", rightClick, e.x_root, e.y_root)
rightClick_menu(window)
		
#Widget Items

#scriptRunner_User_frame:--------------------------------------------
r=0
username_lbl = Label(scriptRunner_User_frame, text="Username:")
username_lbl.grid(row=r, column=0, columnspan=2, sticky="E")
username_ent = Entry(scriptRunner_User_frame)
username_ent.grid(row=r, column=2, columnspan=2, sticky="W", padx=5)
sleep_lbl = Label(scriptRunner_User_frame, text="Sleep Variable:")

sleep_cbx = ttk.Combobox(scriptRunner_User_frame, values=sleepList, width="3")
sleep_cbx.current(sleep_var)


r=1
password_lbl = Label(scriptRunner_User_frame, text="Password:")
password_lbl.grid(row=r, column=0, columnspan=2, sticky="E")
password_ent = Entry(scriptRunner_User_frame, show="*")
password_ent.grid(row=r, column=2, columnspan=2, sticky="W", padx=5)
r=2
elevate_lbl = Label(scriptRunner_User_frame, text="     Elevate Variable:")
elevate_lbl.grid(row=r, column=0, columnspan=2, sticky="E")
elevate_btn = Checkbutton(scriptRunner_User_frame, variable=elevate_btn_var, command=elevate, text="(Optional)")
elevate_btn.grid(row=r, column=2, columnspan=2, sticky="W")
r=3
elevateEnt_lbl = Label(scriptRunner_User_frame, text="Elevate Password:")
elevateEnt_ent = Entry(scriptRunner_User_frame, show="*")
r=4
transition_lbl = Label(scriptRunner_User_frame, text=" ")
transition_lbl.grid(row=r, column=0)

#scriptRunner_Node_frame---------------------------------------------
row=r+1
checkAll_lbl = Label(scriptRunner_Node_frame, text="Check All:")
checkAll_lbl.grid(row=r, column=0, sticky="W")
checkAll_btn = Checkbutton(scriptRunner_Node_frame, variable=checkAll_btn_var, command=checkAll)
checkAll_btn.grid(row=r, column=1, sticky="W")
ipAddress_lbl = Label(scriptRunner_Node_frame,text="IP Address:")
ipAddress_lbl.grid(row=r, column=2, sticky="W")
script_lbl = Label(scriptRunner_Node_frame, text="Script:", padx="5")
script_lbl.grid(row=r, column=3, sticky="W")

status_lbl = Label(scriptRunner_Node_frame, text="Status:")
status_lbl.grid(row=r, column=5, sticky="W")
r=r+1 #Row 1
check1_btn = Checkbutton(scriptRunner_Node_frame, variable=check1_btn_var)
check1_btn.grid(row=r, column=1, sticky="W")
ipEntry1_ent = Entry(scriptRunner_Node_frame)
ipEntry1_ent.grid(row=r, column=2, sticky="W")
combobox1_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)
combobox1_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress1_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress1_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1 #Row 2
check2_btn = Checkbutton(scriptRunner_Node_frame, variable=check2_btn_var)
check2_btn.grid(row=r, column=1, sticky="W")
ipEntry2_ent = Entry(scriptRunner_Node_frame)
ipEntry2_ent.grid(row=r, column=2, sticky="W")
combobox2_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)

combobox2_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress2_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress2_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1 #Row 3
check3_btn = Checkbutton(scriptRunner_Node_frame, variable=check3_btn_var)
check3_btn.grid(row=r, column=1, sticky="W")
ipEntry3_ent = Entry(scriptRunner_Node_frame)
ipEntry3_ent.grid(row=r, column=2, sticky="W")
combobox3_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)
combobox3_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress3_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress3_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1 #Row 4
check4_btn = Checkbutton(scriptRunner_Node_frame, variable=check4_btn_var)
check4_btn.grid(row=r, column=1, sticky="W")
ipEntry4_ent = Entry(scriptRunner_Node_frame)
ipEntry4_ent.grid(row=r, column=2, sticky="W")
combobox4_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)
combobox4_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress4_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress4_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1 #Row 5
check5_btn = Checkbutton(scriptRunner_Node_frame, variable=check5_btn_var)
check5_btn.grid(row=r, column=1, sticky="W")
ipEntry5_ent = Entry(scriptRunner_Node_frame)
ipEntry5_ent.grid(row=r, column=2, sticky="W")
combobox5_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)
combobox5_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress5_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress5_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1 #Row 6
check6_btn = Checkbutton(scriptRunner_Node_frame, variable=check6_btn_var)
check6_btn.grid(row=r, column=1, sticky="W")
ipEntry6_ent = Entry(scriptRunner_Node_frame)
ipEntry6_ent.grid(row=r, column=2, sticky="W")
combobox6_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)
combobox6_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress6_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress6_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1 #Row 7
check7_btn = Checkbutton(scriptRunner_Node_frame, variable=check7_btn_var)
check7_btn.grid(row=r, column=1, sticky="W")
ipEntry7_ent = Entry(scriptRunner_Node_frame)
ipEntry7_ent.grid(row=r, column=2, sticky="W")
combobox7_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)
combobox7_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress7_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress7_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1 #Row 8
check8_btn = Checkbutton(scriptRunner_Node_frame, variable=check8_btn_var)
check8_btn.grid(row=r, column=1, sticky="W")
ipEntry8_ent = Entry(scriptRunner_Node_frame)
ipEntry8_ent.grid(row=r, column=2, sticky="W")
combobox8_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)
combobox8_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress8_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress8_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1 #Row 9
check9_btn = Checkbutton(scriptRunner_Node_frame, variable=check9_btn_var)
check9_btn.grid(row=r, column=1, sticky="W")
ipEntry9_ent = Entry(scriptRunner_Node_frame)
ipEntry9_ent.grid(row=r, column=2, sticky="W")
combobox9_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)
combobox9_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress9_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress9_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1 #Row 10
check10_btn = Checkbutton(scriptRunner_Node_frame, variable=check10_btn_var)
check10_btn.grid(row=r, column=1, sticky="W")
ipEntry10_ent = Entry(scriptRunner_Node_frame)
ipEntry10_ent.grid(row=r, column=2, sticky="W")
combobox10_cbx = ttk.Combobox(scriptRunner_Node_frame, values=scriptList)
combobox10_cbx.grid(row=r, column=3, sticky="W", padx="5")
progress10_pgb = ttk.Progressbar(scriptRunner_Node_frame)
progress10_pgb.grid(row=r, column=5, sticky="W", padx="5")
r=r+1
transition_lbl2 = Label(scriptRunner_Node_frame, text=" ")
transition_lbl2.grid(row=r, column=0)

#Bind right clicks
username_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
password_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
elevateEnt_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)

ipEntry1_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
ipEntry2_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
ipEntry3_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
ipEntry4_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
ipEntry5_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
ipEntry6_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
ipEntry7_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
ipEntry8_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
ipEntry9_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)
ipEntry10_ent.bind("<Button-3><ButtonRelease-3>", rightClick_action)

combobox1_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)
combobox2_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)
combobox3_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)
combobox4_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)
combobox5_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)
combobox6_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)
combobox7_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)
combobox8_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)
combobox9_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)
combobox10_cbx.bind("<Button-3><ButtonRelease-3>", rightClick_action)

#execute_frame-------------------------------------------------------
execute_lbl = Label(execute_frame, text="Start the scripts:")
execute_btn = Button(execute_frame, text="Execute", fg="Green", command=createErrorLists)
execute_btn.pack(side=RIGHT, anchor=W)
execute_lbl.pack(side=LEFT, anchor=W)


#additional_frame
def forget_additional_frame():
	additional_frame.pack_forget()
	editor.pack_forget()
	editor_scrollbar.pack_forget()
	editor_statusbar.pack_forget()
	
	realtime_editor.pack_forget()
	realtime_editor_scrollbar.pack_forget()
	
#Script Realtime
realtime_editor_scrollbar = Scrollbar(additional_frame, orient=VERTICAL)
realtime_editor = Text(additional_frame, height="24", width="60", bg="black", wrap=WORD, fg="white", yscrollcommand=realtime_editor_scrollbar.set)
realtime_editor.bind("<Button-3><ButtonRelease-3>", rightClick_action)
realtime_editor_scrollbar.config(command=realtime_editor.yview)
realtime_editor.see("end")

#e1.bind_class("Entry", "<Button-3><ButtonRelease-3>", rightClick_action)
#Script Editor 
editor_scrollbar = Scrollbar(additional_frame, orient=VERTICAL) 	
editor = Text(additional_frame, height="22", width="60", cursor="xterm", wrap=WORD, yscrollcommand=editor_scrollbar.set)	
editor.bind("<Button-3><ButtonRelease-3>", rightClick_action)	
editor_scrollbar.config(command=editor.yview)
editor_statusbar = Label(additional_frame, text="Currently Editing:"+scriptFile_name)

#------------------------------------------------------------!Widgets

#Window Loop---------------------------------------------------------
window.bind("<Control-e>", scriptEditor_toggle_Hotkey)
window.bind("<Control-r>", scriptRealtime_toggle_Hotkey)
window.config(menu=menubar)
populate_ScriptList()
window.mainloop()
endProgram_var = 1
#--------------------------------------------------------!Window Loop



