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

try:
    # Establish a connection to the database
    connection = pymysql.connect(
        host='bioed.bu.edu',
        user='mchang15',
        password='bmms12s091',
        db='mchang15',
        port=4253
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Execute the SQL query to fetch distinct strain names
    query = "SHOW TABLES"
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Extract strain names from the rows
    strain_names = [row[0] for row in rows]

    # Close the database connection
    connection.close()

    # Construct a JSON response
    response = json.dumps({"strain_names": strain_names})

    # Print the JSON response
    print(response)

except pymysql.Error as e:
    # Handle database errors gracefully
    error_message = {"error": str(e)}
    print(json.dumps(error_message))
    