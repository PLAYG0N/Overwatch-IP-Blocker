import subprocess, ctypes, os, sys
from subprocess import Popen, DEVNULL

#Region NA, EU or AS

Region="1OverwatchNA"

def check_admin():
    try:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        isAdmin = False
    if not isAdmin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def add_rule(rule_name,iprange):
    subprocess.call(
        f"netsh advfirewall firewall add rule name={rule_name} dir=out action=block enable=no remoteip={iprange}", 
        shell=True, 
        stdout=DEVNULL, 
        stderr=DEVNULL
    )
    subprocess.call(
        f"netsh advfirewall firewall add rule name={rule_name} dir=in action=block enable=no remoteip={iprange}", 
        shell=True, 
        stdout=DEVNULL, 
        stderr=DEVNULL
    )
    print(f"Rule {rule_name} for In and Out added")

def modify_rule(rule_name, state):
    state, message = ("yes", "Enabled") if state else ("no", "Disabled")
    subprocess.call(
        f"netsh advfirewall firewall set rule name={rule_name} new enable={state}", 
        shell=True, 
        stdout=DEVNULL, 
        stderr=DEVNULL
    )
    print(f"Rule {rule_name} {message}")

check_admin()

Start=input("Swap to " +Region+"?(y/n) Type first on first startup to create the rules: ")
if (Start=="first"):
    add_rule(Region,"5.42.168.0-5.42.175.255,5.42.184.0,5.42.187.0-5.42.187.255,5.42.188.0-5.42.188.255,5.42.189.0-5.42.189.255,5.42.191.0-5.42.191.255,157.175.0.0-157.175.255.255,15.185.0.0-15.185.255.255,15.184.0.0-15.184.255.255,5.42.190.0-5.42.190.255")
    Start=input("Swap to " +Region+"?(y/n)")

if (Start=="y"or "yes"):
    modify_rule(Region,"yes")
    inp=input("Stop?(y)")

if (inp=="y"):
    modify_rule(Region,0)
    Start=input("Swap to " +Region+"?(y/n)")

if (Start=="n" or "no"):
    exit()
