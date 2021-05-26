Introduction
This code will only work on Nexus Switches Family platform that supports Python Platform 2.7 or greater.
Modules:
Following are the modules which comes pre-packed with the nexus box. So, no need to install any of the external modules for the code to work.
smtplib- https://docs.python.org/3/library/smtplib.html
cisco & cli- 
https://content.cisco.com/chapter.sjs?uri=/searchable/chapter/content/en/us/td/docs/ios-xml/ios/prog/configuration/1612/b_1612_programmability_cg/cli_python_module.html.xm

Need of this code-
Parameters: CRF, INTPUT ERROR, OUTPUT ERROR, GIANTS, COLLISION, etc.
About all the monitoring tools available in the market, this code serves as a time bound monitoring for the interface’s parameters for its errors.
When it comes to monitor the basic Level 1 Physical layer, we need to proactively monitor the parameters of physical interface. 

About How to Use the Code in Nexus Switches-

1. First we need to upload the file monitor-interface.py into the flash file.
2. We could execute this script within the privilege mode.
	nexus#python monitor-interface.py  
			OR
	nexus#python3 monitor-interface.py  
3. By executing this script, we will get the email alerts if the code has detected any change in the interface parameter value.




Apply Scheduling Configuration on Nexus Switches-

Now to make this code run automatically after a specified time we need to now configure scheduling feature on Nexus Switches.
For more information on Scheduling Configuration, kindly refer below document
https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/6-x/system_management/configuration/guide/b_Cisco_Nexus_9000_Series_NX-OS_System_Management_Configuration_Guide/sm_8scheduler.html
E.g.
switch(config)# feature scheduler
switch(config)# scheduler job name MONITOR_INTERFACE
switch(config-job)# python monitor-interface.py

		OR

switch(config-job)# python3 monitor-interface.py

switch(config)# scheduler schedule name REGULAR_INTERVAL
switch(config-schedule)# job name MONITOR_INTERFACE
switch(config-schedule)# time start now repeat 0:10




Wrapping Up-
1.	Code is ready to be executed
2.	Scheduling configuration is applied to run the code after the specific time


Now after every 10 min code will be executed and we will get email alerts if any change in the value has been detected by code.

 

