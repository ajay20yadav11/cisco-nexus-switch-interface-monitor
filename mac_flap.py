#!/bin/env python
import smtplib
from cli import cli
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cisco.vrf import *
from cisco import *
import re
from datetime import date, datetime
import time
from datetime import datetime, timedelta, date
from time import gmtime, strftime

time_now = strftime("%m:%d:%H:%M:%S", time.localtime())
set_global_vrf('default')
tdelta = 0
old_problem = []

def mail():
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y_%H-%M-%S")
    old_hostname = cli("show hostname")
    hostname = old_hostname.strip()
    me = str(hostname) + "@tcscbi.com"
    you = ['network_operation@company.com', 'security_operation@company.com', 'network_lead@company.com']
    msg = MIMEMultipart("alternative")
    msg["Subject"] = str(hostname) + "__MAC FLAP OCCURED"
    msg["From"] = me
    msg["To"] = ','.join(you)
    text2 = (
        "\n Check for MAC FLAP LOGS"
        + "\n"
    )
    interface_full_data = "show logging last 250"
    text6 = cli(interface_full_data)
    text = (
		text2
        + "\n\n\n"
        + str(text6)
    )
    part1 = MIMEText(text, "plain")
    msg.attach(part1)
    s = smtplib.SMTP("10.100.100.100", 25)
    s.sendmail(me, you, msg.as_string())
    s.quit()


def find_time(s1, s2, FMT):
    global tdelta
    tdelta = datetime.strptime(s1, FMT) - datetime.strptime(s2, FMT)

def to_execute():
    global old_problem, time_now, tdelta
    tdelta = 0
    old_never_log_time, never_log_time, diff_time_log, raw_log, output, log_time, old_problem,  = [],[],[],[],[],[],[] 

    output = cli("show logging")  
    text1 = output.split("\n")
    text = text1[-100:]
    raw_log = []
    #now to filter out only mac related logs from collected logs
    raw_log = [ anim for anim in text if 'MAC_MOVE' in anim ]
    old_never_log_time = []
    #to extract the date and time information from mac flap
    for line in raw_log:
        match = re.findall(r"\w+ +\d+ \d+:\d+:\d+", line)
        old_never_log_time.append(match)
    never_log_time = []
    for inter in old_never_log_time:
        never_log_time.append(inter[0])
    log_time = []
    for animated in never_log_time:
        animated1 = animated.replace("  ", " ")
        animated2 = animated1.replace(" ", ":")
        if "Jan" in animated2:
            log_time.append(animated2.replace("Jan", "01"))
        elif "Feb" in animated2:
            log_time.append(animated2.replace("Feb", "02"))
        elif "Mar" in animated2:
            log_time.append(animated2.replace("Mar", "03"))
        elif "Apr" in animated2:
            log_time.append(animated2.replace("Apr", "04"))
        elif "May" in animated2:
            log_time.append(animated2.replace("May", "05"))
        elif "Jun" in animated2:
            log_time.append(animated2.replace("Jun", "06"))
        elif "Jul" in animated2:
            log_time.append(animated2.replace("Jul", "07"))
        elif "Aug" in animated2:
            log_time.append(animated2.replace("Aug", "08"))
        elif "Sep" in animated2:
            log_time.append(animated2.replace("Sep", "09"))
        elif "Oct" in animated2:
            log_time.append(animated2.replace("Oct", "10"))
        elif "Nov" in animated2:
            log_time.append(animated2.replace("Nov", "11"))
        elif "Dec" in animated2:
            log_time.append(animated2.replace("Dec", "12"))
    new_time_diff = []
    for line in log_time:
        find_time(time_now, line, "%m:%d:%H:%M:%S")
        new_time_diff.append(tdelta)
    to_compare_2 = timedelta(hours=1)
    new_mac_problem = [ anim for anim in new_time_diff if anim < to_compare_2 ]
    all_time_diff = [ str(anim) for anim in new_mac_problem ]
    diff_time_log = []
    for i in range(len(all_time_diff) - 1):
        find_time(
              all_time_diff[i], all_time_diff[i+1], "%H:%M:%S"
        )
        diff_time_log.append(tdelta)
    to_compare = timedelta(minutes=15)
    old_problem = [ str(anim) for anim in diff_time_log if anim < to_compare ]
            
to_execute()
            
if len(old_problem) > 5:
	mail()
