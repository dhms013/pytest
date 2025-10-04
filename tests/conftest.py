import pytest
import requests
import random
import string
import os
from faker import Faker
from dotenv import load_dotenv

load_dotenv()
fake = Faker()

@pytest.fixture(scope="session")
def base_url():
    host = os.getenv('APP_HOST')
    port = os.getenv('APP_PORT')
    
    if host and port:
        return f"http://{host}:{port}"
    else:
        raise ValueError("APP_HOST or APP_PORT not found in environment. Check .env file.")

@pytest.fixture(scope="session")
def shared_state():
    # This part runs at the beginning of the test session
    print("\nStarting a new test session...")
    yield {}
    # This part runs at the end of the test session (teardown)
    print("\nCleaning up users after session...")


# Fixture to generate random user data
@pytest.fixture(scope="function")
def user_data():
    def get_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    # first_name = get_random_string(8).capitalize()
    # last_name = get_random_string(8).capitalize()
    random_four_digits = random.randint(1000, 9999)
    # name = f"{first_name} {last_name}"
    name = fake.name()
    first_name = name.split(" ")[0]
    phone_number = f"6143{random.randint(1000000, 9999999)}"
    email = f"{first_name.lower()}{random_four_digits}@yopmail.com"
    password = f"password_{random.randint(1000, 9999)}"

    return {
        "name": name,
        "phoneNumber": phone_number,
        "email": email,
        "password": password
    }