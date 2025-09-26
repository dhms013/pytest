import json
import os

# Define the file path for user data
DATA_FILE = 'users.json'

def get_users_data():
    """Reads user data from the JSON file. Returns an empty list if the file is missing or invalid."""
    
    # Check if the file exists
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure the data is a list, otherwise return empty
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError) as e:
        # Handle cases where the file is corrupted or cannot be read
        print(f"Warning: Could not read or decode {DATA_FILE}. Starting with empty data. Error: {e}")
        return []

def save_users_data(users_data):
    """Writes the current list of users to the JSON file."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            # Use indent=2 for human-readable formatting
            json.dump(users_data, f, indent=2)
    except IOError as e:
        print(f"Error: Could not write to {DATA_FILE}. Data might be lost. Error: {e}")

def get_users_data_and_last_id():
    """
    Reads user data and calculates the largest existing 'id' for new user creation.
    Used primarily by the POST endpoint.
    """
    users_data = get_users_data()
    last_id = 0
    if users_data:
        # Calculate the maximum ID present in the current data
        # Use a default of 0 if a user somehow doesn't have an ID
        ids = [user.get('id', 0) for user in users_data if isinstance(user.get('id'), int)]
        if ids:
            last_id = max(ids)
    
    return users_data, last_id

def get_user_index_by_id(users_data, user_id):
    """Utility function to find the index of a user by ID."""
    # Ensure ID is an integer for reliable comparison
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return -1 # Invalid ID type

    for i, user in enumerate(users_data):
        if user.get('id') == user_id:
            return i
    return -1
