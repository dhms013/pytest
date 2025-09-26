from flask import Blueprint, request, jsonify
import re
from .data_handler import get_users_data, save_users_data

# Create a Blueprint instance for PUT operations
put_bp = Blueprint('put_users', __name__)

# Regex patterns (compiled for efficiency)
# Name: only alphabets and spaces
NAME_REGEX = re.compile(r'^[a-zA-Z\s]+$')

# Phone Number: only numbers, 9 to 12 digits
PHONE_REGEX = re.compile(r'^\d{9,12}$')

# Email: enforced lowercase, format allows for multiple TLD segments (e.g., mail.co.us)
EMAIL_FORMAT_REGEX = re.compile(r'^[^\s@]+@[^\s@]+(\.[^\s@]+)+$')

def validate_user_fields(data, required_fields=None):
    # 1. Check for missing required fields (POST only)
    if required_fields:
        if not all(field in data for field in required_fields):
            return {"error": "Missing required fields"}, 400

    # 2. Validate Name
    # The validation inside the block only runs if 'name' is IN data (optional for PUT)
    if 'name' in data:
        if not NAME_REGEX.match(data['name']):
            return {"error": "Invalid name: Only alphabets and spaces allowed"}, 422
    
    # 3. Validate Phone Number
    # The validation inside the block only runs if 'phoneNumber' is IN data (optional for PUT)
    if 'phoneNumber' in data:
        phone_number = data['phoneNumber']
        if not PHONE_REGEX.match(phone_number):
            if len(phone_number) < 9:
                return {"error": "Phone number is too short (minimum 9 digits)"}, 422
            elif len(phone_number) > 12:
                return {"error": "Phone number is too long (maximum 12 digits)"}, 422
            else:
                return {"error": "Invalid phone number format"}, 422
    
    # 4. Validate Email
    # The validation inside the block only runs if 'email' is IN data (optional for PUT)
    if 'email' in data:
        email = data['email']
        
        # A. Enforce strictly lowercase input (Strict format validation)
        if any(c.isupper() for c in email):
            return {"error": "Email must be in all lowercase letters."}, 422

        # B. Validate email format (Strict format validation)
        if not EMAIL_FORMAT_REGEX.match(email):
            return {"error": "Invalid email format"}, 422

    # If all checks pass
    return None, None

@put_bp.route('/users', methods=['PUT'])
def update_user():
    """Handles updating a user's information via PUT request."""

    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
        
    request_data = request.get_json()
    
    # Check for required ID field
    user_id = request_data.get('id')
    if user_id is None:
        return jsonify({"error": 'Missing required field: id'}), 400

    # Ensure ID is an integer for comparison
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": 'Invalid ID format'}), 400

    # Get users data
    users_data = get_users_data()
    
    # Find the user index in the list
    user_index = -1
    for i, user in enumerate(users_data):
        if user.get('id') == user_id:
            user_index = i
            break
            
    if user_index == -1:
        return jsonify({"error": 'User not found'}), 404

    # Prepare data for update (excluding 'id' and potential control fields from being merged)
    updated_data = {k: v for k, v in request_data.items() if k != 'id'}
    
    # IMPORTANT: If the email is being updated, enforce lowercase as per POST rule
    if 'email' in updated_data:
        email = updated_data['email']
        # 1. Enforce strictly lowercase input
        if any(c.isupper() for c in email):
            return jsonify({"error": "Email update must be in all lowercase letters."}), 422
        # No need for further email format validation here; assumed POST enforces format on creation
        # If needed, you would re-run the email regex check from post_users.py here.

    # Update the user's data using dictionary unpacking
    current_user = users_data[user_index]
    users_data[user_index] = {
        **current_user,
        **updated_data,
    }
    
    updated_user = users_data[user_index]

    # Write the updated data to the file
    save_users_data(users_data)
    
    # Create a response object without the password
    response_user = {
        'id': updated_user.get('id'),
        'name': updated_user.get('name'),
        'phoneNumber': updated_user.get('phoneNumber'),
        'email': updated_user.get('email'),
        'register_token': updated_user.get('register_token')
    }
    
    print('Edited User:', request_data)
    
    # Express used 201 Created here, which is unconventional for PUT (usually 200 OK or 204 No Content), but we match the original logic.
    return jsonify({
        'message': 'User updated successfully', 
        'user': response_user
    }), 201
