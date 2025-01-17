import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from etl_pipeline import transform_data  # Import your functions

def test_transform_data():
    raw_data = [
        {"name": "Bitcoin", "symbol": "BTC", "current_price": 50000},
        {"name": "Ethereum", "symbol": "ETH", "current_price": 3000},
    ]
    expected_output = [
        {"name": "Bitcoin", "symbol": "BTC", "price": 50000},
        {"name": "Ethereum", "symbol": "ETH", "price": 3000},
    ]
    assert transform_data(raw_data) == expected_output