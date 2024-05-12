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
        print("TESTING:", row)
    
        for index, key in enumerate(headers):
            print("TESTING:", row[index])
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
      
def sql_query(data_dict):
    #STRAIN
    strain_insert = "INSERT INTO Strain (strain_name) VALUES (%s);"
    select_check = f"SELECT strain_name FROM Strain WHERE strain_name = %s;"
    
    #check if the strain exists
    cursor.execute(select_check, data_dict['strain_name'])
    existing_strain = cursor.fetchone()

    if not existing_strain:
        #add if it doesnt exist yet
        cursor.execute(strain_insert, data_dict['strain_name'])
        
    #CAGE
    cage_number_check = "SELECT cage_number FROM Cage WHERE cage_number = %s;"
    cage_insert = "INSERT INTO Cage (cage_number, setup_date) VALUES (%s, %s);"
    #check if the cage exists
    if data_dict['cage_number'] is not None:
      cursor.execute(cage_number_check, data_dict['cage_number'])
      existing_cage = cursor.fetchall()
      if not existing_cage:
          #add if it doesnt exist yet
          cursor.execute(cage_insert, (data_dict['cage_number'], data_dict['setup_date']))
        
    #ANIMAL
    animal_insert = "INSERT INTO Animal (mouseID, strain_name, dob, sex, status, mouse_type, dod, notes, protocol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(animal_insert, (data_dict['mouseID'], data_dict['strain_name'], data_dict['dob'], data_dict['sex'], data_dict['status'], data_dict['mouse_type'], data_dict['dod'], data_dict['notes'], data_dict['protocol']))
    
    #GENOTYPE
    genotype_insert = "INSERT INTO Genotype (strain_name, mouseID, genotype_name, genotype_status) VALUES (%s, %s, %s, %s);"
    genotype_names = data_dict['genotype_name']
    genotype_statuses = data_dict['genotype_status']
    if data_dict['genotype_name']:
        #check if genotypes are lists
        if isinstance(genotype_names, list) and isinstance(genotype_statuses, list):
            #iterate over each pair of genotype_name and genotype_status and execute insert statement
            for name, status in zip(genotype_names, genotype_statuses):
                cursor.execute(genotype_insert, (data_dict['strain_name'], data_dict['mouseID'], name, status))
        else:
            #if not lists, handle as a single value
            cursor.execute(genotype_insert, (data_dict['strain_name'], data_dict['mouseID'], genotype_names, genotype_statuses))
        
    #BREEDING
    breeding_insert = "INSERT INTO Breeding (cage_number, studID, dameID, breeding_date, harem_status) VALUES (%s, %s, %s, %s, %s);"
    animal_check = "SELECT mouseID FROM Animal WHERE mouseID = %s"
    #if studID is not null
    if data_dict['studID']:
        #check if the studID exists in animals yet
        cursor.execute(animal_check, data_dict['studID'])
        existing_stud = cursor.fetchall()
        if not existing_stud:
            #add if it doesnt exist yet
            cursor.execute("INSERT INTO Animal (mouseID, sex) VALUES (%s, %s)", (data_dict['studID'], 'male'))
            
        dameIDs = data_dict['dameID']
        #filter out None values from dameIDs
        dameIDs = [dameID for dameID in dameIDs if dameID is not None]
        
        if data_dict['harem_status'] == "Harem":
            harem_status = True
        elif data_dict['harem_status'] == "Not Harem":
            harem_status = False
        
        #check if dameID is lists
        if isinstance(dameIDs, list):
            #iterate over each dameID and execute INSERT IGNORE statement
            for dameID in dameIDs:
                #check if the dameID exists in animals yet
                cursor.execute(animal_check, dameID)
                existing_dame = cursor.fetchall()
                if not existing_dame:
                    #add if it doesnt exist yet
                    cursor.execute("INSERT INTO Animal (mouseID, sex) VALUES (%s, %s)", (dameID, 'female'))
                cursor.execute(breeding_insert, (data_dict['cage_number'], data_dict['studID'], dameID, data_dict['breeding_date'], harem_status))
        else:
           #check if the dameID exists in animals yet
            cursor.execute(animal_check, data_dict['dameID'])
            existing_dame = cursor.fetchall()
            if not existing_dame:
                #add if it doesnt exist yet
                cursor.execute("INSERT INTO Animal (mouseID, sex) VALUES (%s, %s)", (data_dict['dameID'], 'female'))
            cursor.execute(breeding_insert, (data_dict['cage_number'], data_dict['studID'], data_dict['dameID'], data_dict['breeding_date'], harem_status))
        
    #PARENT-PAIR
    if data_dict['parent_cage']:
        cursor.execute(cage_number_check, data_dict['parent_cage'])
        existing_parent_cage = cursor.fetchall()
        if not existing_parent_cage:
            #add if it doesnt exit yet
            cursor.execute("INSERT INTO Cage (cage_number) VALUES (%s);", data_dict['parent_cage'])
    if data_dict['male_parentID']:
        cursor.execute(animal_check, data_dict['male_parentID'])
        existing_male_parent = cursor.fetchall()
        if not existing_male_parent:
            #add if it doesnt exit yet
            cursor.execute("INSERT INTO Animal (mouseID, sex) VALUES (%s, %s)", (data_dict['male_parentID'], 'male'))       
    if data_dict['female_parentID']:
        cursor.execute(animal_check, data_dict['female_parentID'])
        existing_female_parent = cursor.fetchall()
        if not existing_female_parent:
            #add if it doesnt exit yet
            cursor.execute("INSERT INTO Animal (mouseID, sex) VALUES (%s, %s)", (data_dict['female_parentID'], 'female'))
    
    #create a smaller dictionary with the non-None values
    smaller_dict = {
        'cage_number' if k == 'parent_cage' else 'studID' if k == 'male_parentID' else 'dameID' if k == 'female_parentID' else k: v
        for k, v in data_dict.items()  # Iterate over key-value pairs in data_dict
        if v is not None and k in ['parent_cage', 'male_parentID', 'female_parentID']  # Filter keys and values
    }
    parent_pair_check = "SELECT breedingID FROM Breeding WHERE "
    parent_pair_check_conditions = []
    parent_pair_insert = "INSERT INTO Breeding ("
    parent_pair_insert_conditions = []
    parent_pair_values = []

    for key, value in smaller_dict.items():
        parent_pair_check_conditions.append(f"{key} = %s")
        parent_pair_insert_conditions.append(key)
        parent_pair_values.append(value)
                               
    parent_pair_insert += ", ".join(parent_pair_insert_conditions)
    parent_pair_insert += ") VALUES ("
    parent_pair_insert += ", ".join(["%s"] * len(parent_pair_values))  # Using %s placeholders for parameterized execution
    parent_pair_insert += ")"

    parent_pair_check += " AND ".join(parent_pair_check_conditions)
    cursor.execute(parent_pair_check, parent_pair_values)
    existing_parent_pair_check = cursor.fetchall()
    if not existing_parent_pair_check:
        #add if it doesnt exit yet
        cursor.execute(parent_pair_insert, parent_pair_values)
        breedingID = cursor.lastrowid
    else:
        breedingID = existing_parent_pair_check
    
    #get the breedingID just created
    cursor.execute("INSERT INTO Parent_Pair (parent_pairID, mouseID) VALUES (%s, %s);", (breedingID, data_dict['mouseID']))

    #CAGE-ASSIGNMENT
    cage_assignment_insert = "INSERT INTO Cage_Assignments (mouseID, cage_number, cage_type, date_of_assignment, date_of_removal) VALUES (%s, %s, %s, %s, %s);"
    if data_dict['cage_type'] is not None:
      cursor.execute(cage_assignment_insert, (data_dict['mouseID'], data_dict['cage_number'], data_dict['cage_type'], data_dict['date_of_assignment'], data_dict['date_of_removal']))
    
    #LITTER
    litter_insert = "INSERT INTO Litter (dameID, pup_number, pup_dob) VALUES (%s, %s, %s);"
    if (data_dict['pup_number'] is not None or data_dict['pup_dob'] is not None):
        cursor.execute(litter_insert, (data_dict['mouseID'], data_dict['pup_number'], data_dict['pup_dob']))

if filtered_data is None:
    print(json.dumps({'error': 'filteredData not found in form data'}))
else:
    # Process the received data (e.g., store in database, perform calculations, etc.)
    # For demonstration purposes, just print the received data
    #print("Received filtered data:")
    #print(filtered_data)
    
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
          
    cursor = connection.cursor()
    
    try: 
          print(filtered_data)
          create_dictionaries(filtered_data)
          
    except pymysql.Error as e:
          print(str(e))
    
    connection.commit()
    cursor.close()
    connection.close()