import pytest
import requests # type: ignore

@pytest.mark.order(1)
def test_post_user(base_url, user_data, shared_state):
    # 🧪 TEST 1: POST (Create User)
    print("\n--- Testing POST (Create User) ---")
    post_url = f"{base_url}/users"
    create_response = requests.post(post_url, json=user_data)
    assert create_response.status_code == 201
    created_user = create_response.json().get("user")
    assert "id" in created_user
    user_id = created_user["id"]
    print(f"✅ User created successfully with ID: {user_id}")
    shared_state["user_id"] = created_user["id"]