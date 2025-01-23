#!/bin/python3

import re
import os
import shutil
from collections import OrderedDict

'''	

    AUTHOR: r a m e p e t l a [at] g m a i l  c o m
            R A M E S H P E T L A
            
    VERSION: 0.1

    WORKING ENVIRONMENT:

        Python Version: 3.12.3
        OS Version: Windows 11
    
    PREREQUISITES:
    
    USAGE: 


    INPUT INSTRUCTIONS: 


    KNOWN ISSUES: 
    

    OUTCOME:

'''

# \\ -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  PLANNING

'''
Step by Step tasks to be executed by this Program
'''

# \\ -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  INPUT

'''
Variables that can be changed
'''
# Blank PDF Document
blank_pdf = 'C:\\Storage\\my_drive\\Redhat Official Training\\Blank.pdf'


# \\ -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  GLOBAL VARAIBELS

# Stores Tables of Contents in the form of KEY: ch0202title VALUE: [Chapter 2 Implementing an Ansible Playbook]
tocdict = {}    
# Stores Keys containing String 'pr'  from todict
tocdict_key_prlist = []
# Stores Keys containing String 'ch'  from todict
tocdict_key_chlist_temp = []
src_tgt_filepaths = []
current_directory = os.getcwd()


# \\ -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  FUNCTIONS

         
# Renaming Files

def filetorename(sourcefile,targetfile):

    targetfile = os.path.join(current_directory,targetfile + '.pdf')
    os.rename(os.path.join(current_directory,sourcefile), targetfile)
    os.utime(targetfile, None)    # Set the current timestamp as the modified time for sorting files in the explorer.

# Some section/chapter titles have no source files, so a blank PDF is copied with the target file name.


def filestocopy(targetfile):

    targetfile = os.path.join(current_directory,targetfile + '.pdf')    
    shutil.copy(blank_pdf, targetfile)
    os.utime(targetfile, None)

    '''
    The following function processes each title to generate formatted codes based on predefined 
    patterns (such as "Preface A," "Section A.3," "Chapter 3," and  "Section 3.1") and returns the 
    results in a dictionary key format, excluding any lines that contain "Quiz:".
    '''

def fnamegeneration(title, chcode):

    # To process titles that look like "Preface A: Introduction", with the final output formatted as "PrAtitle"

    if 'Preface A' == title[0]:
        chcode = title[0][0:2]
        chcode_dictkey = chcode + title[0][-1] + 'title'  

    # Process titles formatted like "Section A.3: Appendix" to produce the final output in the format "Pr01S03"

    elif 'Section A.' in title[0]:
        chcode_dictkey = chcode + '01' + title[0][0:1] + str(re.split(r'[ .]', title[0])[2]).zfill(2)

 
    # # Process titles formatted like "\ Chapter 3: How Brain Works" to produce the final output in the format "Ch03title"

    # elif 'Chapter' in title[0]:
    #     chcode = title[0][0:2] + title[0][-1].zfill(2)
    #     chcode_dictkey = chcode + 'atitle'

    # Process titles formatted like "Chapter 3: How Brain Works" to produce the final output in the format "Ch03title"

    elif 'Chapter' in title[0]:
        
        title_list = title[0].split()
        chcode = title_list[1]
        if len(chcode) >= 2:
            chcode = title_list[1]
        else:
            chcode = title_list[1].zfill(2)

        chcode = 'ch' + chcode
        chcode_dictkey = chcode + 'atitle'

    # Process titles formatted like "Section 3.1: Managing Daily Routines" to produce the final output in the format "Ch03S01"

    elif 'Section' in title[0]:
        chcode_dictkey = chcode + title[0][0:1] + str(re.split(r'[ .]', title[0])[2]).zfill(2)

    else:
        return None
        
    
    return chcode, chcode_dictkey
    

# \\ Read the input file (toc.txt); each line will be stored in a dictionary \\

def rhtnamingfiles():

    chcode_init = ''

    with open('toc.txt', 'r') as tocfile:
        tocfile_lines = tocfile.readlines()
        current_chcode = ''
        
        for line in tocfile_lines:

            if 'Quiz' not in line:

                line = line.strip()
                chcode_raw = fnamegeneration(line.split(':'), chcode_init)
                print(chcode_raw)
                chcode_init = chcode_raw[0]
                tocdict[chcode_raw[1].lower()] = [line.replace(':', '')]

       

# \\ Reads the contents of the current directory containing files with the format: Filename > DSMATH102 - ch06s11.pdf \\

    for root, dirs, files in os.walk(current_directory):

        files = [file for file in files if 'toc.txt' not in file]

        for file in files:

            filename_list = re.split(r'[.-]', file)   

            target_filename = ""
            chcode_key = "" 

            if 'pr' in filename_list[1] and 's' not in filename_list[1]:
                chcode_key = filename_list[1] + 's01'
                target_filename = tocdict[chcode_key.strip()]

            elif 'pr' in filename_list[1]:
                chcode_key = filename_list[1].strip()
                target_filename = tocdict[chcode_key]

            elif 'sol' in filename_list[1]:
                chcode_key = filename_list[1].split()[0]
                target_filename = tocdict[chcode_key][0] + ' Solution'

            elif 'ch' in filename_list[1] and 's' not in filename_list[1]:
                chcode_key = filename_list[1].strip() + 's01'
                target_filename = tocdict[chcode_key]

            elif 'ch' in filename_list[1]:
                chcode_key = filename_list[1].strip()
                target_filename = tocdict[chcode_key]
            
            source_filename = file

            if 'sol' in source_filename:
                chcode_key = chcode_key.strip() + 'sol'
                tocdict[chcode_key] = [target_filename, source_filename]
            else:
                tocdict[chcode_key.strip()].append(source_filename)

    ''' 
    Adding keys from tocdict to `tocdict_key_prlist` and `tocdict_key_chlist` for sorting purposes. 
    Strings containing 'pr' should appear at the beginning of the list, as they are already in sorted order, 
    so they are stored directly in `tocdict_key_prlist`. However, strings containing 'ch' are unsorted, 
    so they are added to `tocdict_key_chlist` to be sorted later. 
    '''

# \\ Combining lists containing strings with 'pr' and 'ch'
    
    global all_sorted_keys

    for key, values in tocdict.items():
        if 'pr' in key:
            tocdict_key_prlist.append(key)
        else: 
            tocdict_key_chlist_temp.append(key)
    
    all_sorted_keys = tocdict_key_prlist + sorted(tocdict_key_chlist_temp)

    for dict_key in all_sorted_keys:

        if 'title' in dict_key:
            filestocopy(tocdict[dict_key][0])

        else:
            filetorename(tocdict[dict_key][1], tocdict[dict_key][0])  


# \\ -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  MAIN PROGRAM

rhtnamingfiles()
