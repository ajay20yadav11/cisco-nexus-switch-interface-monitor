Introduction-

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
	

