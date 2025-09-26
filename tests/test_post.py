import pytest
import requests
import logging
import json

logger = logging.getLogger(__name__)

@pytest.mark.order(1)
def test_post_user(base_url, user_data, shared_state, caplog):
    # 🧪 TEST 1: POST (Create User)
    caplog.set_level(logging.INFO)
    post_url = f"{base_url}/users"
    
    # --- Logging Request ---
    logger.info("--- TEST 1: POST (Create User) ---")
    logger.info(f"Sending POST request to: {post_url}")
    logger.info(f"Request Body: {json.dumps(user_data, indent=2)}")

    # --- API Call ---
    create_response = requests.post(post_url, json=user_data)
    
    # --- Assertions ---
    assert create_response.status_code == 201, f"Expected status 201, got {create_response.status_code}"
    created_user_response = create_response.json()
    assert "user" in created_user_response, "Response must contain the 'user' object."
    user_data = created_user_response.get("user")
    assert "id" in user_data, "The nested 'user' object must contain 'id'."
    
    # --- Logging Response ---
    user_id = user_data["id"] # Extract the ID from the nested object
    logger.info(f"API Status Code: {create_response.status_code}")
    logger.info(f"✅ User created successfully with ID: {user_id}")
    logger.info(f"API Response Body: {json.dumps(created_user_response, indent=2)}")
    
    # Store user_id in shared_state for use in subsequent tests
    shared_state["user_id"] = user_id