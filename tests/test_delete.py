import pytest
import requests
import logging
import json

logger = logging.getLogger(__name__)

@pytest.mark.order(4)
def test_delete_user(base_url, shared_state, caplog):
    # 🧪 TEST 4: DELETE (Delete User)
    caplog.set_level(logging.INFO)
    delete_url = f"{base_url}/users"
    user_id = shared_state.get("user_id")
    delete_data = {"id": user_id}

    # --- Logging Request ---
    logger.info("--- TEST 4: DELETE (Delete User) ---")
    logger.info(f"Sending DELETE request to: {delete_url}")
    logger.info(f"Request Body: {json.dumps(delete_data, indent=2)}")

    # --- API Call ---
    delete_response = requests.delete(delete_url, json=delete_data)

    # --- Assertions ---
    assert delete_response.status_code == 200, f"Expected status 200, got {delete_response.status_code}"
    deleted_user_response = delete_response.json()
    assert "user" in deleted_user_response, "Response must contain the 'user' object."
    deleted_user = deleted_user_response.get("user")
    assert deleted_user["id"] == user_id, f"Expected deleted user ID to be {user_id}, got {deleted_user['id']}"

    # --- Logging Response ---
    logger.info(f"API Status Code: {delete_response.status_code}")
    logger.info(f"✅ User deleted successfully: {deleted_user['name']}")
    logger.info(f"API Response Body: {json.dumps(deleted_user_response, indent=2)}")
