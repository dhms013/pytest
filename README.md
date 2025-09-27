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
7. python tasks.py test (if you only want to run the pytest) OR python tasks.py (if you want to run the test and generate and open the report)

## Test Scenario
1. Create user (test_post.py already clear)
2. Search all user (test_get.py without params)
3. Search user using id (test_get.py)
4. Search user using name (test_get.py)
5. Search user using phoneNumber (test_get.py)
6. Search user using email (test_get.py)
7. Edit user name (test_put.py)
8. Edit user phoneNumber (test_put.py)
9. Edit user email (test_put.py)
10. Edit user password (test_put.py)
11. Edit user name, phoneNumber, email, and password (test_put.py)
12. Search all user after update (test_get.py without params)
13. Search user using id after update (test_get.py)
14. Search user using name after update (test_get.py)
15. Search user using phoneNumber after update (test_get.py)
16. Search user using email after update (test_get.py)
17. Delete user (test_delete.py)
18. Search the deleted user (test_get.py) 