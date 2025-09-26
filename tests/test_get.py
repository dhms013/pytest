import pytest
import requests
import logging
import json

logger = logging.getLogger(__name__)

@pytest.mark.order(2)
def test_get_user(base_url, shared_state, caplog):
     # 🧪 TEST 2: GET (Retrieve User)
    caplog.set_level(logging.INFO)
    get_url = f"{base_url}/users"
    user_id = shared_state["user_id"]
    params = {"id": user_id}

    # --- Logging Request ---
    logger.info("--- TEST 2: GET (Retrieve User) ---")
    logger.info(f"Sending GET request to: {get_url}")
    logger.info(f"Using user_id from shared_state: {shared_state.get('user_id')}")

    # --- API Call ---
    get_response = requests.get(get_url, params=params)

    # --- Assertions ---
    assert get_response.status_code == 200, f"Expected status 200, got {get_response.status_code}"
    retrieved_user_response = get_response.json()
    assert "user" in retrieved_user_response, "Response must contain the 'user' object."
    retrieved_user = retrieved_user_response.get("user")
    assert "id" in retrieved_user, "The 'user' object must contain 'id'."

    # --- Logging Response ---
    user_id = retrieved_user["id"]
    logger.info(f"API Status Code: {get_response.status_code}")
    logger.info(f"✅ User retrieved successfully with ID: {user_id}")
    logger.info(f"API Response Body: {json.dumps(retrieved_user_response, indent=2)}")

@pytest.mark.order(5)
def test_get_after_delete_user(base_url, shared_state, caplog):
    # 🧪 TEST 5: GET (Verify user is deleted)
    caplog.set_level(logging.INFO)
    get_url = f"{base_url}/users"
    user_id = shared_state["user_id"]
    params = {"id": user_id}

    #--- Logging Request ---
    logger.info("\n--- TEST 5: GET (Verify user is deleted) ---")
    logger.info(f"Sending GET request to: {get_url}")
    logger.info(f"Using user_id from shared_state: {shared_state.get('user_id')}")
    
    #---API Call ---
    get_after_delete_response = requests.get(get_url, params=params)

    #---Assertions ---
    assert get_after_delete_response.status_code == 404, f"Expected status 404, got {get_after_delete_response.status_code}"

    #---Logging Response ---
    logger.info(f"API Status Code: {get_after_delete_response.status_code}")
    logger.info("✅ Verified user is no longer found.")
    logger.info(f"API Response Body: {json.dumps(get_after_delete_response.json(), indent=2)}")