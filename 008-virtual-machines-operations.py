#!/usr/bin/env python3.11

#!/bin/python3

'''	

    AUTHOR: ramepetla (at) g m a i l . c o m
            RAMESH PETLA
            
    VERSION: 0.1

    WORKING ENVIRONMENT:

        Python Version:
        OS Version:
    
    PREREQUISITES:
    
    USAGE: 


    INPUT INSTRUCTIONS: 


    KNOWN ISSUES: 
    

    OUTCOME:

'''

import os, subprocess
from socket import timeout
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from email.policy import default
from threading import TIMEOUT_MAX
from time import sleep

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  PLANNING


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  INPUT


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  GLOBAL VARAIBELS

vm_list = []
template_list = []
vm_and_path_pair = {}

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  FUNCTIONS

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ VM LIST


def vmlist():
    print("\n-+-+-+-+-+-+-+-+-+ VMs LIST:\n")
    for vm in vm_list:
        print(vm)
    print('\n')

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ TMEPLATE LIST


def templatelist():
    print("\n-+-+-+-+-+-+-+-+-+ VM TEMPLATES:\n")
    for vm_template in sorted(template_list):
        print(vm_template)
    print('\n')


#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ VMs RUNNING

def running_vms():
    vm_running_list_dic = {}
    vms_running_list = subprocess.run(['vmrun list > /tmp/vmrun_list'], shell=True)
    with open('/tmp/vmrun_list') as file:
        i = 1
        for line in file.readlines():
            line = line.splitlines()
            if ".vmx" in line[0]:
                vm_name = line[0].split("/")
                vm_name = vm_name[-1].split(".")
                vm_running_list_dic[i] = vm_name[0]
                i += 1
    return vm_running_list_dic
    

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ VM SELECTION

def vm_selection():
    vm_list_dict = {}
    i = 1
    for vm in vm_list:
        vm_list_dict[i] = vm
        i += 1
    return vm_list_dict


#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ START VMs

def vm_power_on():
    returned_vm_list_dic = vm_selection()
    print('\n-+-+-+-+-+-+-+-+-+ AVAILABLE VMs\n')
    for key, value in returned_vm_list_dic.items():
        print(key, value)
    
    start_vms = input("\nSelect VMs to Power On: ")

    for vm_index in start_vms.split(" "):
        for key, value in returned_vm_list_dic.items():
            if key == int(vm_index):
                for vm_name, path in vm_and_path_pair.items():
                    if value in vm_name:
                        cmd = 'vmrun -T ws start {} nogui'.format('"' + path +'"')
                        subprocess.Popen([cmd], shell=True)
                        sleep(5)

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ STOP VMs 

def vm_power_off():
    ret_vm_running_list_dic = running_vms()
    print('\n-+-+-+-+-+-+-+-+-+- CURRENTLY RUNNING VMs\n')
    for key, value in ret_vm_running_list_dic.items():
        print(key, value)

    stop_vms = input("\nSelect VMs to Power Off: ")

    for vm_index in stop_vms.split(" "):
        for key, value in ret_vm_running_list_dic.items():
            if key == int(vm_index):
                for vm_name, path in vm_and_path_pair.items():
                    if value in vm_name:
                        cmd = 'vmrun -T ws stop {} nogui'.format('"' + path +  '"')
                        subprocess.Popen([cmd], shell=True)
                        sleep(5)

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ SNAPSHOT REVERT 

def vm_sanpshot_revert():
    returned_vm_list_dic = vm_selection()
    print('\n-+-+-+-+-+-+-+-+-+ AVAILABLE VMs\n')
    for key, value in returned_vm_list_dic.items():
        print(key, value)

    vm_to_revert_to_snapshot = input("\nSelect VM to Revert to Snapshot: ")

    for key, value in returned_vm_list_dic.items():
        if key == int(vm_to_revert_to_snapshot):
            for vm_name, path in vm_and_path_pair.items():
                if value in vm_name:
                    cmd = 'vmrun listSnapshots {}'.format('"' + path + '"')
                    subprocess.run(['{} > /tmp/vm_snapshots'.format(cmd)], shell=True)

                    with open('/tmp/vm_snapshots') as file:
                        vm_snapshot_dict = {}
                        i = 1
                        for line in file.readlines():
                            if 'snapshots' not in line:
                                line = line.splitlines()
                                vm_snapshot_dict[i] = line[0]
                                i += 1
                        for key, value in vm_snapshot_dict.items():
                            print(key, value)
                        snapshot_to_revert = input("\nSelect Snapshot to Revert: ")

                        for key, snapshot in vm_snapshot_dict.items():
                            if key == int(snapshot_to_revert):
                                cmd = 'vmrun -T ws revertToSnapshot {} {}'.format('"' + path + '"', snapshot)
                                subprocess.run([cmd], shell=True)


#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ SWITCHER 

switcher = {
    1: vmlist,
    2: templatelist,
    3: vm_power_on,
    4: vm_power_off,
    5: vm_sanpshot_revert,
    6: running_vms
}


def selection(option):
    return switcher.get(option, default) ()


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  MAIN PROGRAM


for root, dirs, files in os.walk("/storage"):
    for file in files:
        if file.endswith(".vmx"):
            file_full_path = os.path.join(root,file)
            vm_and_path_pair[file] = file_full_path
            vm_name = file.split(".")
            if "templates" not in file_full_path:
                vm_list.append(str(vm_name[0]))
            else:
                template_list.append(str(vm_name[0]))

vm_list = sorted(vm_list, key=str.lower)


print("\n-+-+-+-+-+-+-+-+-+-  MENU\n\n1: VM List\n2: Template List\n3: Start the VM\n4: Stop the VM\n5: Revert Snapshot\n6: Running VMs (GRAYED OUT)")

user_input = input("\nOption: ")

selection(int(user_input))
