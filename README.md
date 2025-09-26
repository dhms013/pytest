# Pytest for beginners

This is only backup repository. I'm starting to learn API test using Python in my free time

## Note
This repository contains a custom Flask application and custom Pytest scripts for automating API testing. The test scenarios cover simple CRUD API testing. The Flask application automatically generates JSON file as the database, and the Pytest scripts automatically generate and open HTML reports. Ensure you have Python installed before attempting this repository.

## Steps to start this pytest using any terminal :
1. python -m venv venv       # Create your virtual environment
2. activate the virtual environment using one of this commands
- source venv/bin/activate  # On macOS/Linux
- venv\Scripts\activate      # On Windows
3. pip install -r requirements.txt
4. python app.py
5. open new terminal
6. activate the virtual environment using the command you use in the step 2
7. pytest tasks.py test (if you only want to run the pytest) OR pytest tasks.py (if you want to run the test and generate and open the report)
