import collections
import subprocess
import os
import re
import time
from collections import namedtuple
import configparser
from colorama import init, Fore, Back, Style

#### COLOR SACTIONS ####
init()
FORES = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
BRIGHTNESS = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]
def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


#### WINDOWS SACTION ####
def get_windows_ssids():
    cmd_command = subprocess.check_output("netsh wlan show profiles").decode()
    ssids = []

    profiles = re.findall(r"All User Profile\s(.*)", cmd_command)
    for profile in profiles:
        ssid = profile.strip().strip(":").strip()
        ssids.append(ssid)
    return ssids

def saved_passwords_windows(verbose=1):
    ssids =get_windows_ssids()
    Profile = namedtuple("Profile", ["ssid", "ciphers","authentications" , "key"])

    profiles = []

    for ssid in ssids:
        ssid_deta = subprocess.check_output(f"""netsh wlan show profile "{ssid}" key=clear""").decode()
        ciphers = re.findall(r"Cipher\s(.*)",ssid_deta)
        ciphers = "/".join([c.strip().strip(":").strip() for c in ciphers])
        authentications = re.findall(r"Authentication\s(.*)",ssid_deta)
        authentications = "/".join([a.strip().strip(":").strip() for a in authentications])
        authentications = authentications[0:13]
        key = re.findall(r"Key Content\s(.*)",ssid_deta)
        try:
            key = key[0].strip().strip(":").strip()
        except IndexError:
            key = "Not found"
        profile = Profile(ssid=ssid, ciphers=ciphers,authentications=authentications, key=key)
        if verbose >=1:
            print_windows_profile(profile)
            profiles.append(profile)
    return profiles


def print_windows_profile(profile):
    print_with_color(f"{profile.ssid:25}{profile.ciphers:15}{profile.authentications:15}{profile.key:50}",color=Fore.GREEN,brightness=Style.BRIGHT)
    time.sleep(0.4)



def loding(name,name2):
    print(f"====== start loading {name} and extrcting {name2} ======")
    print("******")
    time.sleep(0.5)
    print("##****")
    time.sleep(0.5)
    print("####**")
    time.sleep(0.5)
    print("######")


#### MAIN FUNCTION ####

answer = input("welceome to the WPA \n"
               "do you wont to strat exctract wi-fi password form your local machine? yes/no\n")
if answer[0].lower() == "y":
    print_with_color("This script may only be used for academic and research purposes. The user is entirely responsible for any usage that is not for these purposes.",color=Fore.RED,brightness=Style.DIM)
    try:
        loding("ssids profiles","WI-FI passwords")
        print_with_color("Network's name ========= Ciphers ====== Encryption === password",color=Fore.MAGENTA,brightness=Style.NORMAL)
        get_windows_ssids()
        saved_passwords_windows()
        print_windows_profile(profiles)
    except NameError:
        time.sleep(0.7)
        print("Not found more saved password. have nice day!")
if answer[0].lower() == "n":
    print("have ncie day!")