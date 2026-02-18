import pytest
import requests
from client.data.api.supermarket_client import SupermarketAPIClient

# Define the base URLs for testing
BASE_URL_AGENT = "http://test-agent:8001"
BASE_URL_DB = "http://test-db:8000"

@pytest.fixture
def api_client():
    """Creates a new instance of the client before each test"""
    return SupermarketAPIClient(base_url=BASE_URL_AGENT, db_url=BASE_URL_DB)

def test_initialize_session_success(api_client, requests_mock):
    """Test: Does session initialization work when the server returns a valid response?"""
    
    # 1. Prepare the Mock - what the server is supposed to return
    expected_response = {
        "type": "session_initialized",
        "data": {"cart_id": "12345-abcde", "message": "Ready"}
    }
    requests_mock.post(f"{BASE_URL_AGENT}/session/initialize", json=expected_response, status_code=200)

    # 2. Run the actual function
    result = api_client.initialize_session()

    # 3. Assert that the result matches what we expected
    assert result["data"]["cart_id"] == "12345-abcde"
    assert requests_mock.called is True  # Verify that a network request was actually made

def test_get_cart_success(api_client, requests_mock):
    """Test: Does fetching the cart work?"""
    cart_id = "test-cart-id"
    mock_cart_data = {
        "cart": {
            "store_name": "Mega",
            "total_price": 50.0,
            "items": [{"item_name": "Milk", "quantity": 2}]
        }
    }
    
    # Mock the DB on port 8000
    requests_mock.get(f"{BASE_URL_DB}/cart/{cart_id}", json=mock_cart_data, status_code=200)

    result = api_client.get_cart_from_db(cart_id)

    assert result["cart"]["store_name"] == "Mega"
    assert len(result["cart"]["items"]) == 1

def test_server_error_handling(api_client, requests_mock):
    """Test: How does the client handle a 500 server error?"""
    
    # The server returns an internal error
    requests_mock.post(f"{BASE_URL_AGENT}/session/initialize", status_code=500)

    # We expect the function to raise an Exception
    with pytest.raises(Exception) as excinfo:
        api_client.initialize_session()
    
    # Verify that the error message contains relevant information
    assert "500" in str(excinfo.value)