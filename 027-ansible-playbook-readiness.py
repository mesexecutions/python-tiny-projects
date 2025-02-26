#!/bin/python3

'''	
    Author: ramepetla (at) g m a i l . c o m
            RAMESH PETLA
    Version: 0.1
    
    This Script Tested on the Following Environment

        Python Version:
        OS Version:
    
    USAGE: 


    INPUT INSTRUCTIONS: 


    KNOWN ISSUES: 

'''

import os, sys, shutil, subprocess, zipfile

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  INPUT

name_of_target_dir = input("Enter the Ansible Directory Name: ")
want_zip = input("Zip Ansible directory? (y/n): ")
copy_to_instant_git_folder = input("Sync with Instant Git Repository? (y/n): ")


playbook_name = sys.argv[1]


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  GLOBAL VARAIBELS

current_directory = os.getcwd()
ansible_base_dir = '/tmp/' + name_of_target_dir + '/'
ansible_sub_dirs = [ 'roles', 'scripts', 'host_vars', 'vars', 'files', 'templates', 'inventory']
roles_to_copy =  []
exclude_strings = [ '#', 'name:', 'hosts:', 'gather_facts', 'become', 'vars', 'roles', '---', 'ignore_errors']
roles_dir_base_path = '/fileshare/Workspace/My_Work/Experiences/implementations/computing/devops_automation/ansible/00_roles/'
roles_dir = ['linux-os-build', 'linux-os-hardening']
roles_paths_to_copy = []
target_role_dir = ansible_base_dir + 'roles'
ansible_config_file = '/fileshare/Workspace/My_Work/Experiences/implementations/computing/devops_automation/ansible/00_configs/ansible_generic.cfg'
instant_git_repo = "/fileshare/Workspace/My_Work/Experiences/implementations/computing/Instant_git_repo/"
sensitive_strings = [ 'exclude', 'input', 'ansible.log']
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  FUNCTIONS

# Run CMD

def run_cmd(cmd):
    subprocess.run(cmd, shell=True)

# Create Directory

def create_ansible_dir(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        print("Target Directory Already Exists")

# Roles Fetching

def roles(line):
    if not any(exclude_string in line for exclude_string in exclude_strings):
        line = line.strip('- ').strip()
        return line

# Finding Parent Directory for Role

def role_parent(role):
    for dir in roles_dir:
        dir = roles_dir_base_path + dir + '/'
        roles_available = [ subdir for subdir in os.listdir(dir) if os.path.isdir(os.path.join(dir, subdir))]
        if role in roles_available:
            return dir + role



#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  MAIN PROGRAM

# To Create Sub-Dirs of Ansible Directory

for subdir in ansible_sub_dirs:
    create_ansible_dir(ansible_base_dir + subdir)

# Copy the Current Directory Contents to Target Ansible

run_cmd("cp -r * " + ansible_base_dir)


# Reading Main Playbook for Required ROLES

with open(playbook_name, encoding="utf-8") as yfile:
    lines = yfile.readlines()


# Adding Required Roles to the List After Reading from Main Playbook

for line in lines:
    if line.strip():
        line = roles(line)
        if line != None:
            roles_to_copy.append(roles(line))
    else:
        pass

# Looping Trough Roles. To Copy to Target Roles

for role in roles_to_copy:
    role_parent_dir = role_parent(role)
    run_cmd("cp -r " + role_parent_dir + " " + target_role_dir)

# Printing Total Roles

print("Total Roles Copied: ", len(roles_to_copy))

# Copying Standard Ansible CFG File

shutil.copy(ansible_config_file, ansible_base_dir + 'ansible.cfg' )


# Delete Sensitive Data

for root, directories, files in os.walk(ansible_base_dir):
    for file in files:
        if any(sensitive_string in file for sensitive_string in sensitive_strings):
            run_cmd("rm -f " + root + '/' + file)

# Zipping Final Ansible Folder

output_path = ansible_base_dir + name_of_target_dir + '.zip'
if want_zip == 'y':
    os.chdir('/tmp/')
    run_cmd("zip -rm " + name_of_target_dir + ".zip " + name_of_target_dir)
    

# Upload to GIT Repo

if copy_to_instant_git_folder == 'y' and want_zip == 'y':
    run_cmd("cp /tmp/" + name_of_target_dir + ".zip " + instant_git_repo )
    os.chdir(instant_git_repo)
    run_cmd("git add *")
    run_cmd("git commit -am '{} Added'".format(name_of_target_dir + ".zip"))
    run_cmd("git push")
    run_cmd("rm -f /tmp/" + name_of_target_dir + ".zip" )