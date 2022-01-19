# Dev environment
1. Please have the following installed:
    - PostgreSQL https://www.postgresql.org/download/
    - Python https://www.python.org/downloads/
    - VirtualEnv https://pypi.org/project/virtualenv/

# Instructions for running application    
1. Create a virtual environment 
    $virtualenv env
2. Activate virtual environment
    $source env/bin/activate
3. Install dependencies
    $pip3 install -r requirements.txt
4. Create database 
    $createdb inventory
5. Seed database with "seed_database.py"
    $python3 seed_database.py
6. Run server with "server.py"
    $python3 server.py

# Data schema
Each row will have the following columns:
SKU - integer (primary key, unique)
Name - string
Description - text
Quantity - integer
Unit - string
Location - string
Unit Cost - numeric (2 decimal places)
Image - string (path to image)
Thumbnail - string (path to thumbnail)

# Challenge requirements and features
This app contains all basic CRUD functionality with an additional feature for image upload. 
    