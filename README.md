**Introduction**
- The code is designed to work on Nexus Switches Family platforms that support Python Platform 2.7 or greater.
- It uses the `smtplib` module for sending email alerts and Cisco CLI module for interacting with Cisco Nexus switches.
- smtplib- https://docs.python.org/3/library/smtplib.html

**Need for the Code**
- The code is useful for monitoring parameters like CRF, INPUT ERROR, OUTPUT ERROR, GIANTS, COLLISION, etc., of network interfaces.
- It provides proactive monitoring of physical interface parameters at the Level 1 Physical layer.

**How to Use the Code on Nexus Switches**
1. Upload the file named `monitor-interface.py` to the flash file of the Nexus switch.
2. Execute the script within privilege mode using either `python monitor-interface.py` or `python3 monitor-interface.py`.
3. The script will send email alerts if it detects any changes in the interface parameter values.

**Applying Scheduling Configuration on Nexus Switches**
- https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/6-x/system_management/configuration/guide/b_Cisco_Nexus_9000_Series_NX-OS_System_Management_Configuration_Guide/sm_8scheduler.html
- To run the code automatically at specified intervals, you need to configure scheduling on Nexus switches.
- Refer to the provided documentation link for details on scheduling configuration.
- Example scheduling configuration is provided, which runs the script every 10 minutes.

**Wrapping Up**
1. The code is ready to be executed on Nexus switches.
2. Scheduling configuration is applied to run the code at specific intervals (e.g., every 10 minutes).
3. The code will send email alerts if it detects changes in interface parameter values.

This script can be a valuable tool for monitoring network interfaces on Cisco Nexus switches and receiving timely alerts when issues occur.
