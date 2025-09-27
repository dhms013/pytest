import pytest
import requests
import logging
import json

logger = logging.getLogger(__name__)

# Fields that can be updated
UPDATE_FIELDS = ["name", "phoneNumber", "email", "password"]

UPDATE_SCENARIOS = []
# Full Update (Scenario 11)
UPDATE_SCENARIOS.append(("Full Update (All Fields)", UPDATE_FIELDS))
# Partial Updates (Scenarios 7, 8, 9, 10)
for field in UPDATE_FIELDS:
    UPDATE_SCENARIOS.append((f"Partial Update ({field})", [field]))


@pytest.mark.order(3)
@pytest.mark.parametrize("description, fields_to_update", UPDATE_SCENARIOS)
def test_put_user_update(base_url, shared_state, caplog, user_data, description, fields_to_update):
    """
    Tests the PUT /users/{id} endpoint with partial and full updates. (Scenarios 7-11)
    Updates shared_state with the successful changes for later validation.
    """
    caplog.set_level(logging.INFO)
    
    user_id = shared_state.get("user_id")
    assert user_id is not None, "FATAL: User ID not found in shared_state. POST test failed."
    
    put_url = f"{base_url}/users" # Assuming the URL is /users as per Flask app structure

    # Use the 'user_data' fixture for fresh update values
    new_data = user_data 
    
    # Build the payload
    # The API expects the ID in the body for PUT /users
    update_payload = {"id": user_id} 
    
    for field in fields_to_update:
        if field in new_data:
            update_payload[field] = new_data[field]
        
    # --- Logging Request ---
    logger.info(f"--- TEST 3: PUT (Update User) - Scenario: {description} (Scenarios 7-11) ---")
    logger.info(f"Sending PUT request to: {put_url}")
    logger.info(f"Request Body: {json.dumps(update_payload, indent=2)}")
    
    # --- API Call ---
    update_response = requests.put(put_url, json=update_payload)
    
    # --- Assertions ---
    # Asserting for 201 CREATED status code (as returned by the Flask app)
    assert update_response.status_code == 201, f"Expected status 201, got {update_response.status_code}"
    
    updated_user_response = update_response.json()
    assert "user" in updated_user_response, "Response must contain the nested 'user' object."
    updated_user = updated_user_response.get("user")
    
    # Get the current stored data to update only the fields that were successful
    current_stored_data = shared_state.get("user_data_created", {})
    
    # Verification and Shared State Update
    for field in fields_to_update:
        expected_value = update_payload[field]
        
        # FIX: The API will not return the password, so we only assert it if it's not the password field.
        if field != "password":
            actual_value = updated_user.get(field)
            assert actual_value == expected_value, f"Field '{field}' update failed. Expected '{expected_value}', got '{actual_value}'."
        
        # ALWAYS update shared state, even for password, because the subsequent GET test needs it for comparison.
        current_stored_data[field] = expected_value

    shared_state["user_data_created"] = current_stored_data

    # --- Logging Response ---
    logger.info(f"API Status Code: {update_response.status_code}")
    logger.info(f"✅ User updated successfully: {description}")
    logger.info(f"API Response Body: {json.dumps(updated_user_response, indent=2)}")
