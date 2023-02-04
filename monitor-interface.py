#!/bin/env python


import smtplib
import cisco
from cli import cli
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cisco.vrf import *
from cisco import *
import re
import sys
from datetime import date, datetime
import time

set_global_vrf("default")
updated_network = {}
updated_non_network = {}
old_updated_network = {}
new_updated_network = {}
old_network_data = {}
new_network_data = {}
old_updated_non_network = {}
new_updated_non_network = {}
problem_network_interface = {}
problem_non_network_interface = {}
old_network_data = {}
old_non_network_data = {}

filter_giants = "\s* runts (.*) giants \s*"
filter_crc = "\s* giants (.*) CRC \s*"
filter_input_error = "\s (.*) input error  0 short frame \s"
filter_output_error = "\s (.*) output error  0 collision \s"
filter_collision = "\s output error  (.*) collision \s"

giants_print = "show int | grep CRC"
crc_print = "show int | grep CRC"
input_error_print = "show int | grep overrun"
output_error_print = "show int | grep collision"
collision_print = "show int | grep collision"


# FOR MAIL ALERTS THROUGH SMTP SERVER
def mail(alpha, beta, charlie, delta, actual, owner):
    b = str(charlie[alpha])
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y_%H-%M-%S")
    old_hostname = cli("show hostname")
    hostname = old_hostname.strip()
    me = (
            str(hostname) + "@my_email_id"
    )  # SENDER EMAIL ID PREFERABLY DEVICE HOSTNAME
    you = [
        "your_email_id@organisation.com",
        "team_email_id@organisation.com",
    ]  # RECEIVER EMAIL ID
    msg = MIMEMultipart("alternative")
    # SUBJECT CAN BE CUSTOMAZIED AS PER REQURIEMENT
    msg["Subject"] = (
            str(hostname)
            + "_"
            + str(owner).upper()
            + "_{}_ERROR".format(str(actual)).upper()
            + "___"
            + str(alpha).upper()
    )
    msg["From"] = me
    msg["To"] = ",".join(you)

    # DESIGNED TEXT FOR THE BODY OF MAIL
    text1 = delta
    text2 = (
            "\n Check for the {} value on interface ".format(str(actual))
            + str(alpha)
            + "\n"
    )

    # PRINTS THE DIFFERENCE IN VALUE OF THE MONITORED ERROR PARAMETER
    text3 = (
            "\n The difference in the {} value between 5 minutes is : ".format(
                str(actual)
            )
            + str(beta)
            + "\n"
    )

    # PRINTS THE CURRENT INTERFACE PARAMTER VALUE
    text4 = (
            "\n Current {} value on interface " + str(alpha) + " is :" + b + "\n"
    ).format(str(actual))
    text5 = (
            "\n Date and Time during which the increase in INTPUT error value has been reported: "
            + dt_string
    )
    interface_full_data = "show int " + str(alpha)

    # CONSOLIDATED TEXT
    text6 = cli(interface_full_data)
    text = (
            text1
            + text2
            + text3
            + text4
            + text5
            + "\n\n\n"
            + "*" * 25
            + "\n\n\n"
            + text6
    )
    part1 = MIMEText(text, "plain")
    msg.attach(part1)
    s = smtplib.SMTP(
        "192.168.0.25", 25
    )  # IP ADDRESS DEPENDS AS PER YOUR ORGANISATION IP, USED DUMMY IP 192.168.0.25
    s.sendmail(me, you, msg.as_string())
    s.quit()


def to_execute(magic, to_print_from):

    global network_final_output_to_mail, network_working_data
    global non_network_working_data, non_network_final_output_to_mail
    counter_value = []
    crc_value = []
    network_final_output_to_mail = {}
    non_network_final_output_to_mail = {}
    network_working_data = {}
    non_network_working_data = {}

    # TO GET THE INTERFACE NAME
    old_all_int = cli("show int desc | i Eth|Po")
    all_interface = old_all_int.split("\n")
    final_all_interface = [dum1[0:7] for dum1 in all_interface]
    # TO GET THE INTERFACE THAT ARE NETWORK PORT, CAN BE FETCHED IF THE DESCRIPTION OF THE PORT IS MARKED AS NETWORK
    old_interface = cli("show int desc | i NETWORK_PORT")
    actual_interface = old_interface.split("\n")

    # FROM RAW OUTPUT ONLY EXTRACT THE INTERFACE NAME
    only_network_interface = [str(dum2[0:7]) for dum2 in actual_interface]

    # NOW TO MONITOR THE INTERFACE ERROR OF A PARTICULAR PARAMETER
    crc = cli(to_print_from)
    s = crc.split("\n")
    counter = 1
    for line in s:
        the_magic = re.search(
            magic, line
        )  # MAGIC HAS THE REFIX STING FORMAT THAT CAN EXTRACT THE INTERFACE ERROR VALUE OF A MONITORED PARAMETER
        if the_magic and the_magic.group(1):
            if int(the_magic.group(1)) > 0:
                counter_value.append(counter)
                crc_value.append(the_magic.group(1))
        counter += 1
    new_counter_value = [z for z in counter_value]
    to_the_magic_final_all_interface = [final_all_interface[y] for y in new_counter_value]
    # CREATE A DICTIONARY FOR INTERFACE NAME ALONG WITH ITS ERROR VALU
    all_interface_with_crc_values = dict(
        zip(to_the_magic_final_all_interface, crc_value)
    )
    final_network_crc_interface = list(
        set(to_the_magic_final_all_interface) & set(only_network_interface)
    )
    new_all_interface = list(
        set(to_the_magic_final_all_interface) & set(final_all_interface)
    )
    new_all_interface.sort()
    final_network_crc_interface.sort()
    final_all_interface_only_crc_value = [all_interface_with_crc_values[a] for a in all_interface_with_crc_values]
    final_network_crc_interface_value = [all_interface_with_crc_values[a] for a in final_network_crc_interface]

    # NOW TO MONITOR THE NON NETWORK PORT BY DIFFERENTIATING BETWEEN ALL INTERFACE AND NETWORK INTERFACE
    only_non_network_interface = list(
        set(new_all_interface).difference(final_network_crc_interface)
    )
    only_non_network_interface.sort()
    only_non_network_interface_crc_value = [all_interface_with_crc_values[a] for a in only_non_network_interface]
    for key1 in final_network_crc_interface:
        for value1 in final_network_crc_interface_value:
            network_final_output_to_mail[key1] = value1
            final_network_crc_interface_value.remove(value1)
            break
    network_working_data = network_final_output_to_mail
    for key1 in only_non_network_interface:
        for value1 in only_non_network_interface_crc_value:
            non_network_final_output_to_mail[key1] = value1
            only_non_network_interface_crc_value.remove(value1)
            break
    non_network_working_data = non_network_final_output_to_mail


def quater_next(
        old_phase_network,
        new_phase_network,
        old_phase_server,
        new_phase_server,
        actual,
):
    new_updated_non_network = {}
    problem_non_network_interface = {}
    new_updated_network = {}
    problem_network_interface = {}

    # NETWORK AND NON-NETWORK INTEFACE DETAIL WITH OLD AND NEW INTERFACE VALUE BETWEEN A TIME DIFFERENCE OF 5 MINUTES
    for item, nooe in old_phase_network.items():
        old_updated_network[item] = int(nooe)
    for item, nooe in new_phase_network.items():
        new_updated_network[item] = int(nooe)
    for item, nooe in old_phase_server.items():
        old_updated_non_network[item] = int(nooe)
    for item, nooe in new_phase_server.items():
        new_updated_non_network[item] = int(nooe)
    updated_network = {
        key: new_updated_network[key] - old_updated_network.get(key, 0)
        for key in new_updated_network
    }

    # MAKE A DICTIONARY IF THE DIFFERENCE IN THE INTERFACE VALUE BETWEEEN 5 MINUTES IS GREATER THAN 0
    for key, value in updated_network.items():
        if value > 0:
            problem_network_interface[key] = value
    updated_non_network = {
        key: new_updated_non_network[key] - old_updated_non_network.get(key, 0)
        for key in new_updated_non_network
    }
    for key, value in updated_non_network.items():
        if value > 0:
            problem_non_network_interface[key] = value

    # NOW TO USE MAIL FUNCTION FOR SMTP ALERTS OF THE INTERFACE THAT ARE HAVING ERRORS
    for key, value in problem_network_interface.items():
        to_display = (
                "\n" + "*" * 10 + "For Network Interface" + "*" * 10 + "\n"
        )
        nature = "Network"
        mail(key, value, new_updated_network, to_display, actual, nature)
    for key, value in problem_non_network_interface.items():
        to_display = "\n" + "*" * 10 + "For Server Interface" + "*" * 10 + "\n"
        nature = "Server"
        mail(key, value, new_updated_non_network, to_display, actual, nature)


# NOW TO DEFINE THE RESPECTIVE FUNCTION FOR OLDER VALUE
def older_value(magic, to_print_from):
    global old_network_data, network_working_data
    global old_non_network_data, non_network_working_data
    to_execute(magic, to_print_from)
    old_network_data = network_working_data
    old_non_network_data = non_network_working_data


# NOW TO DEFINE THE RESPECTIVE FUNCTION FOR NEWER VALUE
def newer_value(magic, to_print_from):
    global new_network_data, new_non_network_data
    global network_working_data, non_network_working_data
    to_execute(magic, to_print_from)
    new_network_data = network_working_data
    new_non_network_data = non_network_working_data


# NOW TO APPLY THE RESPECTIVE FUNCTION FOR OLDER VALUE FOR VARIOUS PARAMETERS
older_value(filter_crc, crc_print)
crc_old_network_data = {}
crc_old_non_network_data = {}
crc_old_network_data = old_network_data
crc_old_non_network_data = old_non_network_data
older_value(filter_giants, giants_print)
giants_old_network_data = {}
giants_old_non_network_data = {}
giants_old_network_data = old_network_data
giants_old_non_network_data = old_non_network_data
older_value(filter_input_error, input_error_print)
input_error_old_network_data = {}
input_error_old_non_network_data = {}
input_error_old_network_data = old_network_data
input_error_old_non_network_data = old_non_network_data
older_value(filter_output_error, output_error_print)
output_error_old_network_data = {}
output_error_old_non_network_data = {}
output_error_old_network_data = old_network_data
output_error_old_non_network_data = old_non_network_data
older_value(filter_collision, collision_print)
collision_old_network_data = {}
collision_old_non_network_data = {}
collision_old_network_data = old_network_data
collision_old_non_network_data = old_non_network_data

# WAIT FOR 5 MINUTES
time.sleep(300)

# NOW TO APPLY THE RESPECTIVE FUNCTION FOR NEWER VALUE FOR VARIOUS PARAMETERS
newer_value(filter_crc, crc_print)
crc_new_network_data = {}
crc_new_non_network_data = {}
crc_new_network_data = new_network_data
crc_new_non_network_data = new_non_network_data
newer_value(filter_giants, giants_print)
giants_new_network_data = {}
giants_new_non_network_data = {}
giants_new_network_data = new_network_data
giants_new_non_network_data = new_non_network_data
newer_value(filter_input_error, input_error_print)
input_error_new_network_data = {}
input_error_new_non_network_data = {}
input_error_new_network_data = new_network_data
input_error_new_non_network_data = new_non_network_data
newer_value(filter_output_error, output_error_print)
output_error_new_network_data = {}
output_error_new_non_network_data = {}
output_error_new_network_data = new_network_data
output_error_new_non_network_data = new_non_network_data
newer_value(filter_collision, collision_print)
collision_new_network_data = {}
collision_new_non_network_data = {}
collision_new_network_data = new_network_data
collision_new_non_network_data = new_non_network_data

for exe in ["CRC", "giants", "input_error", "output_error", "collision"]:
    quater_next(
        crc_old_network_data,
        crc_new_network_data,
        crc_old_non_network_data,
        crc_new_non_network_data,
        exe,
    )
