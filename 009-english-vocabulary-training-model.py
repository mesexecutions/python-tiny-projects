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

        1)  


    KNOWN ISSUES: 
    

    OUTCOME:

'''

from os import listdir, stat, utime
from sqlite3.dbapi2 import Cursor
import PyPDF2, sqlite3, os


#-////////////////////////////////////////////// FUNCTIONS /////////////////////////////////////////////

#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ DB CREATION

def db_creation():
    
    with sqlite3.connect('C:\Orktion_Data\My Backup\Database\SQLite\english_vocabulary.db') as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS book_information(book_name text NOT NULL,
                                                                      total_extracted_words INT,
                                                                      advanced_words INT);""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS words(word_name text NOT NULL,
                                                           word_count INT,
                                                           occured_in INT);""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS common_words(word_name text NOT NULL);""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS advanced_words(book_name text NOT NULL,
                                                                    adv_word_name text NOT NULL);""")
    
    db.close()

#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ Reading From DATABASE

def reading_words_information():

    common_words_from_db = []
    word_count_from_db = {}

    with sqlite3.connect('C:\Orktion_Data\My Backup\Database\SQLite\english_vocabulary.db') as db:
        cursor = db.cursor()

        cursor.execute("""SELECT word_name, word_count FROM words""")
        records = cursor.fetchall()
        for word, count in records:
            word_count_from_db[word] = count
        
        cursor.execute("""SELECT word_name FROM common_words""")
        records = cursor.fetchall()
        for word in records:
            common_words_from_db.append(word[0])
    
    db.close()

    return common_words_from_db, word_count_from_db


def book_information():

    book_information_from_db = []

    with sqlite3.connect('C:\Orktion_Data\My Backup\Database\SQLite\english_vocabulary.db') as db:
        cursor = db.cursor()
           
        cursor.execute("""SELECT book_name FROM book_information""")
        records = cursor.fetchall()
        for book in records:
            book_information_from_db.append(book[0])
    db.close()

    return book_information_from_db


#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ Insert Into Database

def insert_into_table_words(word_count_dict):

    from_database = reading_words_information()
    common_words_from_db = from_database[0]
    word_count_from_db =  from_database[1]

    with sqlite3.connect('C:\Orktion_Data\My Backup\Database\SQLite\english_vocabulary.db') as db:
        cursor = db.cursor()
        advanced_words = []
        max_word_occurence = 2
        for key, value in word_count_dict.items():
            if key in word_count_from_db.keys():
                existing_count = word_count_from_db[key]
                new_count = existing_count + value
                if value > max_word_occurence:
                    cursor.execute("""UPDATE words SET word_count = ? WHERE word_name = ?""", (new_count, key))
                else:
                    cursor.execute("""UPDATE words SET word_count = ? WHERE word_name = ?""", (new_count, key))
                    if key not in common_words_from_db:
                        advanced_words.append(key)
            else:
                if value > max_word_occurence:
                    cursor.execute("INSERT INTO words VALUES(?, ?, ?);", (key, value, 1))
                    if key not in common_words_from_db:
                        cursor.execute("INSERT INTO common_words VALUES(?);", (key,))
                elif value <= max_word_occurence:
                    if key not in common_words_from_db:
                        advanced_words.append(key)
                    cursor.execute("INSERT INTO words VALUES(?, ?, ?);", (key, value, 1))
                else:
                    pass
        db.co mmit()

    return advanced_words

#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ Trash Can: Discard Words having Chracters, Numbers, Symbols

def trash_can(raw_list):
    processed_list = []
    for word in raw_list:
        only_letters = word.isalpha()
        if only_letters == False:
            pass
        else:
            processed_list.append(word.lower())
    processed_list = list(set(processed_list))
    processed_list.sort()

    return processed_list

#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ WORD Count

def word_count(unique_words, total_words_in_doc):
    word_count_dict = {}
    for word in unique_words:
        word_occurence = total_words_in_doc.count(word)
        word_count_dict[word] = word_occurence
    
    advanced_words_to_get = insert_into_table_words(word_count_dict)
    return advanced_words_to_get

#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ Text Extraction

def text_extraction(doc):

    # TOTAL EXTRACTED WORDS
    total_extracted_words = []              

    # Creating a PDF File Object
    pdfFileObj = open(doc, 'rb')

    # Creating a PDF Reader Object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Getting Total Pages in Document
    total_pages = pdfReader.numPages

    # Looping Through All Pages
    for page in range(0, total_pages):
        
        # Creating a Page Object
        pageObj = pdfReader.getPage(page)

        # TEXT Extraction
        extracted_text = pageObj.extractText()
        extracted_words = extracted_text.split()

        # Adding Extracted WORDS To TOTAL EXTRACTED WORDS
        for word in extracted_words:
            total_extracted_words.append(word.lower())

    # Unique Words
    unique_words_set = set(total_extracted_words)
    unique_words_list = trash_can(unique_words_set)

    # WORD Count
    advanced_words_recieved = word_count(unique_words_list, total_extracted_words)
    return len(total_extracted_words), len(advanced_words_recieved), advanced_words_recieved


#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ COMMON WORDS TO DATABASE

def common_words_to_db(pdf_doc):
    
    total_common_words_extracted = []

    cwpdfFileObj = open(pdf_doc, 'rb')
    cwpdfReader = PyPDF2.PdfFileReader(cwpdfFileObj)    
    cw_total_pages = cwpdfReader.numPages

    for cw_page in range(0, cw_total_pages):

        cwpageObj = cwpdfReader.getPage(cw_page)

        cw_extracted_text = cwpageObj.extractText()
        cw_extracted_words = cw_extracted_text.split()

        for cw_word in cw_extracted_words:
            total_common_words_extracted.append(cw_word)

    cw_unique_words_set = set(total_common_words_extracted)
    cw_unique_words_list = trash_can(cw_unique_words_set)

    common_words_exist_in_db = reading_words_information()[0]

    with sqlite3.connect('C:\Orktion_Data\My Backup\Database\SQLite\english_vocabulary.db') as db:
        cursor = db.cursor()

        for common_word in cw_unique_words_list:
            common_word_lower = common_word.lower()
            if common_word_lower not in common_words_exist_in_db:
                #print(unique_word)
                cursor.execute("INSERT INTO common_words VALUES(?);", (common_word_lower,))
        
        db.commit()
        db.close

#-/////////////////////////////////////////// ACTUAL PROGRAM ///////////////////////////////////////////

#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ Check if Database Exists

db_file = 'C:\Orktion_Data\My Backup\Database\SQLite\english_vocabulary.db'

if os.path.exists(db_file):
    print("DB Already Created")
else:
    db_creation()

#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ Processing Documents

# Adding Filenames in the Current Directory to LIST

documents_to_scan = os.listdir()

for document in documents_to_scan:

    book_information_from_db = book_information()

    with sqlite3.connect('C:\Orktion_Data\My Backup\Database\SQLite\english_vocabulary.db') as db:
        cursor = db.cursor()

        if 'common_words' in document:
            common_words_to_db(document)

        elif document not in book_information_from_db:
            summary_per_doc = text_extraction(document)
            print(document, summary_per_doc[0], summary_per_doc[1], summary_per_doc[2])
            cursor.execute("INSERT INTO book_information VALUES(?,?,?);", (document, summary_per_doc[0], summary_per_doc[1]))
            for adv_word in summary_per_doc[2]:
                cursor.execute("INSERT INTO advanced_words VALUES(?,?);", (document, adv_word))
        else:
            print("Book {} Already Extracted".format(document))

    db.commit()
    db.close()    


#-\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ Dispose Advanced Words from Common_Words

''' 
common_words may contain some advanced vocabulary which needs to be disposed from the common_words.

seperate database for common_words, and word_count
'''

