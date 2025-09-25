import pytest
import requests # type: ignore

@pytest.mark.order(3)
def test_put_user(base_url, user_data, shared_state):
    # 🧪 TEST 3: PUT (Update User)
    assert "user_id" in shared_state
    user_id = shared_state["user_id"]
    print("\n--- Testing PUT (Update User) ---")
    put_url = f"{base_url}/users"
    updated_name = f"Updated {user_data['name']}"
    updated_data = {"id": user_id, "name": updated_name}
    update_response = requests.put(put_url, json=updated_data)
    assert update_response.status_code == 201
    updated_user = update_response.json().get("user")
    assert updated_user["name"] == updated_name
    print(f"✅ User updated successfully: {updated_user['name']}")