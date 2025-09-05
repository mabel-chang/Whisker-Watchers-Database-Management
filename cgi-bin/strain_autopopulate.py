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

# Read credentials from environment
db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'username')
db_password = os.getenv('DB_PASSWORD', 'password')
db_name = os.getenv('DB_NAME', 'project_db')
db_port = int(os.getenv('DB_PORT', 4253))

# Connect to the database
try:
    # Establish database connection
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=db_port,
        cursorclass=pymysql.cursors.DictCursor
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
    