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

# Create the table in the database based on the DataFrame columns
check_table_query = "SELECT COUNT(*) AS table_exists FROM information_schema.tables WHERE table_schema = 'Team_1' AND table_name = %s"
#cursor.execute(check_table_query, table_name)
print(check_table_query, table_name)
#existing_table = cursor.fetchall()
existing_table=1
if existing_table and table_name=="BreedingLog":
    #if table exists and is breedinglog
    for index, row in df.iterrows():
        update_query = f"UPDATE {table_name} SET "
        update_query_where = f"WHERE Dame/F LIKE %s"
        query_col_names = ''
        query_values = ''

        mouseID = row[0]
        row = [None if pd.isna(value) else value for value in row]
        column_names = df.columns.tolist()

        for i, value in enumerate(row):
            if value is not None:
                query_col_names += f"{column_names[i]} = %s, "
                query_values += f"{value}, "
        # Remove the trailing comma and space
        query_col_names = query_col_names[:-2] + " "
        query_values = query_values[:-2]

        update_query += query_col_names
        update_query += update_query_where

        query_values += f", {mouseID}"
        #cursor.execute(update_query, query_values)
        print(update_query, query_values)
        
elif existing_table:
    #if table exists
    for index, row in df.iterrows():
        update_query = f"UPDATE {table_name} SET "
        update_query_where = f"WHERE mouseID LIKE %s"
        query_col_names = ''
        query_values = ''

        mouseID = row[0]
        row = [None if pd.isna(value) else value for value in row]
        column_names = df.columns.tolist()

        for i, value in enumerate(row):
            if value is not None:
                query_col_names += f"{column_names[i]} = %s, "
                query_values += f"{value}, "
        # Remove the trailing comma and space
        query_col_names = query_col_names[:-2] + " "
        query_values = query_values[:-2]

        update_query += query_col_names
        update_query += update_query_where

        query_values += f", {mouseID}"
        #cursor.execute(update_query, query_values)
        print(update_query, query_values)

# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

print("Data uploaded successfully.")