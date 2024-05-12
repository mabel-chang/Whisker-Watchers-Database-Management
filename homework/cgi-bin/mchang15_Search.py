#!/usr/bin/env python3

import cgi
import cgitb
from string import Template
import pymysql

cgitb.enable()

connection = pymysql.connect(
	host = "bioed.bu.edu",
	user = "mchang15",
	password = "bmms12s091",
	db = "miRNA",
	port = 4253
)

cursor = connection.cursor()

print("Content-type: text/html\n")

#begin HTML
html_template=Template(
"""
<html>
	<head>
		<title>${title}</title>
		${style}
		<script>
		function clearFields() {
			document.getElementById("name").value = "";
			document.getElementById("score").value = "";
			document.getElementById("intro").innerhtml = "";
			document.getElementById("table").innerhtml = "";
		}
		window.onload = clearFields();
		if (window.history.replaceState) {
			window.history.replaceState( null, null, window.location.href );
		}
		</script>
	</head>
	<body>
		<div id="head_explain">
			<p>To get the miRNA information from a gene name, enter the gene name in the textbox, select a targeting score from the drop down, and hit the submit button </p>
		</div>
		<div>
			<h1>Gene Name Search</h1>
			<form action=""https://bioed.bu.edu/cgi-bin/mchang15/mabelchang_test.py" method="post">
				<label for="name">Gene Name:</label>
				<input type="text" if="name" name="name">
				<br>
				<p> Sample Gene Name: A1CF </p>
				<br>
				<label for="score">Maximum Targeting Score:</label>
				<select id="score" name="score">
					<option value = "-0.1" selected>-0.1</option>
					<option value = "-0.2">-0.2</option>
					<option value = "-0.3">-0.3</option>
					<option value = "-0.4">-0.4</option>
					<option value = "-0.5">-0.5</option>
					<option value = "-0.6">-0.6</option>
					<option value = "-0.7">-0.7</option>
				</select>
				<br>
				<input type="submit" value="Submit">
			</form>
		</div>
		<br>
		<div id="table">${intro_html}</div>
		<br>
		<div id="intro">${table_html}</div>
		<br>
		<div id="tail_explain">
			<p>To get the miRNA information from a gene name, enter the gene name in the texbox, select a targeting score from the drop down, and hit the submit button</p>
		</div>
	</body>
</html>
"""
)

#title
title = "Homework 3: miRNA query"

#CSS style
style="""
	<style>
		table, th, td {
			border: 2px solid black;
			border-collapse: collapse;
		}
		th, td {
			padding: 12px;
		}
		th {
			background-color: LightSkyBlue;
		}
		tr:nth-child(even) {
			background-color: LemonChiffon;
		}
		.error {
			color: red;
		}
		#intro {
			font-weight: bold;
		}
	</style>
"""
#intro
intro_html=""

#table
table_html=""

form = cgi.FieldStorage()

#if a gene symbol is submitted
if "name" in form:
	try:
        	us_gene = form.getvalue("name")
        	us_score = form.getvalue("score")

        	query = """
        	select mid, m.name, score
        	from miRNA.gene as g join miRNA.targets using (gid) join miRNA.miRNA as m using (mid)
        	where g.name like %s AND score <= %s;
        	"""

        	try:
            		cursor.execute(query, [us_gene, us_score])
        	except pymysql.Error as e:
            		print(e)

        	results = cursor.fetchall()

        	cursor.close()
        	connection.close()

        	if (results):
            		num_rows = len(results)

            		table_html = Template(
            		"""
            		<table>
                		<thead>
                    			<tr>
                        			<th>miRNA id</th>
                        			<th>miRNA name</th>
                        			<th>score</th>
                    			</tr>
                		</thead>
                		<tbody>${table_rows}</tbody>
            		</table>
            		"""
            		)

            		table_rows = ""

            		for row in results:
                		table_rows += """
                    			<tr>
                        			<td>%s</td>
                        			<td>%s</td>
                        			<td>%s</td>
                    			</tr>
                		""" % (row[0],row[1],row[2])

            		table_html = table_html.safe_substitute(table_rows=table_rows)

        	intro_html += f"""
            		<p>Gene {us_gene} is targeted by {num_rows} miRNAs with score <= {us_score}</p>
        	"""

	except NameError as e:
        	intro_html += f"""
			<p class="error">Entered gene name {us_gene} with score <= {us_score} is not present in the miRNA database </p>
        	"""
else:
	intro_html = ""
	table_html = ""

print(html_template.safe_substitute(title=title, style=style, intro_html=intro_html, table_html = table_html))
