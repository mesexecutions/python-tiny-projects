#!/usr/bin/env python3

r'''
Author: R a m e s h P e t l a <r a m e p e t l a [ a t ] g m a i l . c o m >
Version: 0.1

Environment:
    - Python Version: 3.x
    - OS            : Ubuntu/Windows/macOS

Description:
    - [Brief summary of what this script does.]

Usage:
    $ python3 script_name.py [optional arguments]

Arguments:
    - [--input]   : Input file or directory (optional)
    - [--debug]   : Enable debug mode (optional)

Inputs:
    - [e.g., reads from config.json or takes CLI input]

Outputs:
    - [e.g., prints logs, generates output.txt, writes to DB]

Dependencies:
    - [e.g., requests, pandas, custom_module]
    - Install with: pip install -r requirements.txt

Known Issues:
    - [List any limitations, TODOs, or bugs]

Outcome:
    - [Expected output or result, e.g., summary report generated]

Changelog:
    - v0.1: Initial version - basic structure added.

Development Instructions:
    - Resources Directory: C:\links\resources\bluecoins_analysis
                           /links/resources\bluecoins_analysis

To Do:
    - Check with GenAI for this Program Improvements/Optimization
'''

import os
import pandas as pd
from datetime import datetime
from collections import defaultdict
import re

# >>>>>>>>>>>>>>>>>>>>>>>   INPUT

working_directory = os.getcwd()
master_transaction_file = 'bluecoins_transactions_list.csv'


# List to Capture Transaction Unique Key in the Format of BANKACC-DDMMYYYY-AMOUNT e.g DBS-30052025-11.6
bluecoins_list = []
bankaccount_list = []

# List to Capture Full Transaction Details Linked to Specific Unique Key
bankaccount_dict = defaultdict(list)

# List of Files Available in Current Directory 
files_to_process = []

# Keywords To Validate To Ignore Any Rows
# ignore_keywords = [ 'GIANT', 'FairPrice', 'SHENGSIONG' ]
ignore_keywords = []

# Master Date Sub Transactions Summation

master_subtransactions_dict = defaultdict(list)

# Final List

bankaccount_final_list = []

# >>>>>>>>>>>>>>>>>>>>>>>   FUNCTIONS

def read_csv_with_pandas(rec_filename):
    df = pd.read_csv(rec_filename, on_bad_lines='skip', skipinitialspace=True)
    df.columns = df.columns.str.strip()  # Fix for space issues
    df.dropna(how='all', inplace=True)
    df.drop_duplicates(inplace=True)
    return df


def sanitize_string(rec_string):
    # sanitized_string = re.sub(r'[&_\-\(\)\/\}\]\{\[\@\'\:\,\;\"\#\%\$ ]', '', rec_string)
    sanitized_string = re.sub(r'[^a-zA-Z0-9\.]', '', rec_string)
    return sanitized_string


def find_real_transaction_date(original_date, client_reference):
    """
    If client reference contains a date like 25MAR or 31DEC,
    return adjusted date. Otherwise return original date.
    Returns a formatted string: dd/mm/yyyy
    """
    if not isinstance(client_reference, str):
        return original_date.strftime('%d/%m/%Y')

    match = re.search(r'(\d{1,2})(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)', client_reference.upper())
    if match:
        day = int(match.group(1))
        month_str = match.group(2)
        try:
            month_num = datetime.strptime(month_str, "%b").month
            # Adjust year if needed
            if month_str == 'DEC' and original_date.month == 1:
                year = original_date.year - 1
            else:
                year = original_date.year
            adjusted_date = datetime(year, month_num, day)
            return adjusted_date.strftime('%d/%m/%Y')
        except ValueError:
            return original_date.strftime('%d/%m/%Y')
    return original_date.strftime('%m/%d/%Y')


def find_transaction_type(rec_debit, rec_credit):
    if rec_debit not in ['', ' ', 'nan', None] and not pd.isna(rec_debit):
        return rec_debit, "Expense"
    else:
        return rec_credit, "Income"


def dbs_csv(rec_file_data):
    for index, row in rec_file_data.iterrows():
        row_text = ' '.join(map(str, row.values)).lower()
        if any(keyword.lower() in row_text for keyword in ignore_keywords):  # Ignores rows if keywords in ignore_keywords are found.
            continue  # Skip rows with ignore keywords

        date_raw = str(row['Transaction Date']).split()[0]
        date_obj = datetime.strptime(date_raw, '%d-%b-%y')
        formatted_date = find_real_transaction_date(date_obj, row.get('Client Reference', ''))

        amount, transaction_type = find_transaction_type(str(row['Debit Amount']), str(row['Credit Amount']))
        unique_list_item = 'DBS-' + ''.join([formatted_date.split('/')[2], formatted_date.split('/')[0], formatted_date.split('/')[1]]) + '-' + amount
        bankaccount_list.append(unique_list_item)

        stmt_tag = f"BANK-STMT-DBS-{date_obj.strftime('%b').upper()}-{date_obj.strftime('%Y')} "
        notes = stmt_tag + "Bank Transaction: " + str(row['Transaction Date']) + " Actual Transaction: " + \
              formatted_date + " " + "MetaData: " + row_text
    

        label = 'AddedByAutomationNonVerified MayBeDuplicateTransaction AddedByAutomationVerified SGDBS InSGD SGSGDExpense NonVerified AuditDBS AddedByAutomationOn01JULY2025 DBSAddedByImportingCSV AddedByAutomation' 

        value = [ transaction_type, formatted_date, "Uncategorized Transaction", amount, "Excluded", "Uncategorized", "A_SINGAPORE", "DBS (SGD)", notes, label, "Cleared", "" ]

        if unique_list_item not in bankaccount_dict:
            bankaccount_dict[unique_list_item] = [value]
        else:
            bankaccount_dict[unique_list_item].append(value)


# >>>>>>>>>>>>>>>>>>>>>>>   MAIN PROGRAM: Processing Files Data

# Read your data from master_transaction_file
master_data = read_csv_with_pandas(master_transaction_file)

# Process Data from master_transaction_file

for index, row in master_data.iterrows():
    date_list = str(row['Date']).split()
    date_str = sanitize_string(date_list[0])
    notes = str(row['Notes']).replace('\n', ' ').strip()
    sanitized_notes = sanitize_string(notes)
    unique_list_item = sanitize_string(str(row['Account'])) + '-' + date_str + '-' 
    match = match = re.search(r'\[\{(.*?)\}\]', notes)
    
    if match:
        #unique_subtransaction_key = sanitize_string(str(row['Date'] + row['Type'][0:4] + row['Title'][0:4] + sanitize_string(row['Account']) )) #+ sanitized_notes[-10:]))
        unique_subtransaction_key = unique_list_item + '_' + sanitize_string(date_list[1]) + row['Type'][0:4] + row['Title'][0:4]
        if unique_subtransaction_key not in master_subtransactions_dict:
            master_subtransactions_dict[unique_subtransaction_key] = [row['Amount']]
        else:
            master_subtransactions_dict[unique_subtransaction_key].append(row['Amount'])
    else:
        bluecoins_list.append(unique_list_item + sanitize_string(str(row['Amount'])))  # Store in Format of  Account-Date-Amount e.g: DBS-20240727-5.4, DBS-20240730-2.0, DBS-20240408-1.88


# Process Data from master_subtransactions_dict

for transaction_key, amounts in master_subtransactions_dict.items():
    total_amount = sum(amounts)
    total_amount = round(total_amount, 2)
    bluecoins_list.append(transaction_key.split('_')[0] + sanitize_string(str(total_amount)))


# Processes files in the working_directory except MASTER TRANSACTION FILE.
# Calls relevant function based on file extension and bank account name.

for root, dirs, files in os.walk(working_directory):
    for file in files:
        if 'bluecoins_' not in file and 'Exclude' not in file and file.endswith('.csv'):
            file_data = read_csv_with_pandas(file)
            if 'dbs' in file.lower():
                dbs_csv(file_data)

# >>>>>>>>>>>>>>>>>>>>>>>   MAIN PROGRAM: Processing Data in LISTS & DICTIONARIES

# Sorting Lists
bankaccount_list = sorted(bankaccount_list)
bluecoins_list = sorted(bluecoins_list)


# Preparing bankaccount_final_list to Write to CSV. The Existing Dict bankaccount_dict having Morethan 1 Value for Some Keys. 

filtered_bankaccount_list = set(bankaccount_list)

for transaction_key in filtered_bankaccount_list:
    if transaction_key not in bluecoins_list:
        transaction_values = bankaccount_dict[transaction_key]
        for transaction_value in transaction_values:
            bankaccount_final_list.append(transaction_value)


# >>>>>>>>>>>>>>>>>>>>   WRITE REMAINING BANK TRANSACTIONS TO CSV

print("\nWriting Transactions to CSV in BlueCoins Format\n")

header = [ "(1)Type", "(2)Date", "(3)Item or Payee", "(4)Amount", "(5)Parent Category",
    "(6)Category", "(7)Account Type", "(8)Account", "(9)Notes",
    "(10) Label", "(11) Status", "(12) Split" ]

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'output_{timestamp}.csv'

df = pd.DataFrame(bankaccount_final_list, columns=header)
df.to_csv(filename, index=False)
