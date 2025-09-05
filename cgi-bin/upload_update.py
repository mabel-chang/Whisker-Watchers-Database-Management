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

# Get the filteredData from the form
filtered_data = form.get('filteredData')

def create_dictionaries(arr):
    input_date_format = "%m/%d/%Y"
    output_date_format = "%Y-%m-%d"
    
    headers = arr[0]  # First row contains headers
    data = arr[1:]    # Data starts from the second row
    
    strain_names = set()
    cage_numbers = set()
    
    for row in data:
        dictionary = {}
        repeated_headings = []  # List to store repeated headings
    
        for index, key in enumerate(headers):
            value = row[index]
            if value is None:  # Replace None with empty string
                value = ''
            elif isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                # Remove double quotes from the string
                value = value.strip('"')
        
            if isinstance(value, str) and value.strip() != "" and "/" in value:
                try:
                    # Parse the date using the input format
                    date_obj = datetime.strptime(value, input_date_format)
                    # Format the date in the desired output format
                    formatted_date = date_obj.strftime(output_date_format)
                    value = formatted_date
                except ValueError:
                    # Ignore values that cannot be parsed as dates
                    pass
        
            if key in dictionary:
                # If the key already exists, convert the value to a list
                if isinstance(dictionary[key], list):
                    dictionary[key].append(value)
                else:
                    # Convert the existing value to a list and add the new value
                    dictionary[key] = [dictionary[key], value]
                    repeated_headings.append(key)  # Add the repeated heading to the list
            else:
                dictionary[key] = value
        
            # Collect unique strain_names and cage_numbers
            if key == 'strain_name':
                strain_names.add(value)
            elif key == 'cage_number' or key == 'parent_cage':
                cage_numbers.add(value)
        
        cleaned_data_dict = clean_data_dict(dictionary)
        print(cleaned_data_dict)
        
        sql_query(cleaned_data_dict)
        
def clean_data_dict(data_dict):
    cleaned_data = {}
    for key, value in data_dict.items():
        if isinstance(value, list):
            # If the list is empty, set the key to an empty list
            cleaned_list = [v if v != '' else None for v in value]
            cleaned_data[key] = cleaned_list if cleaned_list else []
        else:
            # Handle single values
            cleaned_data[key] = value if value != '' else None  # Replace empty strings with NULL
    return cleaned_data

def generate_update_query(table_name, columns_list, whereID, data_dict, where_dict, typeID):
    # Initialize the update parts list and values list
    update_parts = []
    values = []

    # Iterate over the columns associated with the table
    for column in columns_list:
        value = data_dict.get(column)
        if value is not None:
            if typeID == "update":
                update_parts.append(f"{column} = %s")
            elif typeID == "insert":
                update_parts.append(f"{column}")
            values.append(value)
            
    if typeID == "update":
        # If there are columns to update, create the update query
        if update_parts:
            if isinstance(whereID, list):
                where_conditions = " AND ".join([f"{col} = %s" for col in whereID])
                update_query = f"UPDATE {table_name} SET {', '.join(update_parts)} WHERE {where_conditions};"
                values.extend(where_dict[col] for col in whereID)
            else:
                update_query = f"UPDATE {table_name} SET {', '.join(update_parts)} WHERE {whereID} = %s;"
                values.append(where_dict[whereID]) 
            return update_query, values
        else:
            return None, None
    elif typeID == "insert":
        #If there are columns to insert, create the insert query
        if update_parts:
            update_query = f"INSERT INTO {table_name} ({', '.join(update_parts)}) VALUES ("
            update_query += ", ".join(["%s"] * len(values))  # Using %s placeholders for parameterized execution
            update_query += ")"
            return update_query, values
        else:
            return None, None

def sql_query(data_dict):
    #STRAIN AND MOUSE CHECK
    if data_dict['strain_name'] is not None:
        strain_check = "SELECT strain_name FROM Strain WHERE strain_name = %s;"
        cursor.execute(strain_check, data_dict['strain_name'])
        existing_strain = cursor.fetchall()
        if existing_strain:
            animal_check = "SELECT mouseID FROM Animal WHERE mouseID = %s;"
            cursor.execute(animal_check, data_dict['mouseID'])
            existing_mouse = cursor.fetchall()
            if existing_mouse:
                #ANIMAL
                animal_columns = ['dob', 'status', 'mouse_type', 'dod', 'notes', 'protocol']
                animal_update, animal_update_values = generate_update_query('Animal', animal_columns, 'mouseID', data_dict, data_dict, 'update')
                if animal_update is not None:
                    cursor.execute(animal_update, animal_update_values)
                
                #CAGE + CAGE-ASSIGNMENT
                if data_dict['cage_number'] is not None:
                    cage_number_check = "SELECT cage_number FROM Cage WHERE cage_number = %s;"
                    cage_insert = "INSERT INTO Cage (cage_number, setup_date) VALUES (%s, %s);"
                    #check if the cage exists
                    cursor.execute(cage_number_check, data_dict['cage_number'])
                    existing_cage = cursor.fetchall()
                    if not existing_cage:
                        #add if it doesnt exist yet
                        cursor.execute(cage_insert, (data_dict['cage_number'], data_dict['setup_date']))

                    #update CAGE
                    if data_dict['setup_date'] is not None:
                        cage_columns = ['setup_date']
                        cage_update, cage_update_values = generate_update_query('Cage', cage_columns, 'cage_number', data_dict, data_dict, 'update')
                        cursor.execute(cage_update, cage_update_values)

                    #insert CAGE-ASSIGNMENT if id new, edit if id exists
                    cage_assignment_columns = ['mouseID', 'cage_number', "cage_type", "date_of_assignment", "date_of_removal"]
                    cage_assignment_check = "SELECT cage_assignmentID FROM Cage_Assignments WHERE mouseID = %s && cage_number = %s;"
                    cursor.execute(cage_assignment_check, (data_dict['mouseID'], data_dict['cage_number']))
                    existing_cage_assignment_check = cursor.fetchall()

                    if existing_cage_assignment_check:
                        existing_cage_assignment_check_dict = {}
                        existing_cage_assignment_check_dict["cage_assignmentID"] = existing_cage_assignment_check[0]
                        #if cage assignment exists
                        cage_assignment_update, cage_assignment_update_values = generate_update_query('Cage_Assignments', cage_assignment_columns, 'cage_assignmentID', data_dict, existing_cage_assignment_check_dict, 'update')
                        cursor.execute(cage_assignment_update, cage_assignment_update_values)
                    elif not existing_cage_assignment_check:
                        #if cage assignment doesnt exist yet
                        cage_assignment_update, cage_assignment_update_values = generate_update_query('Cage_Assignments', cage_assignment_columns, '', data_dict, data_dict, 'insert')
                        cursor.execute(cage_assignment_update, cage_assignment_update_values)                        

                #GENOTYPE
                if data_dict['genotype_name'] is not None:
                    if isinstance(data_dict['genotype_name'], list) and isinstance(data_dict['genotype_status'], list):
                        for name, status in zip(data_dict['genotype_name'], data_dict['genotype_status']):
                            update_parts = []
                            values = []

                            if name is not None:
                                update_parts.append("genotype_name = %s")
                                values.append(name)
                            if status is not None:
                                update_parts.append("genotype_status = %s")
                                values.append(status)
                            if update_parts:
                                update_query = f"UPDATE Genotype SET {', '.join(update_parts)} WHERE mouseID = %s AND strain_name = %s;"
                                values.extend([data_dict['mouseID'], data_dict['strain_name']])
                                cursor.execute(update_query, values)
                            
                    else:
                        update_parts = []
                        values = []

                        if data_dict['genotype_name'] is not None:
                            update_parts.append("genotype_name = %s")
                            values.append(data_dict['genotype_name'])
                        if data_dict['genotype_status'] is not None:
                            update_parts.append("genotype_status = %s")
                            values.append(data_dict['genotype_status'])
                        if update_parts:
                            update_query = f"UPDATE Genotype SET {', '.join(update_parts)} WHERE mouseID = %s AND strain_name = %s;"
                            values.extend([data_dict['mouseID'], data_dict['strain_name']])
                            cursor.execute(update_query, values)

                #BREEDING
                breeding_insert = "INSERT IGNORE INTO Breeding (cage_number, studID, dameID, breeding_date, harem_status) VALUES (%s, %s, %s, %s, %s);"
                animal_check = "SELECT mouseID FROM Animal WHERE mouseID = %s"
                #if studID is not null
                if data_dict['studID']:
                    #check if the studID exists in animals yet
                    cursor.execute(animal_check, data_dict['studID'])
                    existing_stud = cursor.fetchall()
                    if not existing_stud:
                        #add if it doesnt exist yet
                        cursor.execute("INSERT IGNORE INTO Animal (mouseID, sex) VALUES (%s, %s)", (data_dict['studID'], 'male'))

                    dameIDs = data_dict['dameID']
                    #filter out None values from dameIDs
                    dameIDs = [dameID for dameID in dameIDs if dameID is not None]

                    #check if dameID is lists
                    if isinstance(dameIDs, list):
                        #iterate over each dameID and execute INSERT IGNORE statement
                        for dameID in dameIDs:
                            #check if the dameID exists in animals yet
                            cursor.execute(animal_check, dameID)
                            existing_dame = cursor.fetchall()
                            if not existing_dame:
                                #add if it doesnt exist yet
                                cursor.execute("INSERT IGNORE INTO Animal (mouseID, sex) VALUES (%s, %s)", (dameID, 'female'))
                            cursor.execute(breeding_insert, (data_dict['cage_number'], data_dict['studID'], dameID, data_dict['breeding_date'], data_dict['harem_status']))
                    else:
                        #check if the dameID exists in animals yet
                        cursor.execute(animal_check, data_dict['dameID'])
                        existing_dame = cursor.fetchall()
                        if not existing_dame:
                            #add if it doesnt exist yet
                            cursor.execute("INSERT IGNORE INTO Animal (mouseID, sex) VALUES (%s, %s)", (data_dict['dameID'], 'female'))
                        cursor.execute(breeding_insert, (data_dict['cage_number'], data_dict['studID'], data_dict['dameID'], data_dict['breeding_date'], data_dict['harem_status']))
                                
                                
                #LITTER
                litter_insert = "INSERT IGNORE INTO Litter (dameID, pup_number, pup_dob) VALUES (%s, %s, %s);"
                if (data_dict['pup_number'] is not None and data_dict['pup_dob'] is not None):
                    cursor.execute(litter_insert, (data_dict['mouseID'], data_dict['pup_number'], data_dict['pup_dob']))

if filtered_data is None:
    print(json.dumps({'error': 'filteredData not found in form data'}))
else:
    # Process the received data (e.g., store in database, perform calculations, etc.)
    # For demonstration purposes, just print the received data
    #print("Received filtered data:")
    #print(filtered_data)

    # Read credentials from environment
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'username')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_name = os.getenv('DB_NAME', 'project_db')
    db_port = int(os.getenv('DB_PORT', 4253))
    
    try:
      connection = pymysql.connect(
          host=db_host,
          user=db_user,
          password=db_password,
          database=db_name,
          port=db_port
      )
    except pymysql.Error as e: 
          print(str(e))
          
    cursor = connection.cursor()
    
    try: 
          create_dictionaries(filtered_data)
          
    except pymysql.Error as e:
          print(str(e))
    
    connection.commit()
    cursor.close()
    connection.close()