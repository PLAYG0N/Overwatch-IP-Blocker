import subprocess, ctypes, os, sys
from subprocess import Popen, DEVNULL

import sys

import PySimpleGUI as sg

def check_admin():
    try:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        isAdmin = False
    if not isAdmin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

def add_rule(rule_name,iprange):

    #delete old
    subprocess.call(
        f"netsh advfirewall firewall delete rule name={rule_name} dir=out", 
        shell=True, 
        stdout=DEVNULL, 
        stderr=DEVNULL
    )


    subprocess.call(
        f"netsh advfirewall firewall delete rule name={rule_name} dir=in", 
        shell=True, 
        stdout=DEVNULL, 
        stderr=DEVNULL
    )

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

def readips():

    successful=False

    try:
        file = open("OverwatchIPList.txt","r")

        successful=True

    except:
        file=open("OverwatchIPList.txt","w")

        NAIPS="5.42.168.0-5.42.175.255,5.42.184.0-5.42.191.255,24.105.8.0-24.105.15.255,157.175.0.0-157.175.255.255,15.185.0.0-15.185.255.255,15.184.0.0-15.184.255.255,37.244.42.0-37.244.42.255,104.198.0.0-104.198.255.255,34.84.0.0-34.84.255.255,34.85.0.0-34.85.255.255,35.200.0.0-35.200.255.255,35.221.0.0-35.221.255.255,34.146.0.0-34.146.255.255,117.52.0.0-117.52.255.255,121.254.0.0-121.254.255.255,5.42.0.0-5.42.255.255"
        EUIPS="15.177.0.0-15.177.255.255,15.228.0.0-15.228.255.255,170.84.0.0-170.84.255.255,177.71.0.0-177.71.255.255,18.228.0.0-18.231.255.255,200.10.0.0-200.10.255.255,200.29.0.0-200.29.255.255,200.32.0.0-200.32.255.255,34.0.0.0-35.255.255.255,52.207.0.0-52.207.255.255,52.67.0.0-52.67.255.255,52.94.0.0-52.95.255.255,54.207.0.0-54.207.255.255,54.232.0.0-54.233.255.255,54.240.0.0-54.240.255.255,54.94.0.0-54.94.255.255,64.252.0.0-64.252.255.255,99.77.0.0-99.77.255.255,24.105.40.0-24.105.47.255,24.105.8.0-24.105.15.255,37.244.42.0-37.244.42.255,104.198.0.0-104.198.255.255,34.84.0.0-34.84.255.255,34.85.0.0-34.85.255.255,35.200.0.0-35.200.255.255,35.221.0.0-35.221.255.255,34.146.0.0-34.146.255.255,117.52.0.0-117.52.255.255,121.254.0.0-121.254.255.255,5.42.0.0-5.42.255.255"
        ASIAIPS="5.42.168.0-5.42.175.255,5.42.184.0-5.42.191.255,24.105.8.0-24.105.15.255,15.177.0.0-15.177.255.255,15.228.0.0-15.228.255.255,170.84.0.0-170.84.255.255,177.71.0.0-177.71.255.255,18.228.0.0-18.231.255.255,200.10.0.0-200.10.255.255,200.29.0.0-200.29.255.255,200.32.0.0-200.32.255.255,34.0.0.0-35.255.255.255,52.207.0.0-52.207.255.255,52.67.0.0-52.67.255.255,52.94.0.0-52.95.255.255,54.207.0.0-54.207.255.255,54.232.0.0-54.233.255.255,54.240.0.0-54.240.255.255,54.94.0.0-54.94.255.255,64.252.0.0-64.252.255.255,99.77.0.0-99.77.255.255,24.105.40.0-24.105.47.255,24.105.8.0-24.105.15.255"
        CUSTOMIPS=""

        file.write("NA:"+ NAIPS +"\n"+"EU:"+ EUIPS+ "\nAsia:"+ASIAIPS+ "\nCustom:\nVersion 1.0.0")

        print("NewFile")

    if(successful):
        NAIPS=file.readline()
        NAIPS=NAIPS[NAIPS.find(":")+1:].rstrip("\n")
        EUIPS=file.readline()
        EUIPS=EUIPS[EUIPS.find(":")+1:].rstrip("\n")
        ASIAIPS=file.readline()
        ASIAIPS=ASIAIPS[ASIAIPS.find(":")+1:].rstrip("\n")
        CUSTOMIPS=file.readline()
        CUSTOMIPS=CUSTOMIPS[CUSTOMIPS.find(":")+1:].rstrip("\n")

        

    return [NAIPS,EUIPS,ASIAIPS,CUSTOMIPS]


check_admin()



#GUI Stuff

layout = [[sg.Text('Current Region: Default',size=(45,2),key='Status')],
        [sg.Button('Create rules',tooltip="Creates the firewall rules", button_color=('white', 'lightblue'), key='Rules'),
        sg.Button('NA', button_color=('springgreen4', 'black'), key='NA'),
        sg.Button('EU', button_color=('springgreen4', 'black'), key='EU'),
        sg.Button('Asia', button_color=('springgreen4', 'black'), key='Asia'),
        sg.Button('Custom', button_color=('springgreen4', 'black'), key='Custom'),
        sg.Button('Disable', button_color=('white', 'firebrick3'), key='Disable')],
        ]

window = sg.Window("Overwatch Region Swapper by PLAYG0N", layout, auto_size_buttons=False, default_button_element_size=(12,1), use_default_focus=False, finalize=True)





while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Rules':
        #Read list or create TXT
        IPList=readips()

        #NA
        add_rule("1NARegionOverwatch",IPList[0])

        #EU
        add_rule("1EURegionOverwatch",IPList[1])
        
        #Asia
        add_rule("1AsiaOverwatch",IPList[2])

        #Custom
        if not IPList[3]=="":
            add_rule("1CustomOverwatch",IPList[3])

    if event=='NA':
        window.Element('Status').Update("Current Region: NA")
        try:
            modify_rule("1NARegionOverwatch","yes")
            modify_rule("1EURegionOverwatch",0)
            modify_rule("1AsiaOverwatch",0)
            modify_rule("1CustomOverwatch",0)
        except:
            sg.popup("Create the rules first")
    if event=='EU':
        window.Element('Status').Update("Current Region: EU")
        try:
            modify_rule("1NARegionOverwatch",0)
            modify_rule("1EURegionOverwatch","yes")
            modify_rule("1AsiaOverwatch",0)
            modify_rule("1CustomOverwatch",0)
        except:
            sg.popup("Create the rules first")
    if event=='Asia':
        window.Element('Status').Update("Current Region: Asia")
        try:
            modify_rule("1NARegionOverwatch",0)
            modify_rule("1EURegionOverwatch",0)
            modify_rule("1AsiaOverwatch","yes")
            modify_rule("1CustomOverwatch",0)
        except:
            sg.popup("Create the rules first")
    if event=='Custom':
        window.Element('Status').Update("Current Region: Custom")
        try:
            modify_rule("1NARegionOverwatch",0)
            modify_rule("1EURegionOverwatch",0)
            modify_rule("1AsiaOverwatch",0)
            modify_rule("1CustomOverwatch","yes")
        except:
            sg.popup("Create the rules first")

    if event=='Disable':
        window.Element('Status').Update("Current Region: Default")
        try:
            modify_rule("1NARegionOverwatch",0)
            modify_rule("1EURegionOverwatch",0)
            modify_rule("1AsiaOverwatch",0)
            modify_rule("1CustomOverwatch",0)
        except:
            sg.popup("Create the rules first")


#Disable all on exit
modify_rule("1NARegionOverwatch",0)
modify_rule("1EURegionOverwatch",0)
modify_rule("1AsiaOverwatch",0)
modify_rule("1CustomOverwatch",0)

#fordebung=input("HALTING")

window.close()

#"5.42.168.0-5.42.175.255,5.42.184.0,5.42.187.0-5.42.187.255,5.42.188.0-5.42.188.255,5.42.189.0-5.42.189.255,5.42.191.0-5.42.191.255,157.175.0.0-157.175.255.255,15.185.0.0-15.185.255.255,15.184.0.0-15.184.255.255,5.42.190.0-5.42.190.255,5.42.186.0-5.42.186.225"