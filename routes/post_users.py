from flask import Blueprint, request, jsonify
from uuid import uuid4
# Import the shared validation function
from .validation_utils import validate_user_fields
from .data_handler import get_users_data_and_last_id, save_users_data

# Create a Blueprint instance for POST operations
post_bp = Blueprint('post_users', __name__)

@post_bp.route('/users', methods=['POST'])
def create_user():
    """Handles the creation of a new user via POST request."""
    
    # Ensure the request body is valid JSON
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
        
    new_user_data = request.get_json()
    
    # Define required fields for creation
    required_fields = ['name', 'phoneNumber', 'email', 'password']
    
    # Run validation checks using the shared utility
    validation_error, status_code = validate_user_fields(new_user_data, required_fields=required_fields)
    if validation_error:
        return jsonify(validation_error), status_code

    # --- No need for .lower() here, as validation now guarantees it is lowercase ---
    
    # Load existing data and calculate the next ID
    users_data, last_id = get_users_data_and_last_id()
    
    # --- Logic from ExpressJS app ---
    
    # 1. Increment lastId for the new user
    new_user_data['id'] = last_id + 1
    
    # 2. Generate a unique register_token (UUID)
    new_user_data['register_token'] = str(uuid4())

    # 3. Append the new user to the array
    users_data.append(new_user_data)
    
    # 4. Write the updated data to the file
    save_users_data(users_data)
    
    # 5. Create a response object without the password
    response_user = {
        'id': new_user_data['id'],
        'name': new_user_data['name'],
        'phoneNumber': new_user_data['phoneNumber'],
        'email': new_user_data['email'],
        'register_token': new_user_data['register_token']
    }
    
    # Optional: Log the registration (equivalent to console.log in Express)
    print("Registered User:", new_user_data)
    
    # Return 201 Created status
    return jsonify({
        'message': 'User created successfully', 
        'user': response_user
    }), 201
