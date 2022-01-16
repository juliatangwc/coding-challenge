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