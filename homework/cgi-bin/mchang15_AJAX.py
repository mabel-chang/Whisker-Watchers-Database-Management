#!/usr/bin/env python3

import cgi
import cgitb
from string import Template
import pymysql
import json

cgitb.enable()

form = cgi.FieldStorage()

print("Content-type: text/html\n")

if (form):
  selector = form.getvalue("selector", "")
  
  if (selector == "histogram"):
      miRNA = form.getvalue("miRNA", "")
  
      try:
          connection = pymysql.connect(
              host='bioed.bu.edu', 
              user='mchang15',
              password='bmms12s091', 
              db='miRNA',
              port=4253
          ) 
      except pymysql.Error as e: 
          print(str(e))
          
      cursor = connection.cursor()
      
      query = """
      select score
      from targets join miRNA using(mid)
      where name=%s
      """
          
      try: 
          cursor.execute(query,miRNA)
          
      except pymysql.Error as e:
          print(str(e))
          
      results = cursor.fetchall()   
      cursor.close()
      connection.close()
      
      print(json.dumps(results))
      
  if (selector == "table"):
      seq = form.getvalue("sequence", "")
      
      try:
          connection = pymysql.connect(
              host='bioed.bu.edu', 
              user='mchang15',
              password='bmms12s091', 
              db='miRNA',
              port=4253
          ) 
      except pymysql.Error as e: 
          print(str(e))
          
      cursor = connection.cursor()
      
      query = """
      select name, seq
      from miRNA
      where seq REGEXP %s
      order by seq ASC
      """
          
      try: 
          cursor.execute(query, seq)
          
      except pymysql.Error as e:
          print(str(e))
          
      results = cursor.fetchall()   
      cursor.close()
      connection.close()
      
      print(json.dumps(results))
