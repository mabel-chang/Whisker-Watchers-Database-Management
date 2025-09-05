#!/usr/bin/env python3

import cgi
import pymysql
import hashlib
import os
import http.cookies
from datetime import datetime, timedelta

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

# Function to generate session ID
def generate_session_id():
    return hashlib.sha256(os.urandom(128)).hexdigest()

# Function to update session ID in the database
def update_session_id_in_database(email, session_id):
    with connection.cursor() as cursor:
        current_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        sql = "UPDATE Users SET session_id = %s, last_login = %s WHERE email = %s"
        cursor.execute(sql, (session_id, current_time, email))
        connection.commit()

# Function to check if the session has expired
def check_expired(email):
    sql = "SELECT last_login FROM Users WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()  # Fetch the result of the query
        if result:
            last_login = datetime.strptime(result[0], "%m-%d-%Y %H:%M:%S")
            difference = datetime.now() - last_login
            if difference < timedelta(hours=2):
                return False
        else:
            return True


# Function to set session ID as a cookie
# def set_session_cookie(session_id):
#     cookie = http.cookies.SimpleCookie()
#     cookie['session_id'] = session_id
#     cookie['session_id']['path'] = '/'  # Set the cookie path to root
#     print(cookie)

# Function to redirect to home page with session ID
# def redirect_to_home(session_id):
#     print("Content-type: text/html")
#     print("Location: ../html/home.html?session_id=" + session_id)
#     print("")

# Parse form data
form = cgi.FieldStorage()

# Retrieve form data
email = form.getvalue('email')
password = form.getvalue('password')

# Hash the provided password
hashed_password = hashlib.sha256(password.encode()).hexdigest()

# Query the database to check if the credentials exist
with connection.cursor() as cursor:
    sql = "SELECT * FROM Users WHERE email = %s"
    cursor.execute(sql, email)
    user = cursor.fetchone()

# If user exists, check the password
if user:
    stored_hashed_password = user['password_hash']
    if hashed_password == stored_hashed_password:
        # Generate session ID
        session_id = generate_session_id()
        # Update session ID in the database
        update_session_id_in_database(email, session_id)
        # Set session ID as a cookie
        set_session_cookie(session_id)
        # Redirect to the main website with session ID
        redirect_to_home(session_id)
    else:
        # Print error message if password is incorrect
        print("Content-type: text/html")
        print("Location: ../html/sign_in.html?error_message=Incorrect%20email%20or%20password.%20Please%20try%20again.")
        print("")
else:
    # Print error message if email doesn't exist
    print("Content-type: text/html")
    print("Location: ../html/sign_in.html?error_message=Incorrect%20email%20or%20password.%20Please%20try%20again.")
    print("")



