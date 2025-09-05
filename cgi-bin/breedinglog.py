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

# Define the base query
query = "SELECT B.cage_number, C.setup_date AS setupdate, B.studID, A1.strain_name AS stud_strain, B.dameID, A2.strain_name AS dame_strain, L.pup_number, L.pup_dob, B.harem_status FROM Breeding B JOIN Cage C ON B.cage_number = C.cage_number LEFT JOIN Animal A1 ON B.studID = A1.mouseID LEFT JOIN Animal A2 ON B.dameID = A2.mouseID LEFT JOIN Litter L ON B.dameID = L.dameID WHERE 1=1"
params = []

# Add conditions based on form data
if 'BreedingCage' in form:
    BreedingCage = form.getvalue('BreedingCage')
    if BreedingCage:
        query += " AND B.cage_number LIKE %s"
        params.append(f'%{BreedingCage}%')

if 'SetupDate' in form:
    SetupDate = form.getvalue('SetupDate')
    if SetupDate:
        query += " AND setupdate LIKE %s"
        params.append(f'%{SetupDate}%')

if 'Strain' in form:
    Strain = form.getvalue('Strain')
    if Strain:
        query += " AND stud_strain LIKE %s"
        params.append(f'%{Strain}%')

if 'Stud' in form:
    Stud = form.getvalue('Stud')
    if Stud:
        query += " AND B.studID LIKE %s"
        params.append(f'%{Stud}%')

if 'Dam' in form:
    Dam = form.getvalue('Dam')
    if Dam:
        query += " AND B.dameID LIKE %s"
        params.append(f'%{Dam}%')

if 'BreedingStatus' in form:
    BreedingStatus = form.getvalue('BreedingStatus')
    if BreedingStatus:
        query += " AND B.harem_status LIKE %s"
        params.append(f'%{BreedingStatus}%')

# Parse sorting parameters
sort_by = form.getvalue('sort')
sort_order = form.getvalue('order')

if sort_by and sort_order:
    if sort_by == "setup_date":
        query += f" ORDER BY C.setup_date {sort_order}"
    elif sort_by == "strain_name":
        query += f" ORDER BY stud_strain {sort_order}"
    elif sort_by == "studID":
        query += f" ORDER BY B.studID {sort_order}"
    elif sort_by == "dameID":
        query += f" ORDER BY B.dameID {sort_order}"

# Execute SQL query with parameters
cursor.execute(query, params)
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
