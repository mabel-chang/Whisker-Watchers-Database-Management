# WhiskerWatchersDB BF768
## Overview
WhiskerWatchersDB is a laboratory database and web application designed to manage mouse strain data efficiently. The system allows users to upload, update, query, and visualize mouse data while maintaining data integrity and consistency. The database integrates multiple strain tables, a breeding log, and user-friendly features such as data filtering, downloadable reports, and basic statistical metrics. This project was commissioned by Dr. Nabil Rabhi, who provided the specifications and requirements for the database system.
  
## Technologies
* Database: MySQL, managed via DBeaver  
* Backend Connectivity:** Python CGI, PyMySQL
* Frontend: HTML, CSS, JavaScript, jQuery
  
## Features
### 1. User Input
* Batch create or update mouse records by uploading Excel sheets.
* Add new records to existing tables or create new tables via text input.
* Delete mouse records using a comma-separated list of IDs from selected tables.

### 2. Query Tables and Graphical Visualizations
* The Home tab displays alive mouse counts for the entire lab and by strain.
* Users can view entire tables or filtered subsets and download in CSV, Excel, or TXT formats.
* Mouse data can be visualized as bar plots or pie charts, grouped by variables, with charts available for download.  

### 3. Documentation
* The Help tab guides users through features of the website.
* Contextual links in other tabs direct users to relevant instructions.
* Protocol documents can be downloaded as Word files based on strain selection.

### 4. Authentication and Authorization
* Session IDs and cookies ensure persistent sessions between tabs.
* Full admin functionality (e.g., account approval and removal) is under development.
* Access is restricted to Dr. Rabhi’s lab personnel; only registered accounts can access all features.
  
## Project Roles
* Mabel Chang: Designed the relational database and implemented core backend functionality, connecting it to user-facing data management interfaces.
* Akhila Gundavelli: Implemented user authentication, including sign-in/out, password reset, and session management.
* Maria van de Meent: Developed front-end interfaces to display mouse information, including tables, charts, and filtering options.
  
## Aknowledgements
We thank Dr. Nabil Rabhi and the Farmer Lab at Boston University, Chobanian & Avedisian School of Medicine, Department of Biochemistry & Cell Biology for commissioning this project and providing guidance on the database requirements.

We thank Dr. Gary Benson for their guidance and instruction during the course, which made this project possible.

Developed as the final project for BF768: Biological Database Analysis at Boston University (S24)
