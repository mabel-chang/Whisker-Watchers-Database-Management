#!/usr/bin/env python3
import cgi
import pymysql.cursors
import pandas as pd

# Read credentials from environment
db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'username')
db_password = os.getenv('DB_PASSWORD', 'password')
db_name = os.getenv('DB_NAME', 'project_db')
db_port = int(os.getenv('DB_PORT', 4253))

# Connect to the database
connection = pymysql.connect(
     host=db_host,
     user=db_user,
     password=db_password,
     database=db_name,
     port=db_port,
     cursorclass=pymysql.cursors.DictCursor
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Parse form data
form = cgi.FieldStorage()
selected_table = form.getvalue('selected_table')

# Construct SQL query based on filters
sql_query = f"SELECT * FROM `{selected_table}` WHERE 1=1"
params = []

if 'mouseID' in form:
    mouseID = form.getvalue('mouseID')
    if mouseID:
        sql_query += " AND mouseID LIKE %s"
        params.append(f'%{mouseID}%')

if 'parent_cage' in form:
    parent_cage = form.getvalue('parent_cage')
    if parent_cage:
        sql_query += " AND ParentCage LIKE %s"
        params.append(f'%{parent_cage}%')

if 'cage_number' in form:
    cage_number = form.getvalue('cage_number')
    if cage_number:
        sql_query += " AND CageNumber LIKE %s"
        params.append(f'%{cage_number}%')

if 'breeding_cage' in form:
    breeding_cage = form.getvalue('breeding_cage')
    if breeding_cage:
        sql_query += " AND BreedingCage LIKE %s"
        params.append(f'%{breeding_cage}%')

if 'sex' in form:
    sex = form.getvalue('sex')
    if sex:
        sql_query += " AND Sex = %s"
        params.append(sex)

if 'mouse-type' in form:
    mouse_type = form.getvalue('mouse-type')
    if mouse_type:
        sql_query += " AND MouseType = %s"
        params.append(mouse_type)

if 'mouse-status' in form:
    mouse_status = form.getvalue('mouse-status')  # Get list of selected options
    if mouse_status:
        sql_query += f" AND MouseStatus = %s" 
        params.append(mouse_status)

if 'dob' in form:
    dob = form.getvalue('dob')
    if dob:
        sql_query += " AND DOB = %s"
        params.append(dob)

if 'dod' in form:
    dod = form.getvalue('dod')
    if dod:
        sql_query += " AND DOD = %s"
        params.append(dod)

if 'cage-setup' in form:
    cage_setup = form.getvalue('cage-setup')
    if cage_setup:
        sql_query += " AND CageSetup = %s"
        params.append(cage_setup)

# Parse sorting parameters
sort_by = form.getvalue('sort')
sort_order = form.getvalue('order')

# Map "age" to the "AgeWeeks" column in the SQL query
if sort_by == "age":
    sort_by = "AgeWeeks"

# Construct sorting query
if sort_by and sort_order:
    sql_query += f" ORDER BY {sort_by} {sort_order}"

# Execute SQL query with parameters
cursor.execute(sql_query, params)
data = cursor.fetchall()

# Check if no rows are returned
if len(data) == 0:
    print("Content-type: text/html\n")
    print("<p>No records found matching the selected criteria.</p>")
else:
    # Generate HTML table
    html_table = "<table>"
    # Add table headers
    html_table += "<tr>"
    for column in cursor.description:
        html_table += f"<th>{column[0]}</th>"
    html_table += "</tr>"
    # Add table rows
    for row in data:
        html_table += "<tr>"
        for key, value in row.items():
            html_table += f"<td>{value}</td>"
        html_table += "</tr>"
    html_table += "</table>"

    # Print HTML content
    print("Content-type: text/html\n")
    print(html_table)

# Close database connection
connection.close()
