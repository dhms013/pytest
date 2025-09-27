import pytest
import requests
import logging
import json

logger = logging.getLogger(__name__)

@pytest.mark.order(5)
def test_delete_user(base_url, shared_state, caplog):
    """
    Tests the DELETE /users/{id} endpoint to delete the user. (Scenario 17)
    """
    caplog.set_level(logging.INFO)
    
    user_id = shared_state.get("user_id")
    assert user_id is not None, "FATAL: User ID not found in shared_state. Previous test likely failed."
    
    delete_url = f"{base_url}/users"
    delete_payload = {"id": user_id}

    # --- Logging Request ---
    logger.info("--- TEST 5: DELETE (Delete User) (Scenario 17) ---")
    logger.info(f"Sending DELETE request to: {delete_url}")
    logger.info(f"Deleting user with ID: {user_id}")
    
    # --- API Call ---
    delete_response = requests.delete(delete_url, json=delete_payload)
    
    # --- Assertions ---
    assert delete_response.status_code == 200, f"Expected status 200, got {delete_response.status_code}"
    
    response_json = delete_response.json()
    assert "message" in response_json, "Response must contain a 'message' field."
    assert "deleted" in response_json["message"].lower(), "Message must indicate successful deletion."

    # --- Logging Response ---
    logger.info(f"API Status Code: {delete_response.status_code}")
    logger.info(f"✅ User deleted successfully.")
    logger.info(f"API Response Body: {json.dumps(response_json, indent=2)}")