#!/usr/bin/env python3

import cgi
import cgitb
from string import Template
import pymysql
import json
import sys
from datetime import datetime
import pandas as pd
from io import BytesIO
import numpy as np

# Enable CGI traceback for debugging
cgitb.enable()

# Print the HTTP header
print("Content-Type: application/json\n")

# Parse form data
form = cgi.FieldStorage()

try:
    connection = pymysql.connect(
        host='bioed.bu.edu', 
        user='mchang15',
        password='bmms12s091', 
        db='mchang15',
        port=4253
    ) 
except pymysql.Error as e: 
        print(str(e))

def sanitize_input(input_str):
    sanitized_str = ""
    for char in input_str:
        if char:
            if char.isalnum():
                sanitized_str += char
            else:
                sanitized_str += "_"
        else:
            char = None
    return sanitized_str
            
# Get uploaded file data
file_item = form['fileInput']

# Check the Content-Type header to determine the file type
content_type = file_item.type
if "excel" in content_type:
    file_format = "Excel"
elif "csv" in content_type:
    file_format = "CSV"
else:
    file_format = "Unknown"

# Read file data based on file format
file_data = file_item.file.read()
if file_format == "Excel":
    df = pd.read_excel(BytesIO(file_data), engine='openpyxl')
elif file_format == "CSV":
    df = pd.read_csv(BytesIO(file_data))

# Define the table name in your database
table_name = form.getvalue('strainName')
table_name = sanitize_input(f"{table_name}")

# Create a cursor object
cursor = connection.cursor()

if table_name:
    # Create the table in the database based on the DataFrame columns
    #check_table_query = "SELECT COUNT(*) AS table_exists FROM information_schema.tables WHERE table_schema = 'Team_1' AND table_name = %s"
    #cursor.execute(check_table_query, table_name)
    #print(check_table_query, table_name)
    #existing_table = cursor.fetchall()
    #if not existing_table:
        
    # Create the table in the database based on the DataFrame columns
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for column in df.columns:
      column_text = sanitize_input(column)
      create_table_query += f"{column_text} VARCHAR(255), "
      
    create_table_query = create_table_query[:-2] + ")"  #Remove the last comma and space 
    cursor.execute(create_table_query)
    print(create_table_query)

    #Upload the data from the DataFrame to the MySQL table
    for _, row in df.iterrows():
        # Convert NaN values to None in the row
        row = [None if pd.isna(value) else value for value in row]

        mouseID = row[0]  #Assuming the first column contains the value you want
        print("mouseID:", mouseID)
        check_query = f"SELECT * FROM {table_name} WHERE mouseID = %s"
        print("TESTING",check_query, (mouseID))
        cursor.execute(check_query, mouseID)
        print(check_query, mouseID)
        existing_mouse = cursor.fetchall()
        if not existing_mouse:
            #if the mouse does not exist yet
            insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s']*len(row))})"
            cursor.execute(insert_query, tuple(row))
            print(insert_query, tuple(row))

# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

print("Data uploaded successfully.")
