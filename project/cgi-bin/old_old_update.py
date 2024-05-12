#!/usr/bin/env python3
import pymysql
import cgi
import cgitb
import json

# Enable CGI traceback for debugging
cgitb.enable()

# Print the HTTP header
print("Content-Type: text/html\n")

# Connect to the database
try:
    # Establish database connection
    connection = pymysql.connect(
        host='bioed.bu.edu',
        user='mariavdm',
        password='j0o$T1029',
        database='Team_1',
        port=4253,
        cursorclass=pymysql.cursors.DictCursor
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Get update parameters from the form
    form = cgi.FieldStorage()
    
    # Get update parameters from the form
    up_e_mouseID = form.getvalue("up_e_mouseID")
    up_e_notes = form.getvalue("up_e_notes")
    up_e_status = form.getvalue("up_e_status")
    up_e_dod = form.getvalue("up_e_dod")
    up_e_protocol = form.getvalue("up_e_protocol")
    
    up_e_haremStatus = form.getvalue("up_e_haremStatus")
    up_e_studID = form.getvalue("up_e_studID")
    up_e_dameID = form.getvalue("up_e_dameID")
    up_e_dameIDa = form.getvalue("up_e_dameIDa")
    up_e_dameIDb = form.getvalue("up_e_dameIDb")
    up_e_breedingDate = form.getvalue("up_e_breedingDate")
    
    up_e_cageNumber = form.getvalue("up_e_cageNumber")
    up_e_setupDate = form.getvalue("up_e_setupDate")
    up_e_cageType = form.getvalue("up_e_cageType")
    up_e_cageAssignmentDate = form.getvalue("up_e_cageAssignmentDate")
    up_e_cageRemovalDate = form.getvalue("up_e_cageRemovalDate")
    
    up_e_pupNumber = form.getvalue("up_e_pupNumber")
    up_e_pupDOB = form.getvalue("up_e_pupDOB")

    
    # Define the parameters tuples for each query
    protocol_params = (up_e_protocol)
    cage_params = (up_e_cageNumber, up_e_setupDate)
    animal_params = (up_e_mouseID, up_e_notes, up_e_status, up_e_dod)
    breeding_params = (up_e_haremStatus, up_e_studID, up_e_dameID, up_e_breedingDate)
    cageAssignment_params = (up_e_mouseID, up_e_cageNumber, up_e_cageType, up_e_cageAssignmentDate, up_e_cageRemovalDate)
    Litter_params = (up_e_mouseID, up_e_pupNumber, up_e_pupDOB)
    
    up_e_mouseID as mouseID, 
    up_e_status as status, 
    up_e_dod as dod, 
    up_e_notes as notes, 
     as , 
    up_e_cageNumber as cage_number, 
    up_e_setupDate as setup_date, 
    up_e_cageType as cage_type, 
    up_e_cageAssignmentDate as date_of_assignment,
     up_e_cageRemovalDate as date_of_removal, 
     up_e_haremStatus as harem_status, 
     up_e_studID as studID,
     up_e_dameID as dameID, 
     up_e_pupNumber as pup_number, 
     up_e_pupDOB as pup_dob, 
     up_e_breedingDate as breeding_date, 
    
    
    ## Construct the SQL queries for each table
        #Check if the protocl link exists in the protocol table
        if 
        cursor.execute("SELECT protocol_link FROM Protocol WHERE protocol_link = %s", (up_e_protocol,))
        existing_pro_link = cursor.fetchone()
    
        if existing_pro_link:
            #protocol link already exists in the protocol table, set response 
            response["status"] = "error"
            response["message"] = "MouseID already exists in the database."
        else:
            # Check if the mouseID and Cage number are unique in the cage_assignment table
            cursor.execute("SELECT * FROM cage_assignment WHERE mouse_id = %s AND cage_number = %s", (up_e_mouseID, up_e_cageNumber))
            existing_assignment = cursor.fetchone()
    
            if existing_assignment:
                # Edit the existing row in the cage_assignment table
                cursor.execute("UPDATE cage_assignment SET ... WHERE mouse_id = %s AND cage_number = %s", (up_e_mouseID, up_e_cageNumber))
            else:
                # Add a new row in the cage_assignment table
                cursor.execute("INSERT INTO cage_assignment (mouse_id, cage_number, ...) VALUES (%s, %s, ...)", (up_e_mouseID, up_e_cageNumber, ...))

    
    
    
    
    
    
    
    
    animal_query = "INSERT INTO animal (mouse_id, notes, status, dod, protocol) VALUES (%s, %s, %s, %s, %s)"
    #Check if the protocl link exists in the protocol table
        cursor.execute("SELECT protocol_link FROM Protocol WHERE protocol_link = %s", (up_e_protocol,))
        existing_mouse = cursor.fetchone()
    
        if existing_mouse:
            #protocol link already exists in the animal table, set response status to error
            response["status"] = "error"
            response["message"] = "MouseID already exists in the database."
        else:
            # Check if the mouseID and Cage number are unique in the cage_assignment table
            cursor.execute("SELECT * FROM cage_assignment WHERE mouse_id = %s AND cage_number = %s", (up_e_mouseID, up_e_cageNumber))
            existing_assignment = cursor.fetchone()
    
            if existing_assignment:
                # Edit the existing row in the cage_assignment table
                cursor.execute("UPDATE cage_assignment SET ... WHERE mouse_id = %s AND cage_number = %s", (up_e_mouseID, up_e_cageNumber))
            else:
                # Add a new row in the cage_assignment table
                cursor.execute("INSERT INTO cage_assignment (mouse_id, cage_number, ...) VALUES (%s, %s, ...)", (up_e_mouseID, up_e_cageNumber, ...))
                
    
    
    
    
    
    
    
    
    # Execute the queries with parameters
    cursor.execute(animal_query, animal_params)
    cursor.execute(cage_query, cage_params)
    cursor.execute(breeding_query, breeding_params)
    
    # Commit changes to the database
    connection.commit()

    # Fetch the result
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    
except pymysql.MySQLError as e:
    print("An error occurred:", e)
    
# Send the response back to the JavaScript
print("Content-Type: application/json\n")
print(json.dumps(response)

