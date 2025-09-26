import pytest
import requests
import random
import string
from faker import Faker

fake = Faker()

@pytest.fixture(scope="session")
def base_url():
    # Replace with your actual API's base URL
    return "http://localhost:3000"

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