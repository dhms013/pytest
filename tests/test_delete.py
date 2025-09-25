import pytest
import requests # type: ignore

@pytest.mark.order(4)
def test_delete_user(base_url, shared_state):
    # 🧪 TEST 4: DELETE (Delete User)
    assert "user_id" in shared_state
    user_id = shared_state["user_id"]
    print("\n--- Testing DELETE (Delete User) ---")
    delete_url = f"{base_url}/users"
    delete_data = {"id": user_id}
    delete_response = requests.delete(delete_url, json=delete_data)
    assert delete_response.status_code == 200
    deleted_user = delete_response.json().get("user")
    assert deleted_user["id"] == user_id
    print(f"✅ User deleted successfully: {deleted_user['name']}")