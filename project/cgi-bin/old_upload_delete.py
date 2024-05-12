#!/usr/bin/env python3

import cgi
import cgitb
from string import Template
import pymysql
import json
import sys
from datetime import datetime

# Enable CGI traceback for debugging
cgitb.enable()

# Print the HTTP header
print("Content-Type: application/json\n")

def connect_to_database():
    try:
        connection = pymysql.connect(
            host='bioed.bu.edu', 
            user='mchang15',
            password='bmms12s091', 
            db='mchang15',
            port=4253
        )
        return connection
    
    except pymysql.Error as e: 
        print(str(e))
        return None

def delete_data(mouse_ids):
    if not mouse_ids:
        return {'error': 'Strain name or mouse IDs not provided.'}, 400

    try:
        connection = connect_to_database()
        if connection is None:
            return {'error': 'Failed to connect to the database.'}, 500

        cursor = connection.cursor()
        
        for mouseid in mouse_ids:
            tables_to_delete = ['Animal', 'Genotype', 'Parent_Pair', 'Cage_Assignments']
            print("TEting:",mouseid)
            
            # Loop through the list of tables mouseID
            for table_name in tables_to_delete:
                delete_query = f"DELETE FROM {table_name} WHERE mouseID = (%s)"
                cursor.execute(delete_query, mouseid)
                print("Testing:", delete_query, mouseid)
                
            tables_to_delete = ['Breeding', 'Litter']
            # Loop through the list of tables dameID
            for table_name in tables_to_delete:
                delete_query = f"DELETE FROM {table_name} WHERE dameID = (%s)"
                cursor.execute(delete_query, mouseid)
                print("Testing:", delete_query, mouseid)
            
            delete_query = f"DELETE FROM Breeding WHERE studID = (%s)"
            cursor.execute(delete_query, mouseid)
            
    
            # Commit the transaction
            connection.commit()


    except Exception as e:
        return {'error': str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Read form data from standard input
try:
    form_data = sys.stdin.read()
    if not form_data:
        raise ValueError("No data received")
    form = json.loads(form_data)
except json.JSONDecodeError as e:
    print(json.dumps({'error': 'Invalid JSON data: ' + str(e)}))
    sys.exit(1)
except Exception as e:
    print(json.dumps({'error': str(e)}))
    sys.exit(1)
    
try:
    if 'mouseIDs' in form:
        # Get the filteredData from the form
        mouse_ids_str = form.get('mouseIDs')
        table_name = form.get('strainName')
        if mouse_ids_str:
            delete_data(mouse_ids_str)
      
except pymysql.Error as e:
      print(str(e))