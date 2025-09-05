#!/usr/bin/env python3
import pymysql
import cgi
import cgitb
import json

# Enable CGI traceback for debugging
cgitb.enable()

# Print the HTTP header
print("Content-Type: text/html\n")

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
    
    # Construct the SQL query based on filter parameters
    query = """
    SELECT COUNT(*) AS NumAliveMice
    FROM Animal
    WHERE Status NOT IN ('Sacrificed', 'Dead');
    """

    # Execute the query with parameters
    cursor.execute(query)

    # Fetch the result
    rows = cursor.fetchall()
    
    
    # Check if there are any rows returned
    if rows:
        # Extract the count from the first row
        num_alive_mice = rows[0]['NumAliveMice']
        # Print the count data as JSON
        print(json.dumps({"NumAliveMice": num_alive_mice}))
    else:
        # Handle case when no rows are returned
        print(json.dumps({"NumAliveMice": 0}))

    # Close the cursor and connection
    cursor.close()
    connection.close()

except pymysql.MySQLError as e:
    print("An error occurred:", e)

