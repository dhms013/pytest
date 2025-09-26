from flask import Blueprint, request, jsonify
from .data_handler import get_users_data

# Create a Blueprint instance for GET operations
get_bp = Blueprint('get_users', __name__)

# Utility function to prepare user data for a safe response (omit password/token)
def prepare_safe_user_response(user):
    """Removes the 'password' and 'register_token' fields for a safe response."""
    safe_user = user.copy()
    safe_user.pop('password', None)
    return safe_user

@get_bp.route('/users', methods=['GET'])
def get_users():
    """Handles retrieval of users based on query parameters."""
    
    # Read existing users data using the handler
    users_data = get_users_data()

    # Get query parameters
    name = request.args.get('name')
    phone_number = request.args.get('phoneNumber')
    email = request.args.get('email')
    # Use request.args.get() and specify type=int for 'id'
    user_id = request.args.get('id', type=int)

    # Check if no parameters are provided
    if not name and not phone_number and not email and user_id is None:
        # Return all users without passwords
        users_without_passwords = [prepare_safe_user_response(user) for user in users_data]
        return jsonify({
            'message': 'Retrieved all data', 
            'users': users_without_passwords
        }), 200

    # Filter based on query parameters
    filtered_users = users_data

    # Apply filters only if the parameter is present
    if name:
        # Case-insensitive name comparison
        filtered_users = [user for user in filtered_users if user.get('name', '').lower() == name.lower()]
    
    if phone_number:
        # Exact phone number comparison
        filtered_users = [user for user in filtered_users if user.get('phoneNumber') == phone_number]
        
    if email:
        # Case-insensitive email comparison (assuming stored in lowercase, but using .lower() for safety)
        filtered_users = [user for user in filtered_users if user.get('email', '').lower() == email.lower()]
    
    if user_id is not None:
        # Exact ID comparison
        filtered_users = [user for user in filtered_users if user.get('id') == user_id]

    # Handle the case of no users found
    if len(filtered_users) == 0:
        return jsonify({'message': 'User not found'}), 404

    # Prepare response data (omitting passwords)
    users_without_passwords = [prepare_safe_user_response(user) for user in filtered_users]

    # Handle the case of a single user found
    if len(users_without_passwords) == 1:
        return jsonify({
            'message': 'Retrieved data', 
            'user': users_without_passwords[0]
        }), 200

    # Handle the case of multiple users found
    return jsonify({
        'message': 'Retrieved data', 
        'users': users_without_passwords
    }), 200
