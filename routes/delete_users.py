from flask import Blueprint, request, jsonify
from .data_handler import get_users_data, save_users_data

# Create a Blueprint instance for DELETE operations
delete_bp = Blueprint('delete_users', __name__)

@delete_bp.route('/users', methods=['DELETE'])
def delete_user():
    """Handles deleting a user's information via DELETE request."""

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

    # Store the deleted user data before removing it
    deleted_user = users_data[user_index]

    # Remove the user from the array using list splicing
    users_data.pop(user_index)

    # Write the updated data to the file
    save_users_data(users_data)
    
    # Create a response object without the password
    response_user = {
        'id': deleted_user.get('id'),
        'name': deleted_user.get('name'),
        'phoneNumber': deleted_user.get('phoneNumber'),
        'email': deleted_user.get('email'),
        'register_token': deleted_user.get('register_token')
    }

    print('Deleted Id:', user_id)
    
    # Return 200 OK status
    return jsonify({
        'message': 'User deleted successfully', 
        'user': response_user
    }), 200
