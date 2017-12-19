#! /usr/bin/python2.7

"""
Endurance Test for Seamless
"""

import sys
import os
import time
import subprocess


port = ''



####################################################
#FIRMWARE / TOOL BOX MENU
####################################################  


def firmware():
    
    print('Performing... reboot -f')
    os.system('echo "a" > /dev/'+port+'')
    os.system('echo "reboot -f" > /dev/'+port+'')
    counter(11)
    find = False
    i = 0
    while find == False:
        os.system('irsend SEND_ONCE newtv KEY_8')
        time.sleep(0.5)
        os.system('irsend SEND_ONCE newtv KEY_2')
        time.sleep(0.5)
        find = cmd_output('ToolBox')
        i=+1
        if i == 15:
            find = True
            uhd()
            

    print('\nPerforming... key 82  -> enter ToolBox')
    sw_ra_(com)

def sw_ra_(com):
    print \
    ("""
    Which component to change?
    1 - RA
    2 - FW
    3 - FW_FUT
    """)
    choice = input("Type nr: ")
    if choice == 1:
        component = 'ra'
        print('Insert ra code like i.e- 40 33 12')
        a = raw_input('First: ')
        b = raw_input('Second: ')
        c = raw_input('Third: ')
        changer(component,a,b,c)
    elif choice == 2:
        component = 'fw'
        print('Insert fw code like i.e- 4 07 36')
        a = raw_input('First: ')
        b = raw_input('Second: ')
        c = raw_input('Third: ')
        changer(component,a,b,c)
    elif choice == 3:
        component = 'fw_fut'
        print('Insert fw_fut code like i.e- 4 07 36')
        a = raw_input('First: ')
        b = raw_input('Second: ')
        c = raw_input('Third: ')
        changer(component,a,b,c)
    else:
        print('Wrong choice')


def changer(comp,a,b,c):


    os.system('echo "defaults" > /dev/'+port+'')
    os.system('echo "\r"  > /dev/'+port+'')
    time.sleep(1)
    os.system('echo "boot_mode download" > /dev/'+port+'')
    os.system('echo "\r"  > /dev/'+port+'')
    time.sleep(1)
    if comp == 'ra':
        os.system('echo "corrupt ra" > /dev/'+port+'')
        os.system('echo "\r"  > /dev/'+port+'')
        time.sleep(1) 
        os.system('echo "dl_ra_url https://195.116.227.11/FW_02_00_00/AR_'+a+'_'+b+'_'+c+'/htmlapp-'+a+b+c+'.hs3" > /dev/'+port+'')
        os.system('echo "\r"  > /dev/'+port+'')
        time.sleep(1)
    elif comp == 'fw':
        os.system('echo "corrupt firmware" > /dev/'+port+'')
        os.system('echo "\r"  > /dev/'+port+'')
        time.sleep(1)
        os.system('echo "dl_firmware_url https://195.116.227.11/FW_02_00_00/SAGEM_194_test_0'+a+'_'+b+'_'+c+'_'+a+b+c+'.as3" > /dev/'+port+'')
        os.system('echo "\r"  > /dev/'+port+'')
        time.sleep(1)
    elif comp == 'fw_fut':
        os.system('echo "corrupt firmware" > /dev/'+port+'')
        os.system('echo "\r"  > /dev/'+port+'')
        time.sleep(1)
        os.system('echo "dl_firmware_url https://195.116.227.11/FW_02_00_00/SAGEM_194_test_0'+a+'_'+b+'_'+c+'_'+a+b+c+'.fut.as3" > /dev/'+port+'')
        os.system('echo "\r"  > /dev/'+port+'')
        time.sleep(1)
    os.system('echo "quit" > /dev/'+port+'')
    os.system('echo "\r"  > /dev/'+port+'')



####################################################
#Use Case
####################################################

def rm_flash():
    print('rm /flash/.clean')
    os.system('echo "a" > /dev/'+port+'')
    time.sleep(1)
    os.system('echo "rm /flash/.clean" > /dev/'+port+'')
    time.sleep(1)
    result = cmd_output('clean')
    if result == True:
        print('\tPass')
        return True
    else:
        print('\tFail')
        return False

def reboot():
    
    print('Reboot')
    os.system('echo "a" > /dev/'+port+'')
    os.system('echo "reboot -f" > /dev/'+port+'')
    time.sleep(120)
    result = waitForOutput('SAH FirstInstall')
    if result == True:
        print('\tPass')
    return True


def replace_server():

    sed = "'s/rightv.ppd.newtv.tp.pl/rightv.newtv.tp.pl/g'"
    print('Replace server Right_TV')
    time.sleep(5)
    os.system('echo "a" > /dev/'+port+'')
    time.sleep(3)
    os.system('echo "cp -f /usr/share/browser/html/Applications/FirstInstall_FT/setup/servers.js /tmp && sed -i '+sed+' /tmp/servers.js && mount -o bind /tmp/servers.js /usr/share/browser/html/Applications/FirstInstall_FT/setup/servers.js" > /dev/'+port+'')

    time.sleep(2)
    result = cmd_output(sed)
    if result == True:
        print('\tPass')
        return True
    else:
        print('\tFail')
        return False

def install():

    print('Install from SAH menu')
    for i in range(0,2):
        os.system('irsend SEND_ONCE newtv KEY_LEFT')
        time.sleep(2)
    os.system('irsend SEND_ONCE newtv KEY_OK')
    time.sleep(10)
    os.system('irsend SEND_ONCE newtv KEY_OK')
    time.sleep(60)
    
    result = waitForOutput('[popup_02]')
    count = 0
    to_check =['[popup_02]','FIRST INSTALL FINISHED', 'UPGRADE_READY','KARMA DOWNLOADING']
    for element in to_check:
        result = cmd_output(element)
        if result == True:
            print('\tPass: '+element+' in')
            time.sleep(1)
            count+=1
        else:
            print('\tFail: '+element+' not in')
            time.sleep(1)
    if count == len(to_check):
        return True
    else:
        faile_result()
        return False


####################################################
#TEST
####################################################

def waitForOutput(to_find):

    count = 0
    check = True
    while check:
        cmd = ('tail -n50 /home/pi/Desktop/output.txt | grep -i "'+to_find+'"')
        output = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
        result = output.stdout.read()

        if to_find in result:
            print('OK')
            check = False
            return True
        else:
            time.sleep(10)
            count+=1
            if count == 60:
                return False
                break

            
    
def cmd_output(to_find):
    
    cmd = ('tail -n100 /home/pi/Desktop/output.txt | grep -i "'+to_find+'"')
    output = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
    result = output.stdout.read()
    if to_find in result:
        return True
    else:
        return False

def faile_result():
    msg = 'Fail_'+time.strftime("%Y_%m_%d_%H_%M_%S")+'.txt'
    cmd = ("tail -n1000 /home/pi/Desktop/output.txt")
    output = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
    result = output.stdout.read()
    with open(msg,'w')as file:
        file.writelines(result)
    print ('\nNew file created '+msg)
     
    
####################################################
#Endurance
####################################################

def endurance():
    print \
    ("""
    ************************************************
    ENDURANCE test for SEAMLESS
    ************************************************

    Test case:
    1. rm /flash
    2. reboot
    3. replace server info
    4. install from SAH menu
    5. Pass or Fail test

    repeat in loop 10000
    
    """)
    repeat=0
    print('Prepare STB - going to reboot')
    ok = reboot()
    if ok == True:
        print \
        ("""
        ************************************************
        START test 
        ************************************************
        """)
        for i in range(0,10000):
            fin = {}
            run = 'Run:'+str(i)
            cmd1 = rm_flash()
            cmd2 = reboot()
            cmd3 = replace_server()
            cmd4 = install()
            if cmd1 and cmd2 and cmd3 and cmd4==True:
                overall = 'PASS'
            else:
                overall = 'FAILD'
            fin = {'rm_flash':cmd1,
                   'reboot':cmd2,
                   'replace_server_info':cmd3,
                   'install_proc':cmd4}
            to_write = time.strftime("%Y_%m_%d_%H_%M_%S")+'_'+run+'_'+str(fin)+'| result: '+overall+'\n'
            with open('/home/pi/Desktop/Seamless/results.txt','a+')as file:
                file.writelines(to_write)
            print('\nRun'+str(i)+' DONE\nTest has been '+overall+'\n\n')
            time.sleep(5)
        print \
        ("""
        ************************************************
        END test 
        ************************************************
        """)
    else:
        print('Trying again run ENDURANCE')
        endurance()
        repeat+=1
        if repeat == 5:
            print('After 5 tries cannot launch ENDURANCE - check your connection')


####################################################
#Main
####################################################

    
def COM_port():
    print \
    ("""
    Make sure that STB is running and:
    -there is ssh conection between PC-RasPI
    -serial port enabled on RasPI (putty running)

    Make sure that output of COM logs is set to: /home/pi/Desktop/output.txt
    You can change it in function -> def cmd_output(to_find)
    """)
    port_num = raw_input("Insert COM port number: ")
    com = 'ttyUSB'+port_num
    print('COM set --> '+com)
    return com

def main():
    print \
    ("""
    Choose action:
    1. FW/RA change from ToolBOX menu (only UHD implemented)
    2. Run SEAMLESS endurance
    3. Quit
    """)
    choice = input("Your choice: ")
    if choice == 1:
        firmware()
    elif choice == 2:
        endurance()
    else:
        print('Wrong choice')


####################################################    

port = COM_port()
main()

