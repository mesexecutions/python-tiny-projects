#!/usr/bin/env python3

'''	

    AUTHOR: r a m e p e t l a [at] g m a i l  c o m
            R A M E S H P E T L A
            
    VERSION: 0.1

    WORKING ENVIRONMENT:

        Python Version:
        OS Version:
    
    PREREQUISITES:
    
    USAGE: 


    INPUT INSTRUCTIONS: 

        1)  This script can be executed from any location; however, 
            it will only consider the current directory as the working directory.


    KNOWN ISSUES: 
    

    OUTCOME:

'''

import os

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  PLANNING

'''
Should be able to read the input from console, what to replace with what
input: "-, "

'''

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  INPUT

string_to_search = input("Enter String or Character to Search: ")
string_to_replace = input("Enter String to Replace with: ")

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  GLOBAL VARAIBELS

current_directory = os.getcwd()

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  FUNCTIONS


print(current_directory)

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-  MAIN PROGRAM

for root, dirs, files in os.walk(current_directory):
    for file in files:
        if string_to_search in file:
            filename_split = file.split(string_to_search)
            new_filename = file.replace(string_to_search, string_to_replace)
            os.rename(file, new_filename)

                
            