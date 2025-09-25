import pytest
import requests # type: ignore

@pytest.mark.order(2)
def test_get_user(base_url, shared_state):
     # 🧪 TEST 2: GET (Retrieve User)
    assert "user_id" in shared_state
    user_id = shared_state["user_id"]
    print("\n--- Testing GET (Retrieve User) ---")
    get_url = f"{base_url}/users"
    params = {"id": user_id}
    get_response = requests.get(get_url, params=params)
    assert get_response.status_code == 200
    retrieved_user = get_response.json().get("user")
    assert retrieved_user["id"] == user_id
    print(f"✅ User retrieved successfully: {retrieved_user['name']}")
    
@pytest.mark.order(5)
def test_get_after_delete_user(base_url, shared_state):
    # 🧪 TEST 5: GET (Verify user is deleted)
    assert "user_id" in shared_state
    user_id = shared_state["user_id"]
    print("\n--- Testing GET after DELETE (Verification) ---")
    get_url = f"{base_url}/users"
    params = {"id": user_id}
    get_after_delete_response = requests.get(get_url, params=params)
    assert get_after_delete_response.status_code == 404
    print("✅ Verified user is no longer found.")