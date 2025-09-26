import pytest
import requests
import logging
import json

logger = logging.getLogger(__name__)

@pytest.mark.order(3)
def test_put_user(base_url, user_data, shared_state, caplog):
    # 🧪 TEST 3: PUT (Update User)
    caplog.set_level(logging.INFO)

    user_id = shared_state.get("user_id")
    put_url = f"{base_url}/users"

    # --- API Call ---
    updated_name = f"{user_data['name']}"
    update_phoneNumber = f"{user_data['phoneNumber']}"
    update_email = f"{user_data['email']}"
    update_password = f"{user_data['password']}"

    updated_data = {"id": user_id, "name": updated_name, "phoneNumber": update_phoneNumber, "email": update_email, "password": update_password}
    update_response = requests.put(put_url, json=updated_data)

    # --- Logging Request ---
    logger.info("--- TEST 3: PUT (Update User) ---")
    logger.info(f"Sending PUT request to: {put_url}")
    logger.info(f"Request Body: {json.dumps(updated_data, indent=2)}")

    # --- Assertions ---
    assert update_response.status_code == 201, f"Expected status 201, got {update_response.status_code}"
    updated_user_response = update_response.json()
    assert "user" in updated_user_response, "Response must contain the 'user' object."
    updated_user = updated_user_response.get("user")
    assert updated_user["name"] == updated_name, f"Expected name to be updated to {updated_name}, got {updated_user['name']}"

    # --- Logging Response ---
    logger.info(f"API Status Code: {update_response.status_code}")
    logger.info(f"✅ User updated successfully: {updated_user['name']}")
    logger.info(f"API Response Body: {json.dumps(updated_user_response, indent=2)}")
