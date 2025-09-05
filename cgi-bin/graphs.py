#!/usr/bin/env python3
import cgi
import pymysql.cursors
import json

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
except pymysql.Error as e:
    print(f"Database connection error: {e}")
    exit()

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Parse form data
form = cgi.FieldStorage()

mouse_status = form.getvalue('mouse-status')
group1 = form.getvalue('group1')
group2 = form.getvalue('group2')

# Construct SQL query
query = f"SELECT COUNT(DISTINCT mouseID) AS count FROM Animal a JOIN Parent_Pair P using(mouseID) JOIN Breeding b on parent_pairID = breedingID WHERE 1=1"
params = []

if group1:
    if group1 == "Sex":
        sql_query += ', sex'
    elif group1 == "MouseType":
        sql_query += ', type'
    elif group1 == "MouseStatus":
        sql_query += ', status'
    elif group1 == "ParentCage":
        sql_query += ', b.cage_number as ParentCage'
    elif group1 == "AgeWeeks":
        sql_query += ', DATEDIFF(CURRENT_DATE(), dob)/7 as ageWeek'
    elif group1 == "CageNumber":
        sql_query += ', ca.cage_number as CageNumber'

if group2:
    if group2 == "Sex":
        sql_query += ', sex'
    elif group2 == "MouseType":
        sql_query += ', type'
    elif group2 == "MouseStatus":
        sql_query += ', status'
    elif group2 == "ParentCage":
        sql_query += ', b.cage_number as ParentCage'
    elif group2 == "AgeWeeks":
        sql_query += ', DATEDIFF(CURRENT_DATE(), dob)/7 as ageWeek'
    elif group2 == "CageNumber":
        sql_query += ', ca.cage_number as CageNumber'

selected_table = form.getvalue('selected_table')
query += " AND strain_name LIKE %s"
params.append(f'%{selected_table}%')

if mouse_status == 'alive':
    query += " AND status IN ('breeding', 'set for breeding', 'used for study', '', 'none')"
elif mouse_status == 'all':
    pass

group_by_clause = ""

if group1:
    if group1 == "Sex":
        group_by_clause += 'sex'
    elif group1 == "MouseType":
        group_by_clause += 'type'
    elif group1 == "MouseStatus":
        group_by_clause += 'status'
    elif group1 == "ParentCage":
        group_by_clause += 'b.cage_number'
    elif group1 == "AgeWeeks":
        group_by_clause += 'DATEDIFF(CURRENT_DATE(), dob)/7'
    elif group1 == "CageNumber":
        group_by_clause += 'ca.cage_number'
        
    if group2:
        group_by_clause += ", "
        if group2 == "Sex":
            group_by_clause += 'sex'
        elif group2 == "MouseType":
            group_by_clause += 'type'
        elif group2 == "MouseStatus":
            group_by_clause += 'status'
        elif group2 == "ParentCage":
            group_by_clause += 'b.cage_number'
        elif group2 == "AgeWeeks":
            group_by_clause += 'DATEDIFF(CURRENT_DATE(), dob)/7'
        elif group2 == "CageNumber":
            group_by_clause += 'ca.cage_number'

elif group2:
    if group2 == "Sex":
        group_by_clause += 'sex'
    elif group2 == "MouseType":
        group_by_clause += 'type'
    elif group2 == "MouseStatus":
        group_by_clause += 'status'
    elif group2 == "ParentCage":
        group_by_clause += 'b.cage_number'
    elif group2 == "AgeWeeks":
        group_by_clause += 'DATEDIFF(CURRENT_DATE(), dob)/7'
    elif group2 == "CageNumber":
        group_by_clause += 'ca.cage_number'

if group_by_clause:
    query += f" GROUP BY "
    query += group_by_clause

# Execute SQL query
print(query, params)
cursor.execute(query, params)
data = cursor.fetchall()

# Close database connection
connection.close()

# Print the result as JSON
print("Content-type: application/json\r\n")
print(json.dumps(data))
