#!/usr/bin/env python
# Title........: MacAnonymizer
# Description..: This is a Python script for Linux systems to change mac address.
# Author.......: SoftAddict
# Version......: 1.0
# Usage........: python3 MacAnonymizer.py -i "interface" and -m "targetmac"
# Python Version.: 3
import re
import subprocess
import optparse
import colorama
from colorama import Fore, Style


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error(Fore.RED + "[-] Oopsie, Please specify an interface, use --help for more info.")
        # code to handle error
    elif not options.new_mac:
        parser.error(Fore.RED + "[-] Oops, Please specify a new mac, use --help or -h for more info.")
    return options

    # code to handle error


def change_mac(interface, new_mac):
    print(Fore.GREEN + "[+] Initializing...")
    print(Fore.GREEN + "[+] Summoning the mac changer wizard")
    print(Fore.GREEN + "[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])



def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print(Fore.RED + "[-] Could not read MAC address.")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(Fore.GREEN + "[+] MAC address successfully changed to " + current_mac)
else:
    print(Fore.RED + "[-] MAC address did not get changed.")
