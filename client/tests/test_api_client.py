import pytest
import requests
from client.data.api.supermarket_client import SupermarketAPIClient

# Define the base URLs for testing
BASE_URL_AGENT = "http://test-agent:8001"
BASE_URL_DB = "http://test-db:8000"

@pytest.fixture
def api_client():
    """Creates a new instance of the client before each test"""
    print("\n\n[SETUP] Creating a fresh API Client instance...")
    return SupermarketAPIClient(base_url=BASE_URL_AGENT, db_url=BASE_URL_DB)

def test_initialize_session_success(api_client, requests_mock):
    """Test: Does session initialization work when the server returns a valid response?"""
    print("----------------------------------------------------------------")
    print("[TEST START] test_initialize_session_success")
    
    # 1. Prepare the Mock
    expected_response = {
        "type": "session_initialized",
        "data": {"cart_id": "12345-abcde", "message": "Ready"}
    }
    print(f"[MOCK SETUP] Server configured to return: {expected_response}")
    
    requests_mock.post(f"{BASE_URL_AGENT}/session/initialize", json=expected_response, status_code=200)

    # 2. Run the actual function
    print("[ACTION] Calling api_client.initialize_session()...")
    result = api_client.initialize_session()
    print(f"[RESULT] Function returned: {result}")

    # 3. Assertions
    print("[ASSERT] Verifying cart_id matches...")
    assert result["data"]["cart_id"] == "12345-abcde"
    
    print("[ASSERT] Verifying network request was actually made...")
    assert requests_mock.called is True
    
    print("[TEST END] ✅ Success!")

def test_get_cart_success(api_client, requests_mock):
    """Test: Does fetching the cart work?"""
    print("----------------------------------------------------------------")
    print("[TEST START] test_get_cart_success")
    
    cart_id = "test-cart-id"
    mock_cart_data = {
        "cart": {
            "store_name": "Mega",
            "total_price": 50.0,
            "items": [{"item_name": "Milk", "quantity": 2}]
        }
    }
    
    # Mock the DB
    print(f"[MOCK SETUP] DB configured for ID '{cart_id}' with data: {mock_cart_data}")
    requests_mock.get(f"{BASE_URL_DB}/cart/{cart_id}", json=mock_cart_data, status_code=200)

    # Action
    print(f"[ACTION] Fetching cart for ID: {cart_id}...")
    result = api_client.get_cart_from_db(cart_id)
    print(f"[RESULT] Received cart data: {result}")

    # Assertions
    print("[ASSERT] Checking store name is 'Mega'...")
    assert result["cart"]["store_name"] == "Mega"
    
    print("[ASSERT] Checking item count is 1...")
    assert len(result["cart"]["items"]) == 1
    
    print("[TEST END] ✅ Success!")

def test_server_error_handling(api_client, requests_mock):
    """Test: How does the client handle a 500 server error?"""
    print("----------------------------------------------------------------")
    print("[TEST START] test_server_error_handling")
    
    # Mock Error
    print("[MOCK SETUP] Configuring server to crash (Status 500)...")
    requests_mock.post(f"{BASE_URL_AGENT}/session/initialize", status_code=500)

    # Expect Exception
    print("[ACTION] Calling initialize_session() inside pytest.raises block...")
    
    with pytest.raises(Exception) as excinfo:
        api_client.initialize_session()
    
    print(f"[RESULT] Caught expected exception: '{excinfo.value}'")
    
    # Assert
    print("[ASSERT] Verifying exception message contains '500'...")
    assert "500" in str(excinfo.value)
    
    print("[TEST END] ✅ Success (Error was handled correctly)!")