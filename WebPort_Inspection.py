import os
import time
import subprocess
import sys

#Number setting for drive setup

#   A:1 B:2 C:4 ....

#To set up multiple drives, set them to an added number. -> 'drive_num'

# example
# WANT C,D Drive -> 4 + 8 = 12

#Hide the drive you want.
Drive_Hide_command = "reg.exe add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoDrives /t REG_DWORD /d 'drive_num' /f"

#LOCK the drive you want.
Drive_Lock_Command = "reg.exe add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoViewOnDrive /t REG_DWORD /d 'drive_num' /f"

#Show thedrive you want
Drive_SHOW_command = "reg.exe add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoDrives /t REG_DWORD /d 0  /f"

#UnLock thedrive you want
Drive_UnLock_Command = "reg.exe add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v NoViewOnDrive /t REG_DWORD /d 0  /f"

#Resetting OS Option
OS_Setting_Command = "rundll32.exe %Systemroot%\System32\user32.dll,UpdatePerUserSystemParameters"

def search_alive_socket(command_result):
    
    alive_PID_count=0

    #Receives the result of the command in a single line.
    command_result_lines = command_result.split('\n')
    
    print(len(command_result_lines))
    for i in range(len(command_result_lines)):
        if 'WAIT' in command_result_lines[i]:
            pass
        else:
            alive_PID_count += 1
            
    return alive_PID_count
        
def command_input(command):
    process = os.popen(command)
    results = str(process.read())
    return results

def get_netstat(options,port):
    command = "netstat " + options + " TCP | findstr " + port
    results = command_input(command)
    return results

def main():

    #Check the 80 and 443 pods used for web use.
    http_string = get_netstat('-ansp','80')
    https_string = get_netstat('-ansp','443')
    
    http_string_length = len(http_string)
    https_string_length = len(https_string)

    ALIVE_HTTP = search_alive_socket(http_string)
    ALIVE_HTTPS = search_alive_socket(https_string)

    if http_string_length == 0 | http_string.find('TCP')<0 :
        ALIVE_HTTP = 0

    if https_string_length == 0 | http_string.find('TCP')<0:
        ALIVE_HTTPS = 0
    
    Alive_PID_COUNT = ALIVE_HTTP + ALIVE_HTTPS

    #If the webport is active, hide and lock the drive.
    if Alive_PID_COUNT > 3:
        print("Web Port Alive!")
        command_input(Drive_Hide_command)
        command_input(Drive_Lock_Command)
        command_input(OS_Setting_Command)

    #If the webport isn't active, show and unlock the drive.
    else:
        print("Web Port Dead!")
        command_input(Drive_SHOW_command)
        command_input(Drive_UnLock_Command)
        command_input(OS_Setting_Command)
    
if  __name__ == '__main__':
    while 1:
        main()
        Alive_PID_COUNT = 0

        #Inspection every 3 seconds
        time.sleep(3)

        
