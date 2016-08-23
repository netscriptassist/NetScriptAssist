===========================
NetScript Assist: Help File
===========================
- - - - - - - - - 
Table of Contents:
- - - - - - - - - 
    Introduction - Important Tips and Tricks
	
	Part 1- Script Editor
          1a- Writing Basic Scripts
          1b- Writing Scripts with Variables
            1b.1- List of Variables
            1b.2- Example Script with Variables

    Part 2- Script Runner
          2a- Creating/Executing a 'Runner' File
		  2b- Editing the Sleep Variable

    Part 3- Script Realtime
          3a- About Script Realtime
          3b- Saving Script Realtime - Logs

    Part 4- About NetScript Assist
          4a- Additional Tips and Tricks
          4b- Contact NetScript Assist
               -Feedback / Additional Help
--------------------------------------------
- - - - - - - - - - - - - - - - - - - -
Introduction- Important Tips and Tricks
- - - - - - - - - - - - - - - - - - - -
Tips/Tricks:
	- Always test your scripts before using them in production
	- Use the 'Test Connections' (File -> Test Connections)
	  to check your connectivity to the devices in your Script Runner

- - - - - - - - - - -
Part 1- Script Editor
- - - - - - - - - - -
***The NetScript Assist: Script Editor is where you will create and edit scripts. 
   Once you have created the scripts, you are ready to use the 'Script Runner'.

   You don't have to know coding in order to write a useful script. 
   The script acts just like you are typing each line into the remote session.

   NetScript Assist sends the script one line at a time

Tips/Tricks:
     - TEST YOUR SCRIPTS BEFORE YOU USE THEM IN PRODUCTION
     - <Ctrl+E> is the shortcut key command to bring up
        'Script Editor'
     - Make sure that you account for any dialog box that might appear   
	 - If you want to capture all of a command on Cisco devices, use the 
	   'terminal length 0' command in your script. 

1a- Writing Basic Scripts

     - Every line that you type in the 'Script Editor' will
        be entered into the remote device seprately.  

     Example:(Requires elevation)
       copy run start 
       startup-config

     Example2:(Requires elevation)
       copy run start
       [blank linebreak (enter) to accept default 'startup-config']

1b- Writing Scripts with Variables
     
     1b.1- List of Variables you can use:
           --------------------------------
           # (Text for a comment)       [The line will not be sent]

           $username                    [The Username entered in 'Script Runner']
           $password                    [The Password entered in 'Script Runner']
           $elevatepassword             [The Elevate Password entered in 'Script Runner']
           $date                        [The Current Date (Format: MM-DD-YY)]

     1b.2- Example Script using Variables:
           -------------------------------
           Example: (Requires elevation)
              copy run tftp
              #[IP Address of a test TFTP server]
              1.1.1.254
              SwitchBackup_$username_$date
             
           Example2: (Custom elevation)
              enable
              $elevatepassword
              copy run tftp
              #[IP Address of a test TFTP server]
              1.1.1.254
              SwitchBackup_$username_$date
--------------------------------------------
- - - - - - - - - - -
Part 2- Script Runner
- - - - - - - - - - -
Tips/Tricks:
     - Use the check all button to run all nodes
     - The Status bar shows which device your script is executing on.
	 - Use the 'Test Connections' option under File -> Test Connections to make
	   sure the device can connect.

2a- Creating/Executing a 'Runner' File
     - Note: You can save and open your 'Runner' file! 
             *See Edit -> Script Runner
			 (It will not save your username, password, or elevate password.)
			 
     Step 1:  Enter a username and password.
          Step 1a(optional): If the Script needs 'elevated' and is a cisco device, use the 
                             Elevate Scripts checkbox.
     
     Step 2:  Enter IP Addresses of the devices you want to run a script on.

     Step 3:  Select a Script from the dropdown box

     Step 4:  Check the devices you would like to execute your scripts on
          Step 4a(optional): If you want to run all devices, use the 'Check All' box.

     Step 5:  Click the 'Execute' button on the 'Start the scripts' section. 

2b- Editing the sleep variable
	- Note: The Sleep Variable is how long each command will wait before it is entered 
	        into the console. (By default, the sleep variable is set to 2.)
			
	- Note:	This is important to note because slower devices will need 
			more time to parse the input. 
	
	You can edit the sleep timer by going to Edit -> Script Runner -> Edit Sleep Variable
	
--------------------------------------------
- - - - - - - - - - -
Part 3- Script Realtime
- - - - - - - - - - -

3a- About Script Realtime
     - Script Realtime can be opened at anytime by clicking Edit -> Script Realtime -> Script Realtime
        You can also open it by using <Ctrl+R>

     - Script Realtime shows what Script Runner is currently sending.

3b- Saving Script Realtime - Logs
     - You can clear/open/save the Script Realtime log by clicking 
        Edit -> Script Realtime -> New/Open/Save
--------------------------------------------
- - - - - - - - - - -
Part 4- About NetScript Assist
- - - - - - - - - - -

4a- Additional Tips and Tricks
    - Use Shortcut keys to open the following windows:
       <Ctrl+E> NetScript Assist: Script Editor
       <Ctrl+R> NetScript Assist: Script Realtime

    - I recommend testing your script manually to account for
       any dialog message that might occur on the device.

    - I always test my scripts using a test device before using
       my script in production. 


4b- Contact NetScript Assist
     -For any feedback or additional assistance, you can email me at 
       'NetScriptAssist@gmail.com'. I will try to contact you back as 
       soon as possible. 
=================================================================================

Closing Notes:
I have a Networking background and wanted to kindle my love for programming. 
I put my heart into this program and I think the end result will show. If 
you have any comments/questions/concerns, please let me know. 
Email: NetScriptAssist@gmail.com

I am not an expert programmer or app developer so I am sure there will be
plenty of constructive feedback I will use for the future. 

To conclude, this program was built because I did not want to write a bunch of
scripts to complete simple tasks. I found myself re-writing (copy/paste)a bunch 
of my code for every program I would run.

=================================================================================

  _   _      _   ____            _       _        _            _     _   
 | \ | | ___| |_/ ___|  ___ _ __(_)_ __ | |_     / \   ___ ___(_)___| |_ 
 |  \| |/ _ | __\___ \ / __| '__| | '_ \| __|   / _ \ / __/ __| / __| __|
 | |\  |  __| |_ ___) | (__| |  | | |_) | |_   / ___ \\__ \__ | \__ | |_ 
 |_| \_|\___|\__|____/ \___|_|  |_| .__/ \__| /_/   \_|___|___|_|___/\__|
                                  |_| 

 If you found this program helpful, please tell a friend. :)