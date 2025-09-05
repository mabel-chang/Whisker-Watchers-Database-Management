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

    # Get filter parameters from the form
    form = cgi.FieldStorage()
    
    filters = {}
    
    for key in form.keys():
         filters[key] = form.getvalue(key)
   
    params = []

    # Construct the SQL query based on filter parameters
    query = """
    SELECT an.mouseID as MouseID, an.dob as DOB, an.sex as Sex, an.status as Status, an.mouse_type as MouseType, an.dod as DOD, an.notes as Notes, 
           st.strain_name as StrainName, st.strain_status as StrainStatus, 
           c.cage_number as CageNumber, c.setup_date as SetupDate, 
           ca.cage_type as CageType, ca.date_of_assignment as CageAssignmentDate, ca.date_of_removal as CageRemovalDate, 
           br.breeding_date as BreedingDate, 
           CASE
            WHEN br.harem_status IS NULL THEN NULL
            WHEN br.harem_status = 'FALSE' THEN 'Pair'
            ELSE 'Harem'
       	   END AS BreedingType, 
	   br.studID, br.dameID, 
           li.dameID AS LitterMotherID, li.pup_number AS PupID, li.pup_dob AS PupDOB, 
           pr.protocol_link AS Protocol
    FROM Animal AS an
    LEFT JOIN Protocol AS pr ON an.protocolID = pr.protocolID
    LEFT JOIN Strain AS st ON an.mouseID = st.mouseID
    LEFT JOIN Parent_Pair AS pp ON an.mouseID = pp.mouseID
    LEFT JOIN Breeding AS br ON pp.parent_pairID = br.breedingID
    LEFT JOIN Cage_Assignments AS ca ON an.mouseID = ca.mouseID
    LEFT JOIN Cage AS c ON ca.cageID = c.cageID
    LEFT JOIN Litter AS li ON an.mouseID = li.dameID
    WHERE 1=1
    """

    # Get sorting preferences from the form
    sort_column = form.getvalue('sort')
    sort_order = form.getvalue('order')

    if filters:
        for key, value in filters.items():
            if value:
                query += f" AND {key} = '{value}'"
                
    if sort_column and sort_order:
        query += f" ORDER BY {sort_column} {sort_order}"

    # Execute the query with parameters
    cursor.execute(query, params)

    # Fetch the result
    rows = cursor.fetchall()

    # Print the result as HTML table
    if rows:  # Check if rows is not empty
        print("<table border='1'>")
        print("<tr>")
        # Print column headers
        for column in rows[0].keys():
            print("<th>{}</th>".format(column))
        print("</tr>")

        # Print data rows
        for row in rows:
            print("<tr>")
            for value in row.values():
                print("<td>{}</td>".format(value))
            print("</tr>")
        print("</table>")
    else:
        print("<p style='color: red; font-weight: bold;'>ERROR: No data available for selected filtering options. Please try a different combination :)</p>")

        # Add filters if any
        if filters:
            for key in form.keys():
                if key != 'group_by' and filters[key]:
                    count_query += f" AND {key} = %s"
                    params.append(filters[key])
        # Group by the selected variable
        count_query += f" GROUP BY {filters['group_by']}"

        # Execute the count query with parameters
        cursor.execute(count_query, params)
        count_rows = cursor.fetchall()

        # Prepare the data for JSON response
        count_data = [(row['GroupByVariable'], row['MouseCount']) for row in count_rows]

        # Print the count data as JSON
        print("Content-Type: application/json\n")
        print(json.dumps(count_data))

    # Close the cursor and connection
    cursor.close()
    connection.close()

except pymysql.MySQLError as e:
    print("An error occurred:", e)
