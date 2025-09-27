import pytest
import requests
import logging
import json

logger = logging.getLogger(__name__)

# --- Search Scenario Setup ---
ALL_SEARCH_FIELDS = ["id", "name", "phoneNumber", "email"]
# The list includes Scenario 2 (All Users) and Scenarios 3-6 (Parameter Search)
SEARCH_SCENARIOS = [("All Users (List)", [])]
for field in ALL_SEARCH_FIELDS:
    SEARCH_SCENARIOS.append((f"Single Parameter ({field}) (Object)", [field]))


def run_user_search(base_url, shared_state, caplog, description, search_fields):
    get_url = f"{base_url}/users"
    
    # Fetch the latest data/ID from shared state
    created_user_data = shared_state.get("user_data_created", {})
    created_user_id = shared_state.get("user_id")

    search_params = {}
    if not search_fields:
        params_to_log = "None (Fetching all users)"
    else:
        for field in search_fields:
            if field == "id":
                search_params[field] = created_user_id
            elif field in created_user_data:
                # Use the latest updated value from shared_state
                search_params[field] = created_user_data[field]
        params_to_log = json.dumps(search_params)
        
    logger.info(f"Sending GET request to: {get_url}")
    logger.info(f"Search Params: {params_to_log}")
    
    get_response = requests.get(get_url, params=search_params)
    assert get_response.status_code == 200, f"Expected status 200, got {get_response.status_code}"
    
    response_data = get_response.json()
    assert "message" in response_data, "Response must contain a 'message' key."

    required_fields_safe = ["id", "name", "email", "phoneNumber"]

    if not search_fields:
        # Scenario: Search All (Expected: Array/List nested under 'users')
        assert "users" in response_data, "No params: Response must contain the top-level 'users' array."
        retrieved_list = response_data.get("users")
        assert isinstance(retrieved_list, list), "'users' value must be a list."
        assert len(retrieved_list) >= 1, "Expected at least one user in the list."
        log_content = f"Found {len(retrieved_list)} users."
    else:
        # Scenario: Search by Param (Expected: Single User Object nested under 'user')
        assert "user" in response_data, "With params: Response must contain a single 'user' object."
        user_data_nested = response_data.get("user")

        # Check for all safe essential fields
        for field in required_fields_safe:
            assert field in user_data_nested, f"With params: User object is missing required field: '{field}'"

        # Verify the returned user matches the search ID
        assert user_data_nested.get("id") == created_user_id, "Returned user ID does not match the requested ID."
        log_content = json.dumps(user_data_nested, indent=2)

    logger.info(f"API Status Code: {get_response.status_code}")
    logger.info(f"✅ Search successful for scenario: {description}")
    logger.info(f"API Response Verification Summary: {log_content}")


@pytest.mark.order(2)
@pytest.mark.parametrize("description, search_fields", SEARCH_SCENARIOS)
def test_get_user_search_initial(base_url, shared_state, caplog, description, search_fields):
    """Tests search with initial user data (Scenarios 2-6)."""
    caplog.set_level(logging.INFO)
    logger.info(f"--- TEST 2: GET (User Search - Initial) - Scenario: {description} ---")
    # This assertion ensures we have an ID to search with before proceeding
    assert shared_state.get("user_id") is not None, "FATAL: User ID not found in shared_state. POST test likely failed."
    run_user_search(base_url, shared_state, caplog, description, search_fields)


@pytest.mark.order(4)
@pytest.mark.parametrize("description, search_fields", SEARCH_SCENARIOS)
def test_get_user_search_after_update(base_url, shared_state, caplog, description, search_fields):
    """Tests search again to validate updated user data (Scenario 12-16)."""
    # This runs after PUT, using the updated data in shared_state.
    caplog.set_level(logging.INFO)
    logger.info(f"--- TEST 4: GET (User Search - After Update) - Scenario: {description} (Scenario 12-16) ---")
    assert shared_state.get("user_id") is not None, "FATAL: User ID not found in shared_state. POST/PUT test likely failed."
    run_user_search(base_url, shared_state, caplog, description, search_fields)


@pytest.mark.order(6)
def test_get_deleted_user_404(base_url, shared_state, caplog):
    """
    Tests the GET /users endpoint with the ID of the deleted user,
    verifying the 404 response (Scenario 14).
    """
    caplog.set_level(logging.INFO)
    
    deleted_user_id = shared_state.get("user_id")
    get_url = f"{base_url}/users"
    search_params = {"id": deleted_user_id}
    
    # --- Logging Request ---
    logger.info(f"--- TEST 6: GET (Deleted User 404) (Scenario 18) ---")
    logger.info(f"Sending GET request for deleted ID: {deleted_user_id}")
    
    # --- API Call ---
    get_response = requests.get(get_url, params=search_params)
    
    # --- Assertions ---
    assert get_response.status_code == 404, f"Expected status 404, got {get_response.status_code}"
    
    response_json = get_response.json()
    assert "message" in response_json, "404 Response must contain a 'message' field."
    assert "not found" in response_json["message"].lower(), "404 message must indicate user was not found."

    # --- Logging Response ---
    logger.info(f"API Status Code: {get_response.status_code}")
    logger.info(f"✅ Verified 404 response for deleted user (Scenario 14).")
    logger.info(f"API Response Body: {json.dumps(response_json, indent=2)}")
